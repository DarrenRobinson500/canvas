from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django.forms import ModelForm
from .models import Db, File

class DateInput(forms.DateInput):
    input_type = 'date'

class OwnerLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="role"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )
    class Meta:
        model = Db
        fields = ("links",)

class BusObjLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="busobj"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )
    class Meta:
        model = Db
        fields = ("links",)

class ProcessLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="process"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),)
    class Meta:
        model = Db
        fields = ("links",)

class RiskLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="risk"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),)
    class Meta:
        model = Db
        fields = ("links",)

class ControlLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="control"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),)
    class Meta:
        model = Db
        fields = ("links",)

class MetricLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="metric"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),)
    class Meta:
        model = Db
        fields = ("links",)

class IssueLink(ModelForm):
    links = forms.ModelMultipleChoiceField(
        queryset=Db.objects.filter(type="metric"), required=False,
        label="",widget=forms.SelectMultiple(attrs={"class": "form-control"}),)
    class Meta:
        model = Db
        fields = ("links",)


class BaseForm(ModelForm):
    class Meta:
        model = Db
        fields = ("name", "description", "level",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "level": forms.Select(attrs={"class": "form-control"}),
        }

class RiskForm(ModelForm):
    class Meta:
        model = Db
        fields = ("name", "description", "level", "impact_i", "likelihood_i", "impact_r", "likelihood_r", )
        labels = {
            'impact_i': 'Inherent Impact',
            'likelihood_i': 'Inherent Likelihood',
            'impact_r': 'Residual Impact',
            'likelihood_r': 'Residual Likelihood',
        }
        widgets = {
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        "level": forms.Select(attrs={"class": "form-control"}),
        "impact_i": forms.Select(attrs={"class": "form-control"}),
        "likelihood_i": forms.Select(attrs={"class": "form-control"}),
        "impact_r": forms.Select(attrs={"class": "form-control"}),
        "likelihood_r": forms.Select(attrs={"class": "form-control"}),
        }

class ControlForm(ModelForm):
    class Meta:
        model = Db
        fields = ("name", "description", "date_first", "frequency_inst", "frequency_test")
        labels = {
            'date_first': 'Date of first run',
            'frequency_inst': 'How often is the control performed',
            'frequency_test': 'How often is the control tested',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "date_first": forms.DateInput(attrs={"class": "form-control", 'type': 'date'}),
            "frequency_inst": forms.Select(attrs={"class": "form-control"}),
            "frequency_test": forms.Select(attrs={"class": "form-control"}),
        }

class ControlInstForm(ModelForm):
    class Meta:
        model = Db
        fields = ("date_performed", "description", "outcome")
        labels = {
            'date_performed': 'Date performed',
            'description': 'Notes',
        }
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "outcome": forms.Select(attrs={"class": "form-control"}),
            "date_performed": forms.DateInput(attrs={"class": "form-control", 'type': 'date'}),
        }

class ControlTestForm(ModelForm):
    class Meta:
        model = Db
        fields = ("date_performed", "description", "outcome")
        labels = {
            'date_performed': 'Date performed',
            'description': 'Notes',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "outcome": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "date_performed": forms.DateInput(attrs={"class": "form-control", 'type': 'date'}),
        }

class ActionForm(ModelForm):
    class Meta:
        model = Db
        fields = ("name", "description", "level", "date_due")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "date_due": forms.DateInput(attrs={"class": "form-control", 'type': 'date'}),
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
