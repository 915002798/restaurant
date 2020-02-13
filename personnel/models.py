from django.contrib import auth
from django.db import models

# Create your models here.


def get_temp_user():
    am = auth.get_user_model()
    return am.objects.get(id=2).id   # 这里的id=2是在后台添加用户的时候给采购人员添加的用户id号,对于每个角色不同的用户需要更改


# 员工表
class Employee(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=32)
    phone = models.CharField(verbose_name='电话', max_length=32)
    performance = models.IntegerField(verbose_name='绩效', null=True)
    salary = models.DecimalField(verbose_name='工资', max_digits=16, decimal_places=2, null=True, blank=True)
    account = models.ForeignKey('auth.user', verbose_name='账号ID', on_delete=models.CASCADE,
                                null=True, default=get_temp_user)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '员工表'
        verbose_name_plural = verbose_name


# 职位表
class Job(models.Model):
    name = models.CharField(verbose_name='职位名称', max_length=32)
    salary = models.DecimalField(verbose_name='岗位工资', max_digits=16, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '职位表'
        verbose_name_plural = verbose_name


# 排班表
class Distribute(models.Model):
    employee = models.ForeignKey('Employee', verbose_name='员工ID', related_name='distribute', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', verbose_name='职位ID', related_name='distribute', on_delete=models.CASCADE)
    period = models.CharField(verbose_name='工作时间段', max_length=300)

    def __str__(self):
        return f'{self.job}--{self.period}'

    class Meta:
        verbose_name = '排班表'
        verbose_name_plural = verbose_name
