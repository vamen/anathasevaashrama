from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Incharge,college 
from django.http import JsonResponse
import json

def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(college.objects.values('college_id','name'))

    return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
def _dashboard(request, userid):

    userId = list(Incharge.objects.filter(id = userid).values_list('subject', flat = True))
    print(userID)
    var = {"college_name":asd}
    return render_to_response("dash.html", var, RequestContext(request))
@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    #content = body['content']
    #form = request.POST
    coll_id=body["college"]
    user=body["username"]
    password=body["password"]
    print(coll_id, user, password)
    #checks college name in database

    ##############################
    coll_name = list(college.objects.filter(college_id=coll_id).values_list('name', flat = True))
    if len(coll_name) > 0 :
        #do something
        pass
    #
    userId = list(Incharge.objects.filter(user_name=user, password=password).values_list('id', flat = True))

    #print(type(ename[0]))
    print(ename)
    status = 1
    message = 'Username or Password Invalid'
    #authenticated
    if len(ename) > 0:
        status = 0
        message = 'Success'
    print(status, message)
    return JsonResponse({'status':status,'message':message, 'userid':userId})
'''    
#college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    data={"college_name":user,"colleges":college}
    return render_to_response("index.html",data,RequestContext(request))'''

