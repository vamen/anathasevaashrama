from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge, Students, Offerd_course, Section
from django.db.models import F
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from .authentication import *
from django.http import HttpResponseRedirect
import openpyxl

logger=init_logger()
def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(College.objects.values('collegeCode','collegeName'))
    
    response = render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
    response.set_cookie("userid",None)
    response.set_cookie("token",None)
    
    return response 
@csrf_exempt
def excelReader(request):
    excel_file = request.FILES["excel_file"]
    print(excel_file)
    wb = openpyxl.load_workbook(excel_file, data_only=True)

    # getting a particular sheet by name out of many sheets
    worksheet = wb["Sheet1"]
    print(worksheet)
    excel_data = list()
    # iterating over the rows and
    # getting value from each cell in row
    for row in worksheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    print(excel_data)
    return HttpResponseRedirect('/')




@check_login("page")
def _dashboard(request, collegeCode, userid):
    subs = Incharge.objects.filter(lecturerFK = userid).annotate(lName = F('lecturerFK__LecturerName'), secName = F('sectionFK__sectionName'), year = F('sectionFK__year'), subName = F('subjectFK__subjectName')).values('lName','secName','year' ,'subName')
    for sub in subs:
        #sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
        print("Subjects Taken",sub)
    collegeName = College.objects.get(collegeCode = collegeCode)
    lecName = Lecturers.objects.get(id = userid)
    print(type(lecName.LecturerName))
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
        
        response_dict={}
        #check for college
        JsonResponse(authenticate_user(collegeCode,user,password)) 
               
    else:
        ids = list(College.objects.values('collegeCode','collegeName'))
        
        response = render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
        response.set_cookie("userid",None)
        response.set_cookie("token",None)
        
        return response 



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

