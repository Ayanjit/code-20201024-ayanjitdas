from django.urls import include, path
from django.conf.urls import url 
from rest_framework import routers
from . import views

urlpatterns = [
    url('bmicalculator', views.CalculateBMI),
]