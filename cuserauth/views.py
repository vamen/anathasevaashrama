from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge
from django.http import JsonResponse
import json

def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(College.objects.values('collegeCode','collegeName'))
    print(ids)
    return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))

def _dashboard(request, collegeCode, userid):

    subs = list(Incharge.objects.filter(lecturerFK = userid).values('lecturerFK__LecturerName','sectionFK__sectionName','sectionFK__year' ,'subjectFK__subjectName'))
    for sub in subs:
        #sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
        print("Subjects Taken",sub)
    collegeName = list(College.objects.filter(collegeCode = collegeCode).values_list('collegeName',flat = True))[0]
    var = {"college_name":collegeName}
    return render_to_response("dash.html", var, RequestContext(request))

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

    print("EID",eid)
    status = 1
    message = 'Username or Password Invalid'
    #authenticate
    if len(eid) == 1:
        status = 0
        message = 'Success'
    print(status, message)
    return JsonResponse({'status':status,'message':message, 'userid':eid, 'collegeCode':collegeCode})


