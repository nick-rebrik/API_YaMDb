# Generated by Django 3.0.5 on 2021-06-19 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210619_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_superuser',
        ),
    ]
