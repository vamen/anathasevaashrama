from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('dashboard/<int:collegeCode>/<int:userid>/', views._dashboard, name= 'dashboard'),
    path('populator/<int:college>/<int:userid>/<str:sec>/<int:sub>/', views._populator, name= 'populator')
]