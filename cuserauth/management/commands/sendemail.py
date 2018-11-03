from django.core.management.base import BaseCommand, CommandError
from cuserauth.models import Attendence
import datetime 
from cuserauth.models import Attendence


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-d","--date",dest="date",help="date from which message should be sent")
        
   
    def handle(self, *args, **options):
        if options.get("data",None) is None:
           objects=Attendence.objects.filter(messageSentStatus=Attendence.MessageStatus.NOTSENT.value)          
           for rows in objects:
               print(rows.studentFK.studentInfoFK.fatherEmail)
    