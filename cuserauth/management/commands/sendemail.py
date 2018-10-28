from django.core.management.base import BaseCommand, CommandError
from cuserauth.models import Attendence
import datetime 

class Command(BaseCommand):

    def handle(self, *args, **options):
        print(datetime.date.today())         
        pass