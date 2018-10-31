from django.contrib import admin

# Register your models here.

from cuserauth.models import *
admin.site.register(StudentInfo)
admin.site.register(College)
admin.site.register(Incharge)
admin.site.register(Course)
admin.site.register(Offerd_course)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendence)
admin.site.register(Section)
admin.site.register(Lecturers)
admin.site.register(collage_meta)