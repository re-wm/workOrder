# Generated by Django 2.1.5 on 2019-03-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0014_auto_20190315_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='passwd',
            field=models.CharField(default='123456', max_length=20, verbose_name='运维密码'),
        ),
    ]