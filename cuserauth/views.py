from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Incharge,College,Subjects
from django.http import JsonResponse
import json

def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(College.objects.values('college_id','name'))
    return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))

def _dashboard(request, userid):

    subs = list(Incharge.objects.filter(id = userid).values_list('subject_id', flat = True))
    print("SUBSSSS",subs)
    for sub in subs:
        sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
    
        print("SUBSSSS",sub_names)
    var = {"college_name":subs}
    return render_to_response("dash.html", var, RequestContext(request))

@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    coll_id=body["college"]
    user=body["username"]
    password=body["password"]
    print(coll_id, user, password)
    #check for college
    coll = list(College.objects.filter(college_id=coll_id).values_list('id', flat = True))
    #check for user
    eid = list(Incharge.objects.filter(user_name=user, password=password).values_list('college_id', flat = True))

    status = 1
    message = 'Username or Password Invalid'
    #authenticate
    if eid==coll:
        status = 0
        message = 'Success'
    print(status, message)
    return JsonResponse({'status':status,'message':message, 'userid':eid})


