from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie, csrf_protect
from .models import Lecturers,College,Subjects,Incharge, Students, Offerd_course, Section, Course
from django.db.models import F
from django.http import JsonResponse
import json
from django.utils import timezone
from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from .authentication import *
from django.http import HttpResponseRedirect,HttpResponse
import pandas
from django.apps import apps
from .utils.modelValidation import *
from .views2 import *

db_tables = [{"id":1,"tables":'Students'},{"id": 2,"tables":'Course'},{"id": 3,"tables":'Subjects'},{"id": 4,"tables":'Teacher assignment'},{"id": 5,"tables": 'Attendence'},{"id": 6,"tables": 'Lecturers'}]
logger=init_logger()


def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    userid=request.COOKIES.get('userid') 
    token=request.COOKIES.get('token')
    print(token)
    collegeCode=token=request.COOKIES.get('collegeCode')

    if not  (token is None or token==""):
            print("redirecting"+token)
            return HttpResponseRedirect('dashboard/'+collegeCode+"/"+userid)
      

    ids = list(College.objects.values('collegeCode','collegeName'))
    
    response = render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
    response.delete_cookie("userid")
    response.delete_cookie("token")
    response.delete_cookie("collegeCode")
    return response 

def logout(request):
    response=HttpResponseRedirect("/")
    response.delete_cookie("userid")
    response.delete_cookie("token")
    response.delete_cookie("collegeCode")
    #response.delete_cookie("csrftoken")
    return response

def excelDataValidation(option, excel):
    opt = int(option)
    if opt == 2:
        check_cources(excel, Course)
    if opt == 1:
        check_students(excel, Students)

def excelReader(request):
    ex = request.POST['excel_type']
    print(ex)
    excel_file = request.FILES["excel_file"]
    print(excel_file)
    wb = pandas.read_excel(excel_file, sheet_name=0)
    wb = wb.dropna(how='all')
    #wb = wb.rename(columns=wb.iloc[0]).drop(wb.index[0])
    # getting a particular sheet by name out of many sheets
    #polls_tables = apps.get_app_config("cuserauth")
    #print(wb.dtypes)
    #print(polls_tables.models.keys())

    excelDataValidation(ex, wb)
    #if(wb['sl no'].dtype == pandas.Int64Index):
    #    print(wb['sl no'])
    # iterating over the rows and
    # getting value from each cell in row
    #for row in worksheet.iter_rows():
    #    row_data = list()
    #    for cell in row:
    #        row_data.append(str(cell.value))
    #    excel_data.append(row_data)
    
    return HttpResponseRedirect('/')

@csrf_protect
def _dashboard(request, collegeCode, userid):
    try:
        collegeName = College.objects.get(collegeCode = collegeCode)
        lecName = Lecturers.objects.get(id = userid)
    except ObjectDoesNotExist:
        return HttpResponse("Please Contact principal \n lecturer not registered", status= 404)
    print(type(lecName.LecturerName))
    print("dashboard")
    from django.core import serializers
    #c= Students._meta.get_field_by_name()
    #print([f.name for f in Students._meta.get_fields(include_hidden=False)])
    student = [f.name for f in StudentInfo._meta.local_fields]
    #print(i.name for i in student)
    #print(Students._meta.local_fields)
    #object_list = serializers.serialize("python", )
    #for object in object_list:
    #    for field_name, field_value in object['fields'].items():
    #        print (field_name, field_value)
    #sec = list(Incharge.objects.filter(lecturerFK__collegeFK = collegeCode,lecturerFK_id = userid).annotate(lecName = F('lecturerFK__LecturerName'),subCode = F('subjectFK__subjectName'), subName = F('subjectFK_id'),subYear = F('subjectFK__subjectYear'),secName = F('sectionFK__sectionName'), year = F('sectionFK__year')).values('lecName','subCode','subName','subYear','secName', 'year'))
    #print(sec)
    #lName = F('lecturerFK__LecturerName'), secName = F('sectionFK__sectionName'), year = F('sectionFK__year'),
    #subs = Incharge.objects.filter(lecturerFK = lecName).annotate(subCode = F('subjectFK__subjectCode'),subName = F('subjectFK__subjectName')).values('subCode' ,'subName').distinct()
    #for sub in sec:
    #    #sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
    #    print("Subjects Taken",sub)
        
    var = {"college_name":collegeName.collegeName,"lecName":lecName.LecturerName}
    return render(request,"dash.html", var)

@csrf_exempt
def login(request):
    @ensure_csrf_cookie
    @csrf_protect
    def authenticate(request):
        body_unicode = request.body.decode('utf-8') 
        body = json.loads(body_unicode)
        collegeCode=body["college"]
        user=body["username"]
        password=body["password"]
        print(collegeCode, user, password)
        print("in")
        #check for college
        return JsonResponse(authenticate_user(collegeCode,user,password)) 

    @ensure_csrf_cookie
    def loadPage(request):           
        print("load")
        return render(request,'index.html')
    if request.method == 'POST':
        return authenticate(request)
    else:
        return loadPage(request)

# Temperory code
#@ensure_csrf_cookie
@csrf_exempt
def change_password(request):
    @ensure_csrf_cookie
    @csrf_protect
    def postReq(request):
        print("got post request")
        username=request.POST['username']
        password=request.POST['password']
        
        # replace by argon or sha etc ..
        hash_password,salt=authentication_utils.make_password(password)
        obj=Lecturers.objects.filter(LecturerUsername=username)
            
        if len(obj) > 0:
            logger.info("updaing password "+str(hash_password))
            obj.update(LecturerPassword=str(hash_password),salt=salt,LastPasswordChange=timezone.now())
            return render_to_response("temp.html",{"message":"update successfull"})
        return render_to_response("temp.html",{"message":"no user by this user name : "+username},RequestContext(request))

    def getReq(request):
        return render(request,'temp.html')

    if request.method=='POST':
        return postReq(request)
    else:
         return getReq(request)

