from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from dashboard.models import UCS, qali_result, Testcases, URLs
import paramiko
import os,datetime,re
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request, 'welcome_qali_dashboard.html', context=locals())

def add_Abundle_name(request):
    ucs_name = UCS()
    ucs_name.ucs_name = "ICMR3_patch_4_0_4h"
    ucs_name.save()


    return HttpResponse("add A bundle %s successfylly" % ucs_name.ucs_name)


def get_Abundle_name(request):
    Abundles = UCS.objects.all()

    return render(request, 'abundle_list.html', context = locals())


def del_Abundle_name(request):
    abundle = UCS.objects.filter(ucs_name__exact='ICMR3_4.0.4h')
    abundle.delete()
    abundle = UCS.objects.filter(ucs_name__exact='JB_4.1.1a')
    abundle.delete()
    abundle = UCS.objects.filter(ucs_name__exact='JB_MR1_4.1.2a')
    abundle.delete()
    return HttpResponse("delete A bundle successfully")




def get_testcase(request):

    hostname = '10.79.62.236'
    username = 'pengfwan'
    password = 'pengfwan'
    #remote_dir = '/home/pengfwan/qali-test/teams/bios/testcases'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command("cd /home/pengfwan/qali-test/teams/bios/testcases;ls")
    testcasefolder = []
    untestcasefolder = ['Catalog', 'BOOT', 'DIMM_ERR', 'EXEP', '__init__.py', 'INVENTORY_TIDY', 'OLD',
                        'OS_INSTALLATION', 'PCIE', 'PERF', 'STANDALONE', 'TEST']
    for i in stdout.readlines():
        i = i.replace('\n', '')
        if i not in untestcasefolder:
            testcasefolder.append(i)
    print (testcasefolder)
    untestcase = ['__init__.py', 'setup.py', 'cleanup.py']
    testcase_full = []
    for j in testcasefolder:
        stdin, stdout, stderr = ssh.exec_command(
            "cd /home/pengfwan/qali-test/teams/bios/testcases/{0};ls |grep .py".format(j))
        print(j)
        for i in stdout.readlines():
            i = i.replace('\n', '')
            if i not in untestcase:
                testcases = Testcases()
                k = i.replace('.py', '')
                oldcase = Testcases.objects.filter(t_name__exact=k)
                if oldcase:
                    oldcase.delete()
                print(k)
                testcases.t_name = k
                testcases.t_folder_name = j
                testcases.save()
    ssh.close()
    return HttpResponse('update script list success')


def show_testcase(request):

    testcases_list = Testcases.objects.all()
    print (len(testcases_list))
    return render(request, 'script_list.html', context=locals())

def check_ucs_ver(ucs_ver):
    ucs = ucs_ver
    ucs_first = ucs.split('.')[0]
    ucs_second = ucs.split('.')[1]
    ucs_third = ucs.split('.')[2]

#icmr3 patch 4.0.4h
    icmr3_404h = "4gS|4h"
#jb_patch 4.1.1b
    jb_414b = "1aS|1b"
#jb_patch 4.1.1c
    jb_414c = "1bS|1c"
#jb_patch 4.1.1d
    jb_414d = "1cS|1d"
#jb mr1 patch 4.1.2b
    jb_412b = '2aS|2b'
    if ucs_first == '4':
        if ucs_second == '0':
            if ucs_third in ['3', '4a']:
                print ('this is ICMR3_4.0.4a')
                ucsm_version = 'ICMR3_4_0_4a'
            icmr3404h = re.search(icmr3_404h, ucs)
            if icmr3404h:
                print ('this is ICMR3 patch-ICMR3_4.0.4h')
                ucsm_version = 'ICMR3_patch_4_0_4h'
        if ucs_second == '1':
            if ucs_third in ['0','1a']:
                print ('this is JB ')
                ucsm_version = 'JB_4_1_1a'
            jb414b = re.search(jb_414b, ucs)
            if jb414b:
                print ('this is JB patch-JB_4.1.1b')
                ucsm_version = 'JB_patch_4_1_1b'
            jb414c = re.search(jb_414c, ucs)
            if jb414c:
                print ('this is JB patch-4.1.4c')
                ucsm_version = 'JB_patch_4_1_1c'
            if ucs_third in ['1','2a']:
                print ('this is JBMR1')
                ucsm_version = 'JBMR1_4_1_2a'
            jb412b = re.search(jb_412b, ucs)
            if jb412b:
                print ('this is JBMR1 patch-4.1.2b')
                ucsm_version = 'JBMR1_patch_4_1_2b'
    return ucsm_version

