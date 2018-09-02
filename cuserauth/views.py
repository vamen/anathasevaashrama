from django.shortcuts import render
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request,"index.html",context={})
    


