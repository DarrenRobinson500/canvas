from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.forms import ModelForm
from .models import Db, File

class BusObjForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = Db.objects.filter(type="busobj")

    class Meta:
        model = Db
        fields = ('links',)
        labels = {'links': 'Add another business objective',}
        widgets = {'links': forms.SelectMultiple(attrs={'class':'form-control'})}

class BaseForm(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="busobj"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Db
        fields = ("name", "description", "level", "links")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "level": forms.Select(attrs={"class": "form-control"}),
        }


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ("name", "type", "document")
        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "document": forms.FileInput(
                attrs={"class": "form-control", "placeholder": ""}
            ),
        }
