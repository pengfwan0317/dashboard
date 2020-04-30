from django.urls import path, re_path
from server_inventory import views

urlpatterns = [
    re_path(r'^$', views.index),
    path('testbed_inventory/', views.show_testbed_inventory),
    path('search_blade/', views.search_blade),
    re_path('^search_platform/(\w+)/',views.search_platform),
    re_path('^del_testbed/(\w+)/', views.del_testbed),
    re_path('^update_testbed_blade/(\w+)/', views.update_testbed_blade),
    re_path('^show_testbed_blade/(\w+)', views.show_testbed_blade),
    path('del_spe_testbed/',views.del_special_testbed),
]