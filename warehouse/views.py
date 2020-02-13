import json
import datetime
import decimal
import xlrd  # 读取excel表格数据的模块
from xlrd import xldate_as_tuple
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from personnel.models import Employee
from warehouse.models import Supplier, Purchase, PurchaseDetail, Material, Storage, Entry, EntryDetail, Delivery, \
    DeliveryDetail, Junk


# Create your views here.

def quliao(v, i, objs):
    obj = objs[i]
    if obj.num > v:
        obj.num -= v
        obj.save()
        return
    elif obj.num == v:
        obj.delete()
        return
    else:
        v = v - obj.num
        obj.delete()
        return quliao(v, i, objs)


def shelf_life(mdate,gdate):
    y, m, d = str(mdate).split('-')


# 领料登记
@csrf_exempt
def entry(request):
    if request.method == 'GET':
        context = {'storage': {stor_obj.material.name:
                                   {'id': stor_obj.material.id,
                                    'num': sum([s_obj.num for s_obj in
                                                Storage.objects.filter(material__name=stor_obj.material.name)])}
                               for stor_obj in Storage.objects.all()}}
        return render(request, 'warehouse/entry.html', context)
    elif request.method == 'POST':
        results = json.loads(request.POST['results'])
        entry_obj = Entry.objects.create(person=Employee.objects.get(account_id=request.user.id))
        for key, val in results.items():
            stor_objs = Storage.objects.filter(material__name=key).order_by('md')
            quliao(int(val), 0, stor_objs)
            EntryDetail.objects.create(entry=entry_obj, material=Material.objects.get(name=key), num=int(val))
            return JsonResponse({'status': 'success'})


# 采购入库
@csrf_exempt
def delivery(request):
    if request.method == 'GET':
        context = {'purchases': [{'id': pur_obj.id, 'date': pur_obj.date.strftime('%Y-%m-%d %H:%M:%S'),
                                  'term': pur_obj.term.strftime('%Y-%m-%d %H:%M:%S'),
                                  'materials': [{'id': Material.objects.get(name=pd_obj.material.name).id,
                                                 'name': pd_obj.material.name, 'num': pd_obj.num, 'left': pd_obj.left}
                                                for pd_obj in PurchaseDetail.objects.filter(purchase=pur_obj)]}
                                 for pur_obj in Purchase.objects.filter(received=False)]}
        return render(request, 'warehouse/delivery.html', context)
    elif request.method == 'POST':
        content = json.loads(request.POST['content'])
        pur_obj = Purchase.objects.get(id=content['id'])
        delivery_obj = Delivery.objects.create(
            person=Employee.objects.get(account_id=request.user.id))  # 获取入库人员登录账号即为入库人员ID
        for item in content['materials']:
            # 采购订单详单未到货数量减少
            pd_obj = PurchaseDetail.objects.get(purchase=pur_obj, material=item['id'])
            pd_obj.left -= int(item['count'])
            pd_obj.save()
            # 库存单对应物料数量增加
            Storage.objects.create(material_id=item['id'], num=int(item['count']), md=datetime.datetime.now())
            # 入库详单记录增加
            DeliveryDetail.objects.create(delivery=delivery_obj, material_id=item['id'], num=int(item['count']))
        # 判断采购订单是否还存在未到货
        received = True
        for pd_obj in PurchaseDetail.objects.filter(purchase=pur_obj):
            if pd_obj.left > 0:
                received = False
            if received:
                pur_obj.received = True
                pur_obj.save()
        return JsonResponse({'status': '入库成功！'})


# 库存盘点
@csrf_exempt
def inventory(request):
    if request.method == 'GET':
        context = {'storage': [{'id': stor_obj.id, 'name': stor_obj.material.name, 'num': stor_obj.num,
                                'date': stor_obj.date, 'material': stor_obj.material, 'md': str(stor_obj.md),
                                'gd': str(Material.objects.get(id=stor_obj.material_id).gd)
                                } for stor_obj in Storage.objects.all()]}
        return render(request, 'warehouse/inventory.html', context)
    elif request.method == "POST":
        content = json.loads(request.POST['content'])
        for storage_id, count in content.items():
            storage_obj = Storage.objects.get(id=storage_id)
            storage_obj.num = count
            storage_obj.save()
        return JsonResponse({'status': '变更成功！'})


# 报废
@csrf_exempt
def scrap(request):
    if request.method == "POST":
        content = json.loads(request.POST['content'])
        stor_id = int(content['storage'])
        scrap_num = int(content['num'])
        # 库存单数量减少
        storage_obj = Storage.objects.get(id=stor_id)
        if scrap_num > storage_obj.num:
            return JsonResponse({'status': '报废失败，报废数量超过库存数量!'})
        storage_obj.num -= scrap_num
        storage_obj.save()
        # 报废单记录增加
        Junk.objects.create(storage=storage_obj, num=scrap_num, reason=content['reason'])
        return JsonResponse({'status': '报废成功!'})


# 库存查询
def query(request):
    if request.method == 'GET':
        return render(request, 'warehouse/query.html')


def query2(request):
    if request.method == 'GET':
        context = {'storage': [{'id': stor_obj.id, 'name': stor_obj.material.name, 'num': stor_obj.num,
                                'date': str(stor_obj.date), 'gd': str(Material.objects.get(id=stor_obj.material_id).gd),
                                'material_id': stor_obj.material_id, 'md': str(stor_obj.md)} for stor_obj in
                               Storage.objects.all()],
                   'entry': [{'id': entry_obj.id, 'date': str(entry_obj.date), 'person': entry_obj.person.name,
                              'materials': '； '.join([ed.material.name + '*' + str(ed.num)
                                                      for ed in EntryDetail.objects.filter(entry=entry_obj)])}
                             for entry_obj in Entry.objects.all()],
                   'delivery': [
                       {'id': delivery_obj.id, 'date': str(delivery_obj.date), 'person': delivery_obj.person.name,
                        'materials': '； '.join([dd.material.name + '*' + str(dd.num)
                                                for dd in DeliveryDetail.objects.filter(delivery=delivery_obj)])}
                       for delivery_obj in Delivery.objects.all()]}
        return JsonResponse(context)


