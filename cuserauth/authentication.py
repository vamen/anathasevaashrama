from .utils import authentication_utils 
from .utils.logger_utils import init_logger
from .models import Lecturers
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

logger=init_logger()

def check_login(returntype):
    def outter_wrap(function):
        def wrap(request,*args,**kwargs):
            userid=request.COOKIES.get('userid') 
            token=request.COOKIES.get('token')
            
            if (token == "None") and (userid == "None"):
                logger.info("token is None")
                return HttpResponseRedirect('/')

            entry=Lecturers.objects.get(id=int(userid))
            logger.info("LOGIN",token)
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


def authenticate_user(collegeCode,user,password):
    response_dict={}
    message=""    
    logger.info(collegeCode+" "+user+" "+password)
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
                
            else:
                message='wrong password'
                response_dict["status"]=1
                  
    except ObjectDoesNotExist:
                
                response_dict["status"]=1
                message='user does not exist in database'
        
        
    logger.info(message)            
    response_dict["message"] =message 
    return response_dict