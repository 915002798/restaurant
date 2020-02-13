import os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View

from kitchen.models import Prepare
from qiantai.models import Food, Order, FoodType, Detail
from restaurant.settings import UPLOAD_DIRS


# Create your views here.

class GetFoodById(View):
    def get(self, request):
        id = request.GET.get('id', '')
        food = get_object_or_404(Food, id=id)
        food_id = food.id
        food_name = food.name
        return JsonResponse({'food_id': food_id, 'food_name': food_name})


def get_food_by_name(request):
    name = request.GET.get('name', '')
    food = get_object_or_404(Food, name=name)
    food_id = food.id
    food_name = food.name
    return JsonResponse({'food_id': food_id, 'food_name': food_name})


def check_order(order):
    fields = ['type', 'price', 'foods', 'marks', 'guest', 'phone', 'address']
    for field in fields:
        if field not in order.keys():
            return {'status': 'failure', 'msg': '订单不完整'}
    if order['type'] == 3 and not (order['guest'] and order['phone'] and order['address']):
        return {'status': 'failure', 'msg': '订单不完整,配送订单需要填写顾客联系人，电话和地址！'}

    foods_ids = [food.id for food in Food.objects.all()]
    for food in order['foods']:
        if int(food) not in foods_ids:
            return {'status': 'failure', 'msg': '包含无效菜品！'}
        if not Food.objects.get(id=food).available:
            return {'status': 'failure', 'msg': '包含不可销售菜品！'}
    if (len(order['foods']) == 0) or (len(order['foods']) != len(order['marks'])) or (
            len(order['foods']) != len(order['numbs'])) or (len(order['numbs']) != len(order['marks'])):
        return {'status': 'failure', 'msg': '订单不完整！'}
    return {'status': 'success'}


# 点单
def ordering(request):
    if request.method == 'GET':
        context = dict()
        context['menu'] = {
            ft_obj.name: [{'id': fo_obj.id, 'name': fo_obj.name, 'price': fo_obj.price, 'image': fo_obj.image,
                           'describe': fo_obj.describe}
                          for fo_obj in Food.objects.filter(type=ft_obj.id, available=True)]
            for ft_obj in FoodType.objects.all()}
        return render(request, 'qiantai/ordering.html', context)
    if request.method == 'POST':
        order = json.loads(request.POST['params'])
        order['foods'], order['numbs'], order['marks'] = [], [], []
        for i in range(len(order['info'])):
            order['foods'].append(order['info'][i]['f'])
            order['numbs'].append(order['info'][i]['n'])
            order['marks'].append(order['info'][i]['m'])
        print(order)
        result = check_order(order)
        if result['status'] == 'success':
            order_obj = Order.objects.create(type=order['type'], price=order['price'], guest=order['guest'],
                                             phone=order['phone'], address=order['address'], state='未完成')
            result['id'] = order_obj.id
            detail_list = []
            for i in range(len(order['foods'])):
                food_state = '未分配'
                detail_list.append(Detail(order=order_obj,
                                          food=Food.objects.get(id=order['foods'][i]),
                                          mark=order['marks'][i],
                                          state=food_state))
            Detail.objects.bulk_create(detail_list)  # bulk_create()将多个实例插入数据库
        return JsonResponse({'status': '保存成功！'})


# 获取菜品列表
def get_food_list(request):
    foods = Food.objects.all()
    food_list = []
    for food in foods:
        f = ''.join([str(food.id), '--', food.name])
        food_list.append(f)
    return JsonResponse({'food_list': food_list})


# 菜品管理
def food(request, num=1):
    num = int(num)
    foods = Food.objects.all().order_by('-id')
    paginator = Paginator(foods, per_page=5)
    page = paginator.page(num)
    ok_msg = request.session.get('ok_msg')
    err_msg = request.session.get('err_msg')
    request.session['ok_msg'] = None
    request.session['err_msg'] = None

    context = {
        'paginator': paginator,
        'num': num,
        'page': page,
        'ok_msg': ok_msg,
        'err_msg': err_msg,
        'uri': 'qiantai:food'
    }
    return render(request, 'qiantai/food.html', context=context)


