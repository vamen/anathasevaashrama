from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('passwordChange',views.change_password,name='change Password'),
    path('dashboard/<str:collegeCode>/<int:userid>/', views._dashboard, name= 'dashboard')
]