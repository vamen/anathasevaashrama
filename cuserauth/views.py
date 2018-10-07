from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge, Students, Offerd_course, Section
from django.db.models import F
from django.http import JsonResponse
import json

def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = College.objects.values('collegeCode','collegeName')
    print(ids)
    return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))

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

def _populator(request, college, userid, sec, sub):
    #body_unicode = request.body.decode('utf-8')
    #body = json.loads(body_unicode)
    collegeCode=college
    subject=sub
    lecture=userid
    section=sec
    print(sec)
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
@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    collegeCode=body["college"]
    user=body["username"]
    password=body["password"]
    print(collegeCode, user, password)
    #check for college
    eid = list(Lecturers.objects.filter(collegeFK_id = collegeCode, LecturerUsername=user, LecturerPassword=password).values_list('id', flat = True))
    
    #eid = Lecturers.objects.get(collegeFK_id = collegeCode, LecturerUsername=user, LecturerPassword=password)
    if not eid:
        status = 1
        message = 'Username or Password Invalid'
    else:
        status = 0
        message = 'Success'

    #authenticate
    print("EID",eid)
    print(status, message)
    return JsonResponse({'status':status,'message':message, 'userid':eid, 'collegeCode':collegeCode})


