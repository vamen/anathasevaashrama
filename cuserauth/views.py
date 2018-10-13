from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge, Students
from django.db.models import F
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from .authentication import *
from django.http import HttpResponseRedirect


logger=init_logger()
def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(College.objects.values('collegeCode','collegeName'))
    
    response = render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
    response.set_cookie("userid",None)
    response.set_cookie("token",None)
    
    return response 





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
    students = Students.objects.filter(courseFK = subjectObj.courseFK,collegeFK_id = collegeCode, sectionFK = section)

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

