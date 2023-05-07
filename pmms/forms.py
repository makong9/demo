from django import forms
from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','location','asset_type']

class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name']