# 采购订单（上传Excel）
@csrf_exempt
def purchase(request):
    if request.method == 'GET':
        return render(request, 'warehouse/purchase.html')
    elif request.method == 'POST':
        file_obj = request.FILES.get('file')
        sheet = xlrd.open_workbook(file_contents=file_obj.read()).sheets()[0]
        content = {'materials': []}
        for i in range(sheet.nrows):
            if type(sheet.cell_value(i, 0)) == int or type(sheet.cell_value(i, 0)) == float:
                content['materials'].append({'name': sheet.cell_value(i, 1),
                                             'num': sheet.cell_value(i, 2),
                                             'price': str(decimal.Decimal(sheet.cell_value(i, 4))),
                                             'unit': sheet.cell_value(i, 3)})
            elif sheet.cell_value(i, 0).startswith('采购总金额'):
                content['price'] = str(decimal.Decimal(sheet.cell_value(i, 1)))
            elif sheet.cell_value(i, 0).startswith('支付方式'):
                content['method'] = sheet.cell_value(i, 1)
            elif sheet.cell_value(i, 0).startswith('已支付'):
                content['paid'] = sheet.cell_value(i, 1)
            elif sheet.cell_value(i, 0).startswith('签订日期'):
                content['date'] = datetime.datetime(
                    *xldate_as_tuple(sheet.cell_value(i, 1), 0)).strftime('%Y-%m-%d %H:%M:%S')
            elif sheet.cell_value(i, 0).startswith('收货期限'):
                content['term'] = datetime.datetime(
                    *xldate_as_tuple(sheet.cell_value(i, 1), 0)).strftime('%Y-%m-%d %H:%M:%S')
            elif sheet.cell_value(i, 0).startswith('已到货'):
                content['received'] = sheet.cell_value(i, 1)
            elif sheet.cell_value(i, 0).startswith('供方'):
                sn = sheet.cell_value(i, 1)
                supplier_obj = Supplier.objects.get(name=sn)
                content['supplier'] = {'name': sn, 'person': supplier_obj.charger,
                                       'phone': supplier_obj.phone, 'address': supplier_obj.address}
        person = Employee.objects.get(account=request.user.id)
        content['buyer'] = {'name': 'XX中餐厅', 'person': person.name, 'phone': person.phone, 'address': '幸福路幸福街区199号'}
        return JsonResponse({'status': 'success', 'content': content})


# 采购订单（保存到数据库）
@csrf_exempt
def purchase_confirm(request):
    if request.method == "POST":
        content = json.loads(request.POST['invoice'])
        purchase_obj = Purchase.objects.create(
            supplier=Supplier.objects.get(name=content['supplier']['name']),
            person=Employee.objects.get(name=content['buyer']['person']),
            method=content['method'], price=decimal.Decimal(content['price']),
            date=content['date'], term=content['term'],
            paid=(True if content['paid'] == '是' else False),
            received=(True if content['received'] == '是' else False),
        )
        for item in content['materials']:
            PurchaseDetail.objects.create(
                purchase=purchase_obj, left=int(item['num']), material=Material.objects.get(name=item['name']),
                num=int(item['num']), price=decimal.Decimal(item['price']))
        return JsonResponse({'status': '保存成功！'})


# 采购台账
@csrf_exempt
def purchased(request, num=1):
    if request.method == 'GET':
        num = int(num)
        purchases = Purchase.objects.all().order_by('-id')
        paginator = Paginator(purchases, per_page=15)
        page = paginator.page(num)
        context = {
            'paginator': paginator,
            'num': num,
            'page': page,
            'uri': 'warehouse:purchased'
        }
        return render(request, 'warehouse/purchased.html', context=context)
    elif request.method == 'POST':
        req = request.POST['command']
        id = request.POST['id']
        if req == 'query':
            pd_qs = PurchaseDetail.objects.filter(purchase=id)
            content = [{'material': pd_obj.material.name,
                        'num': pd_obj.num,
                        'price': str(pd_obj.price)} for pd_obj in pd_qs]
            return JsonResponse({'status': 'success', 'content': content})
        elif req == 'delete':
            PurchaseDetail.objects.filter(purchase=id).delete()
            Purchase.objects.get(id=id).delete()
            return JsonResponse({'status': '删除成功！'})


# 供应商管理
def supplier(request, num=1):
    if request.method == "GET":
        ok_msg = request.session.get('ok_msg')
        err_msg = request.session.get('err_msg')
        request.session['ok_msg'] = None
        request.session['err_msg'] = None

        num = int(num)
        suppliers = Supplier.objects.all().order_by('-id')
        paginator = Paginator(suppliers, per_page=5)
        page = paginator.page(num)
        context = {
            'paginator': paginator,
            'num': num,
            'page': page,
            'ok_msg': ok_msg,
            'err_msg': err_msg,
            'uri': 'warehouse:supplier'
        }
        return render(request, 'warehouse/supplier.html', context=context)
    if request.method == "POST":
        supplier = json.loads(request.POST['params'])
        Supplier.objects.create(
            name=supplier['name'], charger=supplier['charger'], phone=supplier['phone'], address=supplier['address']
        )
        return JsonResponse({'status': '保存成功！'})


# 删除供应商
def supplier_del(request, pk=None):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    request.session['ok_msg'] = '供应商删除成功!'
    return redirect('/warehouse/supplier/1/')
