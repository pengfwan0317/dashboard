# Generated by Django 2.1.8 on 2020-03-27 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blade',
            name='blade_nvme_info',
        ),
    ]