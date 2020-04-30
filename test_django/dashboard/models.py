from django.db import models

class UCS(models.Model):
    ucs_name = models.CharField(max_length=20, unique=True,)

class URLs(models.Model):
    url_link = models.CharField(max_length=100, unique=True)

class qali_result(models.Model):
    q_bios_name = models.CharField(max_length=30)
    q_blade_name = models.CharField(max_length=16)
    q_case_name = models.CharField(max_length=48)
    q_case_result = models.CharField(max_length=10)
    q_case_link = models.CharField(max_length=150, unique=True)
    q_comments = models.CharField(max_length=16, default='qali')
    q_origin_link = models.CharField(max_length=100, default='link')
    q_python_ver = models.CharField(max_length=50, default='2.7.17')
    q_abundle_version = models.CharField(max_length=16, default='UCSM')
    q_project_version = models.CharField(max_length=30,)

class Testcases(models.Model):
    t_name = models.CharField(max_length=48, unique=True)
    t_folder_name = models.CharField(max_length=16)