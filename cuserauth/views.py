from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Incharge,college 

def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(college.objects.values('college_id','name'))

    return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
    
@csrf_exempt
def login(request):
    #form = request.POST
    coll_id=request.POST["colLister"]
    user=request.POST["username"]
    password=request.POST["password"]
    
    #checks college name in database
    coll_name = list(college.objects.filter(college_id=coll_id).values_list('name', flat = True))
    if len(coll_name) > 0 :
        #do something
        pass

    ename = list(Incharge.objects.filter(user_name=user, password=password).values_list('name', flat = True))

    #print(type(ename[0]))
    print(ename[0])
    if len(ename) > 0:
        #authincated
        pass
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    data={"college_name":user,"colleges":college}
    return render_to_response("index.html",data,RequestContext(request))

