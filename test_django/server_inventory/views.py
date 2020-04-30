from django.http import HttpResponse
from django.shortcuts import render
from server_inventory.models import testbed, blade
from django.shortcuts import render, redirect
import paramiko
import os,datetime,re
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    return render(request, 'welcome_server_inventory.html')


def show_testbed_inventory(request):
    all_testbed = testbed.objects.all()
    if request.method == "GET":
        return render(request, 'show_testbed_inventory.html', context=locals())
    else:
        New_testbed_name = request.POST.get('new_testbed_name')
        New_testbed_ip = request.POST.get('new_testbed_ip')

        testbed_ip_flag = testbed.objects.filter(testbed_ip__exact=New_testbed_ip)
        if testbed_ip_flag:
            return render(request, 'show_testbed_inventory.html', {'msg': 'testbed ip exists'})
        elif len(New_testbed_name) < 1:
            return render(request, 'show_testbed_inventory.html', {'msg': 'testbed name cannot be blank'})
        elif len(New_testbed_ip) < 1:
            return render(request, 'show_testbed_inventory.html', {'msg': 'testbed ip cannot be blank'})
        else:
            new_testbed = testbed()
            new_testbed.testbed_name = New_testbed_name
            new_testbed.testbed_ip = New_testbed_ip
            new_testbed.save()
            return render(request, 'show_testbed_inventory.html', context=locals())


def del_testbed(request, id):
    testbed_name = testbed.objects.filter(id = id)
    testbed_name.delete()
    blade_name = blade.objects.filter(id = id)
    blade_name.delete()
    return redirect('/server_inventory/testbed_inventory/')


