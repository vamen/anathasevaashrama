from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('dashboard/<str:collegeCode>/<int:userid>/', views._dashboard, name= 'dashboard'),
    path('populator/<str:college>/<int:userid>/<str:sec>/<int:sub>/', views._populator, name= 'populator'),
    path('exelFileReader',views.excelReader, name= 'excelReader'),
    path('passwordChange',views.change_password,name='change Password'),

]