# 添加菜品
def food_add(request):
    foodtypes = FoodType.objects.all()
    if request.method == 'GET':
        return render(request, 'qiantai/food_add.html', {'foodtypes': foodtypes})
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        image = request.FILES.get('image', '')

        try:
            food = Food.objects.get(name=name)
            request.session['err_msg'] = '菜品名称重复！'
            return render(request, 'qiantai/food_add.html', {'foodtypes': foodtypes})
        except Food.DoesNotExist:

            if not os.path.exists(UPLOAD_DIRS):
                os.mkdir(UPLOAD_DIRS)
            with open(os.path.join(UPLOAD_DIRS, image.name), 'wb') as fw:
                for c in image.chunks():  # 将文件分块读取到内存上传节约内存
                    fw.write(c)

            Food.objects.create(
                name=name,
                describe=request.POST.get('describe', ''),
                image='/static/upload/' + image.name,
                type_id=int(request.POST.get('type', '')),
                price=request.POST.get('price', ''),
                available=(True if request.POST.get('available', '') == 'on' else False),
                score=request.POST.get('score', ''),
            )
            request.session['ok_msg'] = '菜品添加成功!'
        return redirect('/qiantai/food/1/')


# 修改菜品
def food_edit(request, pk=None):
    foodtypes = FoodType.objects.all()
    if request.method == 'GET':
        food = get_object_or_404(Food, pk=pk)
        return render(request, 'qiantai/food_edit.html', {'foodtypes': foodtypes, 'food': food})
    if request.method == 'POST':
        food = get_object_or_404(Food, pk=pk)
        image = request.FILES.get('image', '')

        if not os.path.exists(UPLOAD_DIRS):
            os.mkdir(UPLOAD_DIRS)
        with open(os.path.join(UPLOAD_DIRS, image.name), 'wb') as fw:
            for c in image.chunks():  # 将文件分块读取到内存上传节约内存
                fw.write(c)

        Food.objects.filter(pk=food.pk).update(
            name=request.POST.get('name', ''),
            describe=request.POST.get('describe', ''),
            image='/static/upload/' + image.name,
            type_id=int(request.POST.get('type', '')),
            price=request.POST.get('price', ''),
            available=(True if request.POST.get('available', '') == 'on' else False),
            score=request.POST.get('score', ''),
        )
        request.session['ok_msg'] = '菜品修改成功!'
    return redirect('/qiantai/food/1/')


# 删除菜品
def food_del(request, pk=None):
    food = get_object_or_404(Food, pk=pk)
    food.delete()
    request.session['ok_msg'] = '菜品删除成功!'
    return redirect('/qiantai/food/1/')


# 订单管理
def ordered(request, num=1):
    ok_msg = request.session.get('ok_msg')
    err_msg = request.session.get('err_msg')
    request.session['ok_msg'] = None
    request.session['err_msg'] = None

    num = int(num)
    orders = Order.objects.all().order_by('-id')
    paginator = Paginator(orders, per_page=15)
    page = paginator.page(num)
    context = {
        'paginator': paginator,
        'num': num,
        'page': page,
        'ok_msg': ok_msg,
        'err_msg': err_msg,
        'uri': 'qiantai:ordered'
    }
    return render(request, 'qiantai/ordered.html', context=context)


# 订单详情
def ordered_detail(request, pk=None):
    if request.method == "GET":
        order = get_object_or_404(Order, pk=pk)
        details = Detail.objects.filter(order=pk)

        return render(request, 'qiantai/order_detail.html', {"order": order, "details": details})


# 删除订单
def ordered_del(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    details = Detail.objects.filter(order=pk)

    for detail in details:
        detail.delete()
    order.delete()
    request.session['ok_msg'] = '订单删除成功!'
    return redirect('/qiantai/ordered/1/')


# 销售统计
def sale(request):
    return render(request, 'qiantai/sale.html')
