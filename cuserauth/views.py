from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Incharge,college 

def index(request):
    college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    return render_to_response("index.html",{"college_name":"Login To Portel","colleges":college},RequestContext(request))
    
@csrf_exempt
def login(request):
    

    college_name=request.POST.get('college', False)

    user=request.POST["username"]
    password=request.POST["password"]
    print(college,user,password)
    
    college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    data={"college_name":user,"colleges":college}
    return render_to_response("index.html",data,RequestContext(request))

