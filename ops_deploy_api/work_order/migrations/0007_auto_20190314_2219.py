# Generated by Django 2.1.5 on 2019-03-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0006_auto_20190314_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='结束时间'),
        ),
    ]
