from django.contrib import admin

# Register your models here.

from cuserauth.models import *

admin.site.register(college)
admin.site.register(Incharge)
admin.site.register(course)
admin.site.register(offerd_course)
admin.site.register(subjects)
admin.site.register(students)
admin.site.register(attendence)