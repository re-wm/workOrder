# Generated by Django 2.1.5 on 2019-03-11 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0002_operator_onduty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='onduty',
            field=models.IntegerField(default=0),
        ),
    ]
