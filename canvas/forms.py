from django import forms
from django.forms import ModelForm
from .models import BusObj, Process

class BusObjForm(ModelForm):
    class Meta:
        model = BusObj
        fields = ('name', 'description', 'level', 'parent')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'level': forms.Select(attrs={'class':'form-control'}),
            'parent': forms.Select(attrs={'class':'form-control'}),
        }

class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ('name',  'description', 'level', 'busobj', 'parent', )
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'level': forms.Select(attrs={'class':'form-control'}),
            'busobj': forms.SelectMultiple(attrs={'class':'form-control'}),
            'parent': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

