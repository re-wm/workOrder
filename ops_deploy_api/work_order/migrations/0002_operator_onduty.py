# Generated by Django 2.1.5 on 2019-03-10 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='onduty',
            field=models.BooleanField(default=0),
        ),
    ]
