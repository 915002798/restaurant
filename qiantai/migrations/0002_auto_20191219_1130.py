# Generated by Django 3.0 on 2019-12-19 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse', '0001_initial'),
        ('qiantai', '0001_initial'),
        ('kitchen', '0002_auto_20191219_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='material',
            field=models.ManyToManyField(through='warehouse.Bom', to='warehouse.Material', verbose_name='所需物料清单'),
        ),
        migrations.AddField(
            model_name='food',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qiantai.FoodType', verbose_name='类别ID'),
        ),
        migrations.AddField(
            model_name='detail',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qiantai.Food', verbose_name='菜品ID'),
        ),
        migrations.AddField(
            model_name='detail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qiantai.Order', verbose_name='订单ID'),
        ),
        migrations.AddField(
            model_name='detail',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.Station', verbose_name='所属工位ID'),
        ),
    ]