from django.db import models

# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    college_id  = models.CharField(max_length=200,unique=True,default="None") 
    ld_phone  = models.CharField(max_length=20,default="None")
    sub_start = models.DateTimeField(blank=True)
    sub_end = models.DateTimeField(blank=True)
    
    def  __str__(self):
        return self.name

class Course(models.Model):
    # name and domain unique
    name = models.CharField(max_length=200)
    cource_id = models.CharField(max_length=200,default="None")
    domain = models.CharField(max_length=200)
    year = models.IntegerField(default="None")
    def  __str__(self):
        return self.name

class Section(models.Model):
    #
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    section_name = models.CharField(max_length = 5)
    year = models.IntegerField(default="None")

class Offerd_course(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    college = models.ForeignKey(College,on_delete=models.CASCADE)  
    start = models.DateTimeField(blank = True)
    end = models.DateTimeField(blank = True)


class Subjects(models.Model):
    # multiple row entry if subjects comes in multiple year  
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)
    year = models.IntegerField(default=0)

    def  __str__(self):
        return self.subject_name

class Students(models.Model):
    section = models.ForeignKey(Section,on_delete=models.PROTECT)
    sname = models.CharField(max_length=200)
    parent = models.CharField(max_length=200)
    
    phones = models.CharField(max_length=200) 
    course = models.ForeignKey(course,on_delete=models.PROTECT)
    college = models.ForeignKey(college,on_delete=models.PROTECT)  
    roll_no=models.CharField(max_length=200,unique=True,default="None")
    year=models.IntegerField()    
    
    def  __str__(self):
        return self.sname

class Attendence(models.Model):
    subject_session=models.ForeignKey(Subjects,on_delete=models.PROTECT)
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    cfrom=models.TimeField()
    cto=models.TimeField()
    date=models.DateField()
    status=models.IntegerField(default="None")

    def  __str__(self):
        return self.student.sname

class Incharge(models.Model):
    college = models.ForeignKey(College,on_delete=models.PROTECT)
    subject = models.ForeignKey(Subjects,on_delete=models.PROTECT)
    section = models.ForeignKey(Section,on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    user_name= models.CharField(max_length=200,unique=True,default="None")
    password = models.CharField(max_length=200,default="password")
    
    def  __str__(self):
        return self.name
