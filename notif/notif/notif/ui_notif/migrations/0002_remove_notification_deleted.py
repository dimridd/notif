# Generated by Django 2.2.4 on 2020-01-17 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui_notif', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='deleted',
        ),
    ]