from django.db import models
from django.db.models import Max
from .constants import full_name
import datetime


def add_frequency(startdate, frequency):
    delta = datetime.timedelta(days=0)
    if frequency == "Monthly": delta = datetime.timedelta(days=30)
    if frequency == "Quarterly": delta = datetime.timedelta(days=91)
    if frequency == "Half yearly": delta = datetime.timedelta(days=182)
    if frequency == "Yearly": delta = datetime.timedelta(days=365)
    return (startdate + delta)


class Db(models.Model):
    TYPE_CHOICES = [
        ("role", "role"),
        ("busobj", "busobj"),
        ("obligation", "obligation"),
        ("process", "process"),
        ("risk", "risk"),
        ("metric", "metric"),
        ("control", "control"),
        ("control_inst", "control_inst"),
        ("control_test", "control_test"),
        ("issue", "issue"),
        ("action", "action"),
    ]
    LEVEL_CHOICES = [(1, 1), (2, 2), (3, 3)]

    LIKELIHOOD_CHOICES = [
        ("1", "Rare (1) <10%"),
        ("2", "Unlikely (2) 10% - 25%"),
        ("3", "Possible (3) 25% - 50%"),
        ("4", "Likely (4) 50% - 80%"),
        ("5", "Almost Certain (5) > 80%"),
    ]
    IMPACT_CHOICES = [
        ("1", "Insignificant"),
        ("2", "Minor"),
        ("3", "Moderate"),
        ("4", "Major"),
        ("5", "Severe"),
    ]

    FREQUENCY_CHOICES = [("Once", "Once"), ("Monthly", "Monthly"), ("Quarterly", "Quarterly"), ("Half yearly", "Half yearly"),("Yearly", "Yearly"),]
    OUTCOME_CHOICES = [("Failure", "Failure"), ("Qualified", "Qualified"), ("Success", "Success"),]

    type = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_due = models.DateField(null=True, blank=True)
    date_first = models.DateField(null=True, blank=True)
    date_performed = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)
    links = models.ManyToManyField("self", blank=True, symmetrical=True)

    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    visible = models.BooleanField(null=True)

    incumbant = models.CharField(max_length=255, null=True, blank=True)

    impact_i = models.CharField(max_length=255, null=True, blank=True, choices=IMPACT_CHOICES)
    likelihood_i = models.CharField(max_length=255, null=True, blank=True, choices=LIKELIHOOD_CHOICES)
    impact_r = models.CharField(max_length=255, null=True, blank=True, choices=IMPACT_CHOICES)
    likelihood_r = models.CharField(max_length=255, null=True, blank=True, choices=LIKELIHOOD_CHOICES)
    risk_category = models.CharField(max_length=255, null=True, blank=True)

    frequency = models.CharField(max_length=255, null=True, blank=True, choices=FREQUENCY_CHOICES)
    frequency_inst = models.CharField(max_length=255, null=True, blank=True, choices=FREQUENCY_CHOICES)
    frequency_test = models.CharField(max_length=255, null=True, blank=True, choices=FREQUENCY_CHOICES)
    outcome = models.CharField(max_length=255, null=True, blank=True, choices=OUTCOME_CHOICES)

    def __str__(self):
        if self.name is None:
            result = "No name provided"
        else:
            result = self.name
        return result

    def next_due_inst(self):
        result = ""
        if self.type == "control":
            query = self.links.all().filter(type='control_inst').order_by('-date_performed')
            if query.count() > 0:
                result = query[0].date_performed
            else:
                result = self.date_created
            result = add_frequency(result, self.frequency_inst)
        return result

    def next_due_test(self):
        result = ""
        if self.type == "control":
            query = self.links.all().filter(type='control_test').order_by('-date_performed')
            if query.count() > 0:
                result = query[0].date_performed
            else:
                result = self.date_created
            result = add_frequency(result, self.frequency_test)
        return result

    def owner(self):
        query = self.links.all().filter(type='role')
        if query.count() == 0: result = ""
        else: result = query[0]
        if self.type == "role": result = ""
        return result

    def owner_id(self):
        query = self.links.all().filter(type='role')
        if query.count() == 0: result = "Error"
        else: result = query[0].id
        return result

    def busobj(self):
        query = self.links.all().filter(type='busobj')
        result = ""
        if query.count() > 0:
            for item in query: result = result + ", " + item.name
            result = result[1:]
        return result

    def process(self):
        query = self.links.all().filter(type='process')
        result = ""
        if query.count() > 0:
            for item in query: result = result + ", " + item.name
            result = result[1:]
        return result

    def risk(self):
        query = self.links.all().filter(type='risk')
        result = ""
        if query.count() > 0:
            for item in query: result = result + ", " + item.name
            result = result[1:]
        return result

    def control(self):
        query = self.links.all().filter(type='control')
        result = ""
        if query.count() > 0:
            for item in query: result = result + ", " + item.name
            result = result[1:]
        return result

    def control(self):
        query = self.links.all().filter(type='control_inst')

    def control_inst(self):
        query = self.links.all().filter(type='control_inst')
        result = ""
        if query.count() > 0:
            for item in query:
                if result is None:
                    result = ", " + item.name
                # else:
                #     result = result + ", " + item.name

            result = result[1:]
            if result is None:
                result = "NONE"
        return result

    def control_test(self):
        query = self.links.all().filter(type='control_test')
        result = ""
        if query.count() > 0:
            for item in query: result = result + ", " + item.name
            result = result[1:]
        return result

    def type_full(self):
        if self.type is None:
            result = "No type"
        else:
            result = full_name[self.type]
        return result

    def colour(self):
        colour = {
            "role": "purple",
            "busobj": "blue",
            "obligation": "blue",
            "theme": "black",
            "process": "green",
            "risk": "orange",
            "metric": "yellow",
            "control": "yellow",
            "control_inst": "yellow",
            "control_test": "yellow",
        }
        return colour[self.type]

    def risk_rating(self):
        risk_rating = ""
        if self.type == "risk":
            risk_rating = "Low"
        if self.impact_r=="2" and self.likelihood_r=="5":
            risk_rating = "Medium"
        if self.impact_r=="3":
            risk_rating = "Medium"
            if self.likelihood_r == "1":
                risk_rating = "Low"
        if self.impact_r=="4":
            risk_rating = "High"
            if self.likelihood_r == "1":
                risk_rating = "Medium"
        if self.impact_r=="5":
            risk_rating = "Severe"
            if self.likelihood_r == "1":
                risk_rating = "High"
        return risk_rating

class Node(models.Model):
    NODE_CHOICES = [
        ("person", "Person"),
        ("busobj", "BusObj"),
        ("process", "Process"),
        ("control", "Control"),
        ("event", "Event"),
        ("action", "Action"),
    ]

    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="No description")
    type = models.CharField(max_length=255, null=True, blank=True, choices=NODE_CHOICES)
    level = models.IntegerField(null=True, blank=True)
    parent = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return self.text


class Connection(models.Model):
    a = models.ForeignKey(Db, blank = True, null = True, related_name = "Child", on_delete = models.CASCADE)
    b = models.ForeignKey(Db, blank = True, null = True, on_delete = models.CASCADE)
    visible = models.BooleanField(null=True)


class File(models.Model):
    TYPE_CHOICES = [
        ("role", "role"),
        ("busobj", "busobj"),
        ("obligation", "obligation"),
        ("process", "process"),
        ("risk", "risk"),
        ("metric", "metric"),
        ("control", "control"),
        ("issue", "issue"),
    ]

    name = models.CharField(max_length=100)
    document = models.FileField(upload_to="files/", blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)
