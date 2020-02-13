# _*_ coding=UTF-8 _*_
# 作者：Ariel
# 创建时间：2020-01-08 9:56 
from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('distribution/', views.distribution, name='distribution'),
    path('prepare/', views.prepare, name='prepare'),
    path('finish/', views.finish, name='finish'),
]
