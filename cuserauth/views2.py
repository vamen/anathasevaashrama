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
def _sectionHandler(request, id):
    #if request.method == 'POST':
    print('Section')
    #body_unicode = request.body.decode('utf-8')
    #body = json.loads(body_unicode)
    #in_id = body["id"]
    #collegeCode=body["collegeCode"]
    #lectureId = body["userID"]
    #subCode = body['subCode']
    sec = Incharge.objects.get(id = id)
    studentList = list(Students.objects.filter(sectionFK = sec.sectionFK).values('studentInfoFK_id', 'studentInfoFK__studentName'))

    print(sec)
    print(studentList)
    return JsonResponse(json.dumps(studentList),safe=False)

def _attendenceButtonClick(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        collegeCode=body["collegeCode"]
        lecture = body["userID"]

        subjectHandled = list(Incharge.objects.filter(lecturerFK__collegeFK = collegeCode,lecturerFK_id = userid).annotate(subCode = F('subjectFK__subjectCode'),subName = F('subjectFK__subjectName')).values('subCode', 'subName').distinct())
        print(subjectHandled)
        listOfSubs = []
        for subjectInfo in subjectHandled:
            print(subjectInfo['subCode'])
            listingSubs = list(Incharge.objects.filter(lecturerFK__collegeFK = collegeCode,lecturerFK_id = userid, subjectFK_id = subjectInfo['subCode']).annotate(subYear = F('subjectFK__subjectYear'),secName = F('sectionFK__sectionName'), year = F('sectionFK__year')).values('id','subYear','secName', 'year'))
            print(listingSubs)
            dataAdd = {'subCode':subjectInfo['subCode'], 'subName':subjectInfo['subName'],'sections':listingSubs}
            listOfSubs.append(dataAdd)
            #lister.update
        print(listOfSubs)
        return JsonResponse({'subjectsHandled':listOfSubs})

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

