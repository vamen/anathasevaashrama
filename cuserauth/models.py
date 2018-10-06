from django.db import models

# Create your models here.
'''
format to be used in medel
    #Priority top to bottom
        primary Key
        Forign Key
        fileds
        classes
'''

class College(models.Model):
    #primary key
    collegeCode  = models.CharField(max_length=20, primary_key=True, verbose_name = 'College Code')
    #Fields
    collegeName = models.CharField(max_length=20, blank=True, null = False, verbose_name = 'Name')
    collegeAdress = models.CharField(max_length=200, blank=True, null = False, verbose_name = 'Address')
    collegeLandLineNumber  = models.CharField(max_length=20, blank=True, null = False, verbose_name = 'Land Line Number')
    collegeSubStart = models.DateTimeField(blank=True, verbose_name = 'Subscription Start Date')
    collegeSubEnd = models.DateTimeField(blank=True, verbose_name = 'Subscription End Date')
    
    #classes
    def  __str__(self):
        return self.collegeName

class Course(models.Model):
    #Fields
    courceName = models.CharField(max_length=200,blank=True, null = False, verbose_name = 'Name')
    courceDomain = models.CharField(max_length=20, blank=True, verbose_name = 'Domain')   
    #classes
    class Meta:
        unique_together = ('courceName','courceDomain')
    def  __str__(self):
        return self.courceName
        # name and domain unique    

class Section(models.Model):
    #Forign Key
    collegeFK = models.ForeignKey(College,on_delete=models.PROTECT)
    courseFK = models.ForeignKey(Course,on_delete=models.CASCADE)
    #Fields
    sectionName = models.CharField(max_length = 5)
    year = models.IntegerField(default=0)

    #classes
        #why? if i make nly secName and year i cant create new secs for different colleges
    class Meta:
        unique_together = ('collegeFK','courseFK','sectionName', 'year',)

    def  __str__(self):
        return self.sectionName+str(self.year)

class Offerd_course(models.Model):
    #Forign Key
    collegeFK = models.ForeignKey(College,on_delete=models.PROTECT)
    courseFK = models.ForeignKey(Course,on_delete=models.CASCADE)  
    
    #Fields
    year = models.IntegerField(default=0)
    start = models.DateTimeField(blank = True)
    end = models.DateTimeField(blank = True)
    #classses
    class Meta:
        unique_together = ('collegeFK','courseFK',)
    def  __str__(self):
        return self.courseFK.courceName

class Subjects(models.Model):
    #PrimaryKey
    subjectCode = models.CharField(max_length=20, primary_key=True)
    #ForignKey
        # multiple row entry if subjects comes in multiple year  
    courseFK = models.ForeignKey(Course,on_delete=models.CASCADE)

    subjectName = models.CharField(max_length=20)
    subjectYear = models.IntegerField(null=False)
    #classes
    class Meta:
        unique_together = ('courseFK','subjectCode',)
    def  __str__(self):
        return self.subjectName

class Students(models.Model):
    #PrimaryKey
    StudentRollNo=models.CharField(max_length=200,primary_key=True)
    #Forign Key
    sectionFK = models.ForeignKey(Section,on_delete=models.PROTECT)
    courseFK = models.ForeignKey(Offerd_course,on_delete=models.PROTECT)
    collegeFK = models.ForeignKey(College,on_delete=models.PROTECT)  

    #fields
    studentName = models.CharField(max_length=20,null = False)
    studentParent = models.CharField(max_length=20,null = False)
    studentPhone = models.CharField(max_length=10,null = False) 
    year=models.IntegerField(null = False)    
    #classes
    def  __str__(self):
        return self.studentName

class Attendence(models.Model):
    #Forign Key
    subjectFK = models.ForeignKey(Subjects,on_delete=models.PROTECT)
    studentFK = models.ForeignKey(Students,on_delete=models.CASCADE)
    #fields
    sessionfrom=models.TimeField()
    sessionto=models.TimeField()

    sessionDate=models.DateField()
    studentstatus=models.IntegerField()
    #classes
    def  __str__(self):
        return self.studentFK.studentName

class Lecturers(models.Model):

    #Forign Key
    collegeFK = models.ForeignKey(College,on_delete=models.PROTECT)
    #Fields
    LecturerName = models.CharField(max_length=200,default="None")
    LecturerUsername= models.CharField(max_length=200,unique=True,default="None")
    LecturerPassword = models.CharField(max_length=200,default="pass")
    #classes
    def  __str__(self):
        return self.LecturerName

class Incharge(models.Model):
    #Forign Key
    lecturerFK = models.ForeignKey(Lecturers,on_delete=models.PROTECT)
    sectionFK = models.ForeignKey(Section,on_delete=models.PROTECT)
    subjectFK = models.ForeignKey(Subjects,on_delete=models.PROTECT) 
    class Meta:
        unique_together = ('lecturerFK','sectionFK', 'subjectFK')

    def  __str__(self):
        return self.lecturerFK.LecturerName
