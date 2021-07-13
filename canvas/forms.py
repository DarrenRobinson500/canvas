from django import forms
from django.forms import ModelForm
from .models import Db, File

class BaseForm(ModelForm):
    class Meta:
        model = Db
        fields = ('name', 'description', 'level', 'links')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'level': forms.Select(attrs={'class':'form-control'}),
            'links': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ('name','type','document')
        widgets = {
            'type': forms.Select(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }

