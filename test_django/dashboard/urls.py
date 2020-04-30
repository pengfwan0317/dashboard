from django.urls import path, re_path
from dashboard import views

urlpatterns = [
    re_path(r'^$', views.index),
    path('index/', views.index),
    path('add_Abundle/', views.add_Abundle_name),
    path('del_Abundle/', views.del_Abundle_name),
    path('get_Abundle/', views.get_Abundle_name),
    path('update_testcase/', views.get_testcase),
    path('get_testcase/', views.show_testcase),
    path('add_qaliresult/', views.add_qaliresult),
    re_path('^del_html/(\w+)',views.del_html),
    path('show_qali_result/', views.get_qali_result),

    re_path('^get_qali_result/(\w+)/', views.get_special_result),

]