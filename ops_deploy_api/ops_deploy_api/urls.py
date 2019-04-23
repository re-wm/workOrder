"""ops_deploy_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from work_order import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.login),
    path('index/', views.index),
    path('ops_order/', views.ops_order),
    path('no_order_ops/', views.no_order_ops),
    path('yes_order_ops/', views.yes_order_ops),
    path('index2/', views.index2),
    path('sub_order/', views.sub_order),
    path('no_order_sub/', views.no_order_sub),
    path('yes_order_sub/', views.yes_order_sub),
    path('ops_on/', views.ops_on),
    # path('ops_on_set/', views.ops_on_set),
    path('logout/', views.logout),
    path('order_list/', views.order_list),
    path('add_order/', views.add_order),
    path('delete_order/', views.delete_order),
    path('edit_order/', views.edit_order),
    path('user_list/', views.user_list),
    path('add_user/', views.add_user),
    path('delete_user/', views.delete_user),
    path('edit_user/', views.edit_user),
    path('group_list/', views.group_list),
    path('add_group/', views.add_group),
    path('delete_group/', views.delete_group),
    path('edit_group/', views.edit_group),
    path('company_list/', views.company_list),
    path('add_company/', views.add_company),
    path('delete_company/', views.delete_company),
    path('edit_company/', views.edit_company),
    # path('add_order/', views.add_order),
    # path('delete_order/', views.delete_order),
]
