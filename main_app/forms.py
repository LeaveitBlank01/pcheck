from django.contrib.auth.models import User
from django import forms
from . import models

class CreatePCForm(forms.ModelForm):
    class Meta:
        model = models.PC
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control select'}),
            'system_condition': forms.Select(attrs={'class': 'form-control select'}),
        }


class UpdatePCForm(forms.ModelForm):
    class Meta(CreatePCForm.Meta):
        fields = '__all__'

