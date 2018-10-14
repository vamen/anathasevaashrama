from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from .models import Lecturers,College,Subjects,Incharge, Students, Offerd_course, Section, Course
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F


db_tables = [{"id":1,"tables":'Students'},{"id": 2,"tables":'Course'},{"id": 3,"tables":'Subjects'},{"id": 4,"tables":'Teacher assignment'},{"id": 5,"tables": 'Attendence'},{"id": 6,"tables": 'Lecturers'}]

def excel_upload(request):
    return render_to_response("excel.html", {"tables":db_tables},RequestContext(request))

@csrf_exempt

def _sectionHandler(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 
        body = json.loads(body_unicode)
        collegeCode=body["collegeCode"]
        lectureId = body["userID"]
        subCode = body['subCode']
        sec = list(Incharge.objects.filter(lecturerFK_id = lectureId,subjectFK__subjectCode = subCode).annotate(secName = F('sectionFK__sectionName'), year = F('sectionFK__year')).values('secName', 'year'))
       
        return JsonResponse(json.dumps(sec),safe=False)

def _studentUnderSub(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    collegeCode=body["collegeCode"]
    subject = body["subID"]
    lecture = body["userID"]
    section = body["sec"]
    year = body["year"]

    subjectObj = Subjects.objects.get(subjectCode = subject)
    print('subjectObj',subjectObj)

    courseObj = Offerd_course.objects.get(courseFK = subjectObj.courseFK_id)
    print('courseObj',courseObj)

    sectionObj = Section.objects.get(sectionName = sec, year = year)
    print('sectionObj',sectionObj)

    students = list(Students.objects.filter(collegeFK_id = collegeCode, sectionFK = sectionObj, courseFK = courseObj).values('StudentRollNo','studentName'))
    #students = list(Students.objects.filter(collegeFK_id = collegeCode,courseFK_id = subjectObj.courseFK).all())
    print(students)
    return JsonResponse({'students':students})
def _studentUnderSub(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8') 
        body = json.loads(body_unicode)
        collegeCode=body["collegeCode"]
        lectureId = body["userID"]
        subID = body['subID']

