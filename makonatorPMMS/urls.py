"""
URL configuration for makonatorPMMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from pmms import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.asset_list, name='asset_list'),
    #path('asset/edit/<int:asset_id>/', views.asset_edit, name='asset_edit'),
    path('asset/<int:pk>/', views.asset_type_detail, name='asset_type_detail'),
    path('assets/create/', views.asset_create, name='asset_create'),
    path('work_orders/', views.work_order_list, name='work_order_list'),
    path('maintenance_tasks/', views.maintenance_task_list, name='maintenance_task_list'),
    path('admin/', admin.site.urls),


    # Add additional URL patterns for creating, updating, and deleting objects as needed
]
