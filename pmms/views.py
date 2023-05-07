from .models import *
from django.shortcuts import render, redirect
from .models import Asset
from .forms import AssetForm

def dashboard(request):
    total_assets = Asset.objects.count()
    total_work_orders = WorkOrder.objects.count()
    total_maintenance_tasks = MaintenanceTask.objects.count()

    context = {
        'total_assets': total_assets,
        'total_work_orders': total_work_orders,
        'total_maintenance_tasks': total_maintenance_tasks
    }
    return render(request, 'dashboard.html', context)

def asset_list(request):
    assets = Asset.objects.all()
    context = {'assets': assets}
    return render(request, 'asset/list.html', context)

def asset_detail(request):
    assets = Asset.objects.all()
    context = {'assets': assets}
    return render(request, 'asset/detail.html', context)

def asset_type_list(request):
    asset_types = AssetType.objects.all()
    context = {'asset_types': asset_types}
    return render(request, 'asset/list.html', context)


def asset_type_detail(request, pk):
    asset_type = AssetType.objects.get(pk=pk)
    context = {'asset_type': asset_type}
    return render(request, 'asset/type_detail.html', context)
def work_order_list(request):
    work_orders = WorkOrder.objects.all()
    context = {'work_orders': work_orders}
    return render(request, 'work_order/list.html', context)
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()
    context = {'form': form}
    return render(request, 'asset/create.html', context)

def maintenance_task_list(request):
    maintenance_tasks = MaintenanceTask.objects.all()
    context = {'maintenance_tasks': maintenance_tasks}
    return render(request, 'maintenance_task/list.html', context)

# Add additional views for creating, updating, and deleting objects as needed