def add_qaliresult(request):
    all_qali_link = URLs.objects.all()
    if request.method == "GET":
        return render(request, 'add_qali_result.html', context=locals())
    else:
        html = request.POST.get('new_link')
        print (html)

        url_flag = URLs.objects.filter(url_link__exact=html)
        if url_flag:
            return render(request,'add_qali_result.html',{'msg':'html link exists'})
        elif len(html) < 1:
            return render(request, 'add_qali_result.html', {'msg': 'html link cannot be blank'})
        else:
            url_link = URLs()
            url_link.url_link = html
            url_link.save()
            res = requests.get(html)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
    #overall qali config
            over_link = soup.select('a')[0]['href']

            qali_config = soup.select('table')[0].text
            for p in qali_config.split('\n'):
                if "UCS_version" in p:
                    overall_ucs_version = p.split(":")[1]

                if "Server" in p:
                    overall_server_version = p.split(":")[1]

                if "BIOS:" in p:
                    over_bios_version = p.split(":")[1]

                if "Python_version" in p:
                    oversion_python_version = p.split(":")[1]

                if "Comment" in p:
                    over_comments = p.split(":")[1]

            testcase_dic = []
            testcase_select = ['']

            for testcase_href in soup.select('td')[18:]:
                if testcase_href.text not in testcase_select:
                    testcase_dic.append(testcase_href.text)

            for i in testcase_dic:
                testcase_list = Testcases.objects.filter(t_name__exact=i)
                if testcase_list:
                    qali_case_list = qali_result()

                    qali_case_list.q_case_name = i

                    result = testcase_dic.index(i) + 1
                    qali_case_list.q_case_result = testcase_dic[result]

                    for testcase_href in soup.select('a'):
                        if i in testcase_href['href']:
                            qali_case_list.q_case_link = testcase_href['href']
                    qali_case_list.q_bios_name = over_bios_version
                    qali_case_list.q_blade_name = overall_server_version
                    qali_case_list.q_project_version = check_ucs_ver(overall_ucs_version.strip())
                    qali_case_list.q_abundle_version = overall_ucs_version
                    qali_case_list.q_origin_link = over_link
                    qali_case_list.q_comments = over_comments
                    qali_case_list.q_python_ver = oversion_python_version
                    qali_case_list.save()

            return render(request, 'add_qali_result.html', context=locals())

def del_html(request,id):

    result_html = URLs.objects.filter(id = id)
    result_html.delete()
    return redirect('/dashboard/add_qaliresult/')

def get_qali_result(request):
    qali_result_list = qali_result.objects.all()
    rel_project_list = []
    for i in qali_result_list:
        if not i.q_project_version in rel_project_list:
            rel_project_list.append(i.q_project_version)

    if request.method == 'GET':
        context = {
            "project_list": rel_project_list,
            #"qali_result": qali_result_list
        }
        return render(request, 'qali_result_list.html', context=context)
    else:
        result_project_id = request.POST.get('project_id')
        print(result_project_id)
        qali_result_list = qali_result.objects.filter(q_project_version__exact=result_project_id)
        pass_result = qali_result.objects.filter(q_project_version__exact=result_project_id).filter(q_case_result__exact="PASS")
        fail_result = qali_result.objects.filter(q_project_version__exact=result_project_id).filter(q_case_result__exact="FAIL")
        #all qali scripts
        over_all_len = len(Testcases.objects.all())
        #all selected qali results
        all_len = len(qali_result_list)
        #selected pass results
        pass_len = len(pass_result)
        #selected fail results
        fail_len = len(fail_result)
        #selected other fail results
        other_len = all_len-pass_len-fail_len
        #scripts not run in this project
        un_run_len = over_all_len-all_len

        context = {
            "project_list": rel_project_list,
            "selected_project_id": result_project_id,
            "qali_result": qali_result_list,
            "fail_result": fail_len,
            "pass_result": pass_len,
            "other_result": other_len,
            "un_run_result": un_run_len,

        }
        return render(request, 'qali_result_list.html', context=context)


def get_special_result(request,case_name):
    qali_result_list = qali_result.objects.filter(q_case_name__exact=case_name)
    return render(request, 'show_special_case_result.html', context=locals())


