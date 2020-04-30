from django.db import models

class testbed(models.Model):
    testbed_name = models.CharField(max_length=20, )
    testbed_ip = models.CharField(max_length=20, )

class blade(models.Model):
    blade_testbed = models.CharField(max_length=20)
    blade_chassis_id = models.CharField(max_length=10)
    blade_slot_id = models.CharField(max_length=10)
    blade_pid = models.CharField(max_length=30)
    blade_name = models.CharField(max_length=10)
    blade_sn = models.CharField(max_length=12)
    blade_cpu_info = models.CharField(max_length=80)
    blade_memory_info = models.CharField(max_length=150)
    blade_tpm_info = models.CharField(max_length=15)
    blade_adaptor_info = models.CharField(max_length=80)
    blade_mini_storage = models.CharField(max_length=30)
    blade_storage_info = models.CharField(max_length=150)
    #blade_nvme_info = models.CharField(max_length=210)
    blade_gpu_info = models.CharField(max_length=20)