# Generated by Django 2.1.8 on 2020-03-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blade_testbed', models.CharField(max_length=20)),
                ('blade_chassis_id', models.CharField(max_length=10)),
                ('blade_slot_id', models.CharField(max_length=10)),
                ('blade_pid', models.CharField(max_length=15)),
                ('blade_name', models.CharField(max_length=10)),
                ('blade_sn', models.CharField(max_length=12)),
                ('blade_cpu_info', models.CharField(max_length=80)),
                ('blade_memory_info', models.CharField(max_length=100)),
                ('blade_tpm_info', models.CharField(max_length=15)),
                ('blade_adaptor_info', models.CharField(max_length=80)),
                ('blade_mini_storage', models.CharField(max_length=15)),
                ('blade_storage_info', models.CharField(max_length=100)),
                ('blade_nvme_info', models.CharField(max_length=210)),
                ('blade_gpu_info', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='testbed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testbed_name', models.CharField(max_length=20)),
                ('testbed_ip', models.CharField(max_length=20)),
            ],
        ),
    ]
