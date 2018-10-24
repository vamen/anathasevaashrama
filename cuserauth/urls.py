from django.urls import path

from . import views
from . import views2
urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('dashboard/<str:collegeCode>/<int:userid>/', views._dashboard, name= 'dashboard'),
    #path('studentUnderSub', views2._studentUnderSub, name= 'populator'),
    path('exelFileReader',views.excelReader, name= 'excelReader'),
    path('passwordChange',views.change_password,name='change Password'),
    path('excel_upload', views2.excel_upload, name = 'Excel'),
    path('subject_handeled_info', views2.subject_handeled_info, name = 'Attandence'),
    path('sectionHandler/<int:id>/', views2._sectionHandler, name = 'sections'),
    path('openAttendance', views2._openAttendance, name = 'openAttendance'),
    path('mark_attendance', views2._markingAttendance, name = 'markAttendance')
    #path('sectionHandler/<int:id>/', views2._sectionHandler, name = 'sections')
]