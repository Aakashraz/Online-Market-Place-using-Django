from django.urls import path

from . import views     #import of views from current directory i.e. dashboard

app_name= 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]

