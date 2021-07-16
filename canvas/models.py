from django.db import models


class Db(models.Model):
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
    LEVEL_CHOICES = [(1, 1), (2, 2), (3, 3)]

    type = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    notes = models.TextField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)
    links = models.ManyToManyField("self", blank=True, symmetrical=True)

    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    visible = models.BooleanField(null=True)

    incumbant = models.CharField(max_length=255, null=True, blank=True)

    impact_i = models.CharField(max_length=255, null=True, blank=True)
    likelihood_i = models.CharField(max_length=255, null=True, blank=True)
    impact_r = models.CharField(max_length=255, null=True, blank=True)
    likelihood_r = models.CharField(max_length=255, null=True, blank=True)
    risk_category = models.CharField(max_length=255, null=True, blank=True)

    frequency = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

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
        }
        return colour[self.type]


class BusObj(models.Model):
    LEVEL_CHOICES = [(1, 1), (2, 2), (3, 3)]

    name = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)
    description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Process(models.Model):
    LEVEL_CHOICES = [(4, 4), (5, 5), (6, 6)]

    name = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)
    description = models.TextField(null=True, blank=True)

    parent = models.ManyToManyField("self", blank=True, symmetrical=True)
    busobj = models.ManyToManyField(BusObj, blank=True)

    def __str__(self):
        return self.name


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
    process = models.ForeignKey(
        Process, null=True, blank=True, on_delete=models.CASCADE
    )
    busobj = models.ForeignKey(BusObj, null=True, blank=True, on_delete=models.CASCADE)

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
