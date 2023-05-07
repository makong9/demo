from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone



class AssetType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AssetCategory(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Asset(models.Model):
    asset_tag = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,blank=True, null=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    purchase_date = models.DateField(default=timezone.now)
    warranty_expiration = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class AssetHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    document = models.FileField(upload_to='asset_history_docs/', null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} - {self.description}"

class AssetPerformanceData(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()

    def __str__(self):
        return f"{self.asset.name} - {self.metric_name}"

class DepreciationMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AssetDepreciation(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    depreciation_method = models.ForeignKey(DepreciationMethod, on_delete=models.CASCADE)
    acquisition_cost = models.DecimalField(max_digits=10, decimal_places=2)
    useful_life = models.PositiveIntegerField()  # in years
    salvage_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} - {self.depreciation_method.name}"

class WorkOrderPriority(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.name

class WorkOrderStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WorkOrder(models.Model):
    description = models.CharField(max_length=255)
    priority = models.ForeignKey(WorkOrderPriority, on_delete=models.CASCADE)
    deadline = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(WorkOrderStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class WorkOrderHistory(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.work_order.description} - {self.description}"

class WorkOrderTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    priority = models.ForeignKey(WorkOrderPriority, on_delete=models.CASCADE)
    estimated_duration = models.PositiveIntegerField()  # in hours

    def __str__(self):
        return self.name

class WorkOrderComment(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.work_order.description}"

class MaintenanceTrigger(models.Model):
    TRIGGER_TYPE_CHOICES = [
        ('time', 'Time Interval'),
        ('usage', 'Usage'),
        ('custom', 'Custom'),
    ]
    name = models.CharField(max_length=100)
    trigger_type = models.CharField(max_length=10, choices=TRIGGER_TYPE_CHOICES)

    def __str__(self):
        return self.name

class MaintenanceTask(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    trigger = models.ForeignKey(MaintenanceTrigger, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MaintenanceEvent(models.Model):
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    due_date = models.DateField()
    work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.task.name} - {self.due_date}"

class MaintenanceChecklist(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    items = models.TextField()  # For simplicity, store items as a single text field, you can use JSON or other format

    def __str__(self):
        return self.name
