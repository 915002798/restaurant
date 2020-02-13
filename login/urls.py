# _*_ coding=UTF-8 _*_
# 作者：Ariel
# 创建时间：2019-12-17 10:04
from django.urls import path
from login import views

app_name = 'login'

urlpatterns = [
    path('', views.login, name='login'),
]
