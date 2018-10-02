from django.db import models

# Create your models here.

class college(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    sub_start = models.DateTimeField(blank=True)
    sub_end = models.DateTimeField(blank=True)

class course(models.Model):
    name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)

class offerd_course(models.Model):
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    college = models.ForeignKey(college,on_delete=models.CASCADE)  
    year = models.IntegerField()

class subjects(models.Model):
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    sname = models.CharField(max_length=200)
    year = models.IntegerField()

class students(models.Model):
    sname = models.CharField(max_length=200)
    parent = models.CharField(max_length=200)
    phones = models.CharField(max_length=200) 
    course = models.ForeignKey(course,on_delete=models.PROTECT)
    college = models.ForeignKey(college,on_delete=models.PROTECT)  

class attendence(models.Model):
    subject=models.ForeignKey(subjects,on_delete=models.PROTECT)
    student=models.ForeignKey(students,on_delete=models.CASCADE)
    cfrom=models.TimeField()
    cto=models.TimeField()
    date=models.DateField()
    status=models.IntegerField()


class Incharge(models.Model):
    college = models.ForeignKey(college,on_delete=models.PROTECT)
    subject = models.ForeignKey(subjects,on_delete=models.PROTECT)
    name = models.CharField(max_length=200) 
    password=models.CharField(max_length=200)