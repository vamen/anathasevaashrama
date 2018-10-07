from django.shortcuts import render,render_to_response
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Lecturers,College,Subjects,Incharge
from django.db.models import F
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from django.http import HttpResponseRedirect


logger=init_logger()
def index(request):
    #college=["Anantha sevashram ,Malladihalli",'juniour college,chanagiri']
    
    ids = list(College.objects.values('collegeCode','collegeName'))
    
    response = render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))
    response.set_cookie("userid",None)
    response.set_cookie("token",None)
    
    return response 



def check_login(returntype):
    def outter_wrap(function):
        def wrap(request,*args,**kwargs):
            userid=request.COOKIES.get('userid') 
            token=request.COOKIES.get('token')
            entry=Lecturers.objects.get(pk=int(userid))
            print(token,userid)
            if not token is None:
                if token==entry.token:
                    return function(request,*args,**kwargs)
            if returntype == "json":
                response_dict={}
                response_dict["status"]=1
                response_dict["message"]="user logged out"
                JsonResponse(response_dict)
            else:    

                return HttpResponseRedirect('/')
        return wrap        
    return outter_wrap


@check_login("page")
def _dashboard(request, collegeCode, userid):

    subs = list(Incharge.objects.filter(lecturerFK = userid).annotate(lName = F('lecturerFK__LecturerName'), secName = F('sectionFK__sectionName'), year = F('sectionFK__year'), subName = F('subjectFK__subjectName')).values('lName','secName','year' ,'subName'))
    for sub in subs:
        #sub_names = list(Subjects.objects.filter(id = sub).values_list('subject_name', flat = True))
        print("Subjects Taken",sub)
    collegeName = list(College.objects.filter(collegeCode = collegeCode).values_list('collegeName',flat = True))[0]
    lecName = Lecturers.objects.get(id = userid)
    print(lecName)
    var = {"college_name":collegeName, "subjectsHandled":subs,"lecName":lecName}
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
        message=""
        #check for college
        try:
            row=Lecturers.objects.get(collegeFK_id = collegeCode, LecturerUsername=user)
        
            if authentication_utils.check_password(row.LecturerPassword,row.salt,password):
                token=authentication_utils.generate_token(row.LecturerUsername,row.salt)
                
                message='Success'
                response_dict["status"] = 0
                response_dict["userid"]=row.id
                response_dict["token"]=token
                response_dict["collegeCode"]=collegeCode
                row.token=token
                row.save()
                return JsonResponse(response_dict)
            else:
                message='wrong password'
                response_dict["status"]=1
                  
        except ObjectDoesNotExist:
                
                response_dict["status"]=1
                message='user does not exist in database'
        
        
        logger.info(message)            
        response_dict["message"] =message 
        return JsonResponse(response_dict)        
    else:
            ids = list(College.objects.values('collegeCode','collegeName'))
            return render_to_response("index.html",{"college_name":"Login To Portel","ids":ids},RequestContext(request))


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

