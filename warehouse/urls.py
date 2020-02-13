# _*_ coding=UTF-8 _*_
# 作者：Ariel
# 创建时间：2019-12-30 16:42
from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('entry/', views.entry, name='entry'),
    path('inventory/', views.inventory, name='inventory'),
    path('scrap/', views.scrap, name='scrap'),
    path('query/', views.query, name='query'),
    path('query2/', views.query2, name='query2'),
    path('delivery/', views.delivery, name='delivery'),

    path('purchase/', views.purchase, name='purchase'),
    path('purchase_confirm/', views.purchase_confirm, name='purchase_confirm'),
    path('purchased/', views.purchased, name='purchased'),
    path('purchased/<num>/', views.purchased, name='purchased'),

    path('supplier/<num>/', views.supplier, name='supplier'),
    path('supplier_del/<pk>', views.supplier_del, name='supplier_del'),
]
