# _*_ coding=UTF-8 _*_
# 作者：Ariel
# 创建时间：2019-12-19 15:54 

from django.urls import path
from . import views

app_name = 'qiantai'

urlpatterns = [
    path('ordering/', views.ordering, name='ordering'),
    path('getFoodById/', views.GetFoodById.as_view(), name='getFoodById'),
    path('getFoodByName/', views.get_food_by_name, name='get_food_by_name'),
    path('get_food_list/', views.get_food_list, name='get_food_list'),

    path('food/<num>/', views.food, name='food'),
    path('food_add/', views.food_add, name='food_add'),
    path('food_edit/<pk>/', views.food_edit, name='food_edit'),
    path('food_del/<pk>/', views.food_del, name='food_del'),

    path('ordered/<num>/', views.ordered, name='ordered'),
    path('ordered_detail/<pk>/', views.ordered_detail, name='ordered_detail'),
    path('ordered_del/<pk>/', views.ordered_del, name='ordered_del'),

    path('sale/', views.sale, name='sale'),
]