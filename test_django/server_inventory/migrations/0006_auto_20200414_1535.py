# Generated by Django 2.1.8 on 2020-04-14 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_inventory', '0005_auto_20200328_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blade',
            name='blade_pid',
            field=models.CharField(max_length=30),
        ),
    ]