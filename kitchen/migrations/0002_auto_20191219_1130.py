# Generated by Django 3.0 on 2019-12-19 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('qiantai', '0001_initial'),
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='foods',
            field=models.ManyToManyField(through='kitchen.Capacity', to='qiantai.Food', verbose_name='可加工菜品'),
        ),
        migrations.AddField(
            model_name='prepare',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qiantai.Food', verbose_name='菜品ID'),
        ),
        migrations.AddField(
            model_name='capacity',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qiantai.Food', verbose_name='菜品ID'),
        ),
        migrations.AddField(
            model_name='capacity',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.Station', verbose_name='工位ID'),
        ),
    ]