"""
URL configuration for staffix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('load_admin_app', views.load_admin_app , name='load_admin_app'),
    path('register_job', views.register_job , name='register_job'),
    path('register_view', views.register_view , name='register_view'),
    path('edit_job/<int:job_id>', views.edit_job , name='edit_job'),
    path('delete_job/<int:job_id>', views.delete_job , name='delete_job'),
    path('view_applications', views.view_applications , name='view_applications'),
    path('approve_application/<int:application_id>', views.approve_application , name='approve_application'),
    path('delete_application/<int:application_id>', views.delete_application , name='delete_application'),
    path('onboard', views.onboard , name='onboard'),
    path('delete_onboard/<int:application_id>', views.delete_onboard , name='delete_onboard'),
    path('add_employee/<int:application_id>', views.add_employee , name='add_employee'),
    path('our_employees', views.our_employees , name='our_employees'),
    path('employee/<int:employee_id>', views.employee_detail, name='employee_detail'),
    path('admin_dashboard', views.admin_dashboard , name='admin_dashboard'),
]
