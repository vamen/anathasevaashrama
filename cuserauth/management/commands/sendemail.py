from django.core.management.base import BaseCommand, CommandError
from django.db.models.query import QuerySet
from cuserauth.models import Attendence,Subjects
import datetime 
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user ="spicknspan.dev@gmail.com"
gmail_password="1ks13cs122"
subject="Absent for classes"

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument("-d","--date",dest="date",help="date from which message should be sent")
        
    def intialise_smtp(self):
        try:
            self.server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(gmail_user, gmail_password)
            
            
        except Exception as e:
            print("something went wrong "+str(e))
        
    def init_message(self):
        self.msg=MIMEMultipart()
        self.msg["From"]=gmail_user
        self.msg["subject"]=subject
        

    def handle(self, *args, **options):
        self.intialise_smtp()
        
        # TODO: Querying same database thrice for same data for each user whihc is unnecessary
        if options.get("data",None) is None:
           absent_list=Attendence.objects.filter(messageSentStatus=Attendence.MessageStatus.NOTSENT.value)
           students=absent_list.distinct("studentFK")          
           for entry in students:
                self.init_message()
                email_text=entry.studentFK.studentInfoFK.studentName+" was absent for following classes :\n"   
                to=entry.studentFK.studentInfoFK.fatherEmail
                self.msg["to"]=to
                print(to)
                studentFK=entry.studentFK
                absent_classes_dates=absent_list.filter(studentFK=studentFK).values("sessionDate").distinct("sessionDate") 
                for date in absent_classes_dates:
                    date=date["sessionDate"].strftime("%Y-%m-%d")
                    email_text=email_text+" on date : "+str(date)+"\n"
                    absent_subjects=absent_list.filter(studentFK=studentFK,sessionDate=date,messageSentStatus=Attendence.MessageStatus.NOTSENT.value)
                    for absent_subject in absent_subjects:
                        email_text=email_text+absent_subject.subjectFK.subjectName+" from "+str(absent_subject.sessionFrom)+" to "+str(absent_subject.sessionTo)+"\n"
                print(email_text)
                self.msg.attach(MIMEText(email_text))
                self.server.sendmail(gmail_user,to,self.msg.as_string()) 
                print("email sent for ",entry.studentFK.studentInfoFK.studentName)
                time.sleep(0.5)  
           self.server.quit()       
    
                


        #    server.close() 