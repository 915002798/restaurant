from django.db import models


# Create your models here.


# 物料单
class Material(models.Model):
    name = models.CharField(verbose_name='物料名', max_length=32)
    type = models.CharField(verbose_name='类别', max_length=16)
    unit = models.CharField(verbose_name='单位', max_length=16)  # 物料包装单位
    gd = models.IntegerField(verbose_name='保质期')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '物料单'
        verbose_name_plural = verbose_name


# 物料清单
class Bom(models.Model):
    food = models.ForeignKey('qiantai.Food', verbose_name='菜品ID', related_name='bom', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', verbose_name='物料ID', related_name='bom', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量')

    def __str__(self):
        return f'{self.food}'

    class Meta:
        verbose_name = '物料清单'
        verbose_name_plural = verbose_name


# 供应商
class Supplier(models.Model):
    name = models.CharField(verbose_name='供应商名', max_length=32)
    charger = models.CharField(verbose_name='联系人', max_length=16)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    address = models.CharField(verbose_name='地址', max_length=300)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name


# 库存单
class Storage(models.Model):
    material = models.ForeignKey('Material', verbose_name='物料编号', related_name='storage', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量')
    md = models.DateTimeField(verbose_name='生产日期')
    date = models.DateTimeField(verbose_name='入库日期', auto_now_add=True)

    def __str__(self):
        return f'{self.material}====={self.md}'

    class Meta:
        verbose_name = '库存单'
        verbose_name_plural = verbose_name


# 报废单
class Junk(models.Model):
    storage = models.ForeignKey('Storage', verbose_name='库存编号', related_name='junk', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='报废数量')
    reason = models.CharField(verbose_name='报废原因', max_length=300)
    date = models.DateTimeField(verbose_name='报废日期', auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '报废单'
        verbose_name_plural = verbose_name


# 采购单
class Purchase(models.Model):
    date = models.DateTimeField(verbose_name='签订日期', auto_now_add=True, db_index=True)  # 加索引
    term = models.DateTimeField(verbose_name='收货期限', null=True)
    person = models.ForeignKey('personnel.Employee', verbose_name='采购人员ID', related_name='purchase',
                               on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', verbose_name='供应商ID', related_name='purchase', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='总价', max_digits=8, decimal_places=2)
    method = models.CharField(verbose_name='支付方式', max_length=16, null=True)
    paid = models.BooleanField(verbose_name='已支付', default=False)
    received = models.BooleanField(verbose_name='已到货', default=False)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = '采购单'
        verbose_name_plural = verbose_name


# 采购明细
class PurchaseDetail(models.Model):
    purchase = models.ForeignKey('Purchase', verbose_name='所属采购单ID', related_name='purchase_detail',
                                 on_delete=models.CASCADE)
    material = models.ForeignKey('Material', verbose_name='所属物料单ID', related_name='purchase_detail',
                                 on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='单价', max_digits=8, decimal_places=2)
    num = models.IntegerField(verbose_name='数量')
    left = models.IntegerField(verbose_name='未到货数量', default=0)

    def __str__(self):
        return f'{self.purchase}'

    class Meta:
        verbose_name = '采购明细'
        verbose_name_plural = verbose_name


# 领料单
class Entry(models.Model):
    date = models.DateTimeField(verbose_name='领料时间', auto_now_add=True)
    person = models.ForeignKey('personnel.Employee', verbose_name='人员ID', related_name='entry',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = '领料单'
        verbose_name_plural = verbose_name


# 领料详单
class EntryDetail(models.Model):
    entry = models.ForeignKey('Entry', verbose_name='领料单ID', related_name='entry_detail', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', verbose_name='物料ID', related_name='entry_detail', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量')

    def __str__(self):
        return f'{self.num}'

    class Meta:
        verbose_name = '领料详单'
        verbose_name_plural = verbose_name


# 采购入库单
class Delivery(models.Model):
    date = models.DateTimeField(verbose_name='入库时间', auto_now_add=True)
    person = models.ForeignKey('personnel.Employee', verbose_name='人员ID', related_name='delivery',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = '采购入库单'
        verbose_name_plural = verbose_name


# 采购入库详单
class DeliveryDetail(models.Model):
    delivery = models.ForeignKey('Delivery', verbose_name='入库单ID', related_name='delivery_detail',
                                 on_delete=models.CASCADE)
    material = models.ForeignKey('Material', verbose_name='物料ID', related_name='delivery_detail',
                                 on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量')

    def __str__(self):
        return f'{self.num}'

    class Meta:
        verbose_name = '采购入库详单'
        verbose_name_plural = verbose_name
