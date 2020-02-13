from django.db import models


# Create your models here.


# 工位
class Station(models.Model):
    charger = models.ForeignKey('personnel.Employee', verbose_name='员工ID', related_name='station', on_delete=models.CASCADE)
    foods = models.ManyToManyField('qiantai.Food', verbose_name='可加工菜品', through='Capacity')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '工位'
        verbose_name_plural = verbose_name


# 任务分配表（工位加工任务）
class Capacity(models.Model):
    station = models.ForeignKey('Station', verbose_name='工位ID', related_name='capacity', on_delete=models.CASCADE)
    food = models.ForeignKey('qiantai.Food', verbose_name='菜品ID', related_name='capacity', on_delete=models.CASCADE)
    time = models.FloatField(verbose_name='加工时间')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '任务分配'
        verbose_name_plural = verbose_name


# 预备菜品
class Prepare(models.Model):
    food = models.ForeignKey('qiantai.Food', verbose_name='菜品ID', related_name='prepare', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='数量', default=0)
    used = models.IntegerField(verbose_name='已售', default=0)
    total = models.IntegerField(verbose_name='总计', default=0)
    date = models.TimeField(verbose_name='有效时间', auto_now=True)

    def __str__(self):
        return f'{self.food}'

    class Meta:
        verbose_name = '预备菜品'
        verbose_name_plural = verbose_name
