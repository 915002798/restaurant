from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

# 菜品种类
class FoodType(models.Model):
    name = models.CharField(max_length=32, verbose_name='菜品种类')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '菜品种类'
        verbose_name_plural = verbose_name


# 菜品
class Food(models.Model):
    name = models.CharField(verbose_name='菜品名', max_length=16, unique=True)
    describe = models.CharField(verbose_name='描述', max_length=300, null=True, blank=True)
    image = models.ImageField(verbose_name='菜品图片地址', upload_to='static/upload/')
    type = models.ForeignKey('FoodType', verbose_name='类别', related_name='food', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='单价', max_digits=8, decimal_places=2)
    available = models.BooleanField(verbose_name='可销售', default=True)
    score = models.IntegerField(verbose_name="评分", default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    material = models.ManyToManyField('warehouse.Material', verbose_name="原料", through='warehouse.Bom')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '菜品'
        verbose_name_plural = verbose_name


# 订单
class Order(models.Model):
    type = models.CharField(verbose_name='类别', max_length=8)
    foods = models.ManyToManyField('Food', verbose_name='菜品', through='Detail')
    price = models.DecimalField(verbose_name='总价', max_digits=8, decimal_places=2)
    guest = models.CharField(verbose_name='顾客', max_length=32, null=True, blank=True)
    phone = models.CharField(verbose_name='手机', max_length=11, null=True, blank=True)
    address = models.CharField(verbose_name='地址', max_length=300, null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='日期', auto_now_add=True, db_index=True)  # 加索引
    state = models.CharField(verbose_name='状态', max_length=8)

    def __str__(self):
        return f'{self.id}--{self.type}'

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


# 菜品详情（订单==菜品，多对多）
class Detail(models.Model):
    order = models.ForeignKey('Order', verbose_name='订单ID', related_name='detail', on_delete=models.CASCADE)
    food = models.ForeignKey('Food', verbose_name='菜品ID', related_name='detail', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量', default=1,)
    mark = models.CharField(verbose_name='备注', max_length=300, null=True, blank=True)
    state = models.CharField(verbose_name='完成状态', max_length=8)
    station = models.ForeignKey('kitchen.Station', verbose_name='所属工位ID', related_name='detail',
                                on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.order}--{self.food}--{self.state}'

    class Meta:
        verbose_name = '菜品详情'
        verbose_name_plural = verbose_name
