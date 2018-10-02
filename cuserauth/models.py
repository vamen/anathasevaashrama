from django.db import models

# Create your models here.

class college(models.Model):
    name = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    college_id = models.CharField(max_length=200,unique=True,default="None") 
    ld_phone  = models.CharField(max_length=20,default="None")
    sub_start = models.DateTimeField(blank=True)
    sub_end = models.DateTimeField(blank=True)
    
    def  __str__(self):
        return self.name

class course(models.Model):
    # name and domain unique
    name = models.CharField(max_length=200)
    cource_id = models.CharField(max_length=200,default="None")
    domain = models.CharField(max_length=200)
    year = models.IntegerField(default="None")
    def  __str__(self):
        return self.name


class offerd_course(models.Model):

    course = models.ForeignKey(course,on_delete=models.CASCADE)
    college = models.ForeignKey(college,on_delete=models.CASCADE)  
    start = models.DateTimeField(blank = True,default="None")
    end = models.DateTimeField(blank = True,default="None")


class subjects(models.Model):
    # multiple row entry if subjects comes in multiple year  
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)
    year = models.IntegerField(default=0)

    def  __str__(self):
        return self.subject_name

class students(models.Model):
    sname = models.CharField(max_length=200)
    parent = models.CharField(max_length=200)
    phones = models.CharField(max_length=200) 
    course = models.ForeignKey(course,on_delete=models.PROTECT)
    college = models.ForeignKey(college,on_delete=models.PROTECT)  
    roll_no=models.CharField(max_length=200,unique=True,default="None")
    year=models.IntegerField()    
    
    def  __str__(self):
        return self.sname

class attendence(models.Model):
    subject_session=models.ForeignKey(subjects,on_delete=models.PROTECT)
    student=models.ForeignKey(students,on_delete=models.CASCADE)
    cfrom=models.TimeField()
    cto=models.TimeField()
    date=models.DateField()
    status=models.IntegerField(default="None")

    def  __str__(self):
        return self.student.sname



class Incharge(models.Model):
    college = models.ForeignKey(college,on_delete=models.PROTECT)
    subject = models.ForeignKey(subjects,on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    user_name= models.CharField(max_length=200,unique=True,default="None")
    password = models.CharField(max_length=200,default="password")

    def  __str__(self):
        return self.name