def update_testbed_blade(request, testbedname):
    testbed_name = testbed.objects.filter(testbed_name__exact=testbedname)
    blade_testbed = blade.objects.filter(blade_testbed__exact=testbedname)
    blade_testbed.delete()
    for i in testbed_name:
        query_ip = i.testbed_ip
    hostname = query_ip
    username = 'admin'
    password = 'Nbv12345'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password)
    #get chassis NO
    stdin, stdout, stderr = ssh.exec_command("show chassis")
    for i in stdout:
        if ('Acknowledged' in i):
            chassis_no = i.split()[0]
            print('chassis no is {0}'.format(chassis_no))
    #get server NO
            stdin, stdout, stderr = ssh.exec_command("scope chassis {0};show server detail|grep Slot:".format(chassis_no))
            for i in stdout:
                blade_no = i.split(':')[1].strip()
                #blade_no = re.findall("Slot: (.+?)", i, re.DOTALL)[0]
    #get server health status
                stdin, stdout, stderr = ssh.exec_command(
                    "scope server {0}/{1};show status detail|grep 'Slot Status'".format(chassis_no,blade_no))
                for i in stdout:
                    if 'Missing' in i:
                        print ('blade {0}/{1} is Missing'.format(chassis_no,blade_no))
                    else:
                        blade_info_all = blade()
                        print('blade {0}/{1} is Equipped'.format(chassis_no, blade_no))
                        #get blade discovery status
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show status detail|grep 'Discovery'".format(chassis_no, blade_no))
                        for i in stdout:
                            blade_discovery = i.split(':')[1]
                            discovery_flag = True if 'Complete' in blade_discovery else False
    #get blade detail information
                        #show position
                        blade_info_all.blade_testbed = testbedname
                        blade_info_all.blade_chassis_id = chassis_no
                        blade_info_all.blade_slot_id = blade_no
                        #show PID
                        blade_pid = 'NA'
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show detail|grep PID".format(chassis_no,blade_no))
                        for i in stdout:
                            blade_pid = i.split(':')[1].strip()
                        print (blade_pid)
                        blade_info_all.blade_pid = blade_pid
                        #show SN
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show detail|grep Serial".format(chassis_no, blade_no))
                        for i in stdout:
                            blade_sn = i.split(':')[1].strip()
                        print (blade_sn)
                        blade_info_all.blade_sn = blade_sn
                        #show CPU
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show cpu detail".format(chassis_no, blade_no))
                        cpu_info = 'NA'
                        if discovery_flag:
                            line_nu = 0
                            for i in stdout:
                                if line_nu < 12:
                                    j = i.strip()
                                    if 'Cores:' in j:
                                        cpu_cores = j.split()[1]
                                    if 'Product Name:' in j:
                                        cpu_name = j.split(':')[1]
                                    if 'Speed (GHz):' in j:
                                        cpu_speed = j.split(':')[1].replace('0','')
                                    if 'Stepping:' in j:
                                        cpu_step = j.split()[1]
                                    line_nu += 1
                                else:
                                    break
                            cpu_info = cpu_name+' '+cpu_cores+'C'+cpu_speed+'GHz '+'stepping '+cpu_step
                        print (cpu_info)
                        blade_info_all.blade_cpu_info = cpu_info
                        #show_cisco_blade_name
                        if discovery_flag:
                            if blade_pid in 'UCSB-B200-M6':
                                blade_info_all.blade_name = 'Wasco'
                            if blade_pid in 'UCSB-B200-M5':
                                blade_info_all.blade_name = 'PR-CKL' if int(cpu_step) > 4 else 'PR-SKL'
                            if blade_pid in 'UCSB-B480-M5':
                                blade_info_all.blade_name = 'PO-CKL' if int(cpu_step) > 4 else 'PO-SKL'
                            if blade_pid in 'UCSB-B420-M4':
                                blade_info_all.blade_name = 'KC-BDW' if 'v4' in cpu_name else 'KC-HSW'
                            if blade_pid in 'UCSB-B200-M4':
                                blade_info_all.blade_name = 'CS-BDW' if 'v4' in cpu_name else 'CS-HSW'
                            if blade_pid in 'UCSB-B200-M3':
                                blade_info_all.blade_name = 'CR-IVB' if 'v2' in cpu_name else 'CR-SNB'
                            if blade_pid in 'UCSB-B420-M3':
                                blade_info_all.blade_name = 'SEQ-IVB' if 'v2' in cpu_name else 'SEQ-SNB'
                            if blade_pid in 'UCSB-B22-M3':
                                blade_info_all.blade_name = 'SC-IVB' if 'v2' in cpu_name else 'SC-SNB'
                            if blade_pid in 'UCSB-EX-M4-3':
                                blade_info_all.blade_name = 'Shasta'
                            if blade_pid in 'UCSB-EX-M4-2':
                                blade_info_all.blade_name = 'YS2'
                            if blade_pid in 'UCSB-EX-M4-1':
                                blade_info_all.blade_name = 'YS1'
                            if blade_pid in 'N20-B6625-1':
                                blade_info_all.blade_name = 'Gooding'
                            if blade_pid in 'N20-B6625-2':
                                blade_info_all.blade_name = 'Ventura'
                            if 'B230' in blade_pid:
                                blade_info_all.blade_name = 'Marin'
                            if blade_pid in 'B440-BASE-M2':
                                blade_info_all.blade_name = 'SF'
                        else:
                            blade_info_all.blade_name = 'NA'
                        #show Memory
                        all_memory_info = one_memory_info = memory_amount = 'NA'
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show memory detail".format(chassis_no, blade_no))

                        if discovery_flag:
                            line_nu = 0
                            for i in stdout:
                                if line_nu < 12:
                                    j = i.strip()
                                    if 'Product Name:' in j:
                                        memory_name = j.split(':')[1]
                                    if 'Vendor Description:' in j:
                                        memory_vendor = j.split(':')[1]
                                    if 'PID:' in j:
                                        memory_pid = j.split(':')[1]
                                    line_nu += 1
                                else:
                                    break
                            one_memory_info = memory_vendor + memory_name + '/'+memory_pid
                            stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show memory detail|grep Equipped|wc -l".format(chassis_no, blade_no))
                            for i in stdout:
                                memory_amount = i.strip()
                            all_memory_info = memory_amount + ' *' + one_memory_info
                        print (all_memory_info)
                        blade_info_all.blade_memory_info = all_memory_info
                        #show tpm
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show tpm detail|grep Model".format(chassis_no, blade_no))
                        tpm_info = 'NA'
                        for i in stdout:
                            tpm_info = i.split(':')[1].strip()
                        print (tpm_info)
                        blade_info_all.blade_tpm_info = tpm_info
                        #show adaptor
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show adapter detail|grep PID".format(chassis_no, blade_no))
                        adaptor_list = []
                        if discovery_flag:
                            for i in stdout:
                                adaptor_info = i.split(':')[1].strip()
                                adaptor_list.append(adaptor_info)
                            print(adaptor_list)
                        blade_info_all.blade_adaptor_info = adaptor_list
                        #show M.2
                        m2_name = 'NA'
                        if discovery_flag:
                            if re.search('M5', blade_pid):
                                print(blade_pid)
                                stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show mini-storage detail|grep Model".format(chassis_no, blade_no))
                                for i in stdout:
                                    m2_name = i.split(':')[1].strip()
                        print (m2_name)
                        blade_info_all.blade_mini_storage = m2_name
                        #show storage controller
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show raid-controller detail|grep PID".format(chassis_no, blade_no))
                        storage_list = []
                        for i in stdout:
                            single_storage = i.split(':')[1].strip()
                            if 'N/A' not in single_storage:
                                storage_list.append(single_storage)
                        print(storage_list)
                        if stdout and '' in storage_list:
                            stdin, stdout1, stderr = ssh.exec_command(
                                "scope server {0}/{1};show raid-controller detail|grep Model".format(chassis_no,
                                                                                                   blade_no))
                            for i in stdout1:
                                single_storage = i.split(':')[1].strip()
                                storage_list.append(single_storage)
                            print(storage_list)
                        while '' in storage_list:
                            storage_list.remove('')
                        all_storage_list = storage_list
                        blade_info_all.blade_storage_info = all_storage_list
                        #show GPU
                        stdin, stdout, stderr = ssh.exec_command(
                            "scope server {0}/{1};show graphics-card detail|grep Model".format(chassis_no, blade_no))
                        gpu_model = 'NA'
                        if stdout and stdout:
                            for i in stdout:
                                gpu_model = i.split(':')[1].strip()
                        blade_info_all.blade_gpu_info = gpu_model
                        blade_info_all.save()
    return redirect('/server_inventory/testbed_inventory/')


def show_testbed_blade(request,testbedname):
    testbed_name = testbed.objects.filter(testbed_name__exact=testbedname)
    for i in testbed_name:
        query_ip = i.testbed_ip

    testbed_blade_list = blade.objects.filter(blade_testbed=testbedname)
    return render(request,'show_testbed_blade.html',context=locals())


def search_blade(request):
    search_blade_sn = request.POST.get('server_sn')
    search_blade_sn = search_blade_sn.lower()
    search_blade_flag = blade.objects.filter(blade_sn__exact=search_blade_sn)
    if search_blade_flag:
        return render(request, 'show_special_blade.html', context=locals())
    else:
        return redirect('/server_inventory/')


def search_platform(request,testplatform):
    search_platfor_name = blade.objects.filter(blade_name__contains=testplatform)
    if search_platfor_name:
        return render(request, 'show_special_platform.html', context=locals())
    else:
        return redirect('/server_inventory/')


def del_special_testbed(request):
    blade_name = blade.objects.filter(blade_testbed__exact='ten')
    blade_name.delete()
    return redirect('/server_inventory/testbed_inventory/')