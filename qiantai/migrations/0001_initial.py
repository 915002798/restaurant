# Generated by Django 3.0 on 2019-12-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(blank=True, max_length=300, null=True, verbose_name='备注')),
                ('state', models.CharField(max_length=8, verbose_name='状态')),
            ],
            options={
                'verbose_name': '菜品详情',
                'verbose_name_plural': '菜品详情',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='菜品名')),
                ('describe', models.CharField(blank=True, max_length=300, null=True, verbose_name='描述')),
                ('image', models.CharField(max_length=300, verbose_name='菜品图片')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格')),
                ('available', models.BooleanField(default=True, verbose_name='是否可销售')),
                ('score', models.IntegerField(default=0, verbose_name='评分')),
            ],
            options={
                'verbose_name': '菜品',
                'verbose_name_plural': '菜品',
            },
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='菜品种类')),
            ],
            options={
                'verbose_name': '菜品种类',
                'verbose_name_plural': '菜品种类',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=8, verbose_name='类别')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='总价')),
                ('guest', models.CharField(blank=True, max_length=32, null=True, verbose_name='顾客')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='地址')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='日期')),
                ('state', models.CharField(max_length=8, verbose_name='状态')),
                ('foods', models.ManyToManyField(through='qiantai.Detail', to='qiantai.Food', verbose_name='菜品')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
    ]