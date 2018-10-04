from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('dashboard/<int:userid>', views._dashboard, name= 'dashboard')
]