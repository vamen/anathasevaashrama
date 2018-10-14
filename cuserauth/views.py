from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge, Students, Offerd_course, Section, Course
from django.db.models import F
from django.http import JsonResponse
import json
from django.utils import timezone
from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from .authentication import *
from django.http import HttpResponseRedirect
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
    return response
def excelDataValidation(option, excel):
    opt = int(option)
    if opt == 2:
        check_cources(excel, Course)
    if opt == 1:
        check_students(excel, Students)

@csrf_exempt
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
def _sectionHandler(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 
        body = json.loads(body_unicode)
        collegeCode=body["collegeCode"]
        lectureId = body["userID"]
        subID = body['subID']
        sec = Incharge.objects.filter(lecturerFK_id = lectureId,subjectFK__subjectCode = subID).annotate(secName = F('sectionFK__sectionName'), year = F('sectionFK__year')).values('secName', 'year')
        print(sec)
        return JsonResponse(sec) 
@check_login("page")
def _dashboard(request, collegeCode, userid):
    collegeName = College.objects.get(collegeCode = collegeCode)
    lecName = Lecturers.objects.get(id = userid)
    print(type(lecName.LecturerName))
    #lName = F('lecturerFK__LecturerName'), secName = F('sectionFK__sectionName'), year = F('sectionFK__year'),
    subs = Incharge.objects.filter(lecturerFK = lecName).annotate(subCode = F('subjectFK__subjectCode'),subName = F('subjectFK__subjectName')).values('subCode' ,'subName').distinct()
    for sub in subs:
        #sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
        print("Subjects Taken",sub)
        
    var = {"college_name":collegeName.collegeName, "subjectsHandled":subs,"lecName":lecName.LecturerName}
    return render_to_response("dash.html", var, RequestContext(request))


@csrf_exempt
def login(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 
        body = json.loads(body_unicode)
        collegeCode=body["college"]
        user=body["username"]
        password=body["password"]
        print(collegeCode, user, password)
        
        #check for college
        return JsonResponse(authenticate_user(collegeCode,user,password)) 
               
    else:
        HttpResponseRedirect("/")


def _populator(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    collegeCode=body["college"]
    subject=body["subject"]
    lecture=body["lecture"]
    section=body["section"]
    subjectObj = Subjects.objects.get(subjectCode = subject)
    print('subjectObj',subjectObj)
    courseObj = Offerd_course.objects.get(courseFK = subjectObj.courseFK_id)
    print('courseObj',courseObj)
    sectionObj = Section.objects.get(sectionName = sec, year = 1)
    print('sectionObj',sectionObj)
    students = list(Students.objects.filter(collegeFK_id = collegeCode, sectionFK = sectionObj, courseFK = courseObj).values('StudentRollNo','studentName'))
    #students = list(Students.objects.filter(collegeFK_id = collegeCode,courseFK_id = subjectObj.courseFK).all())
    print(students)
    return JsonResponse({'students':students})


# Temperory code
@csrf_exempt
def change_password(request):
    if request.method=='GET':
        return render_to_response('temp.html',{"message":""})
    else:
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

