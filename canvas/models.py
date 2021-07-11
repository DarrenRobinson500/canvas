from django.db import models

class BusObj(models.Model):
    LEVEL_CHOICES = [(1,1),(2,2),(3,3)]

    name = models.CharField(max_length= 255,null=True,blank=True)
    level = models.IntegerField(null=True, blank=True,choices=LEVEL_CHOICES)
    description = models.TextField(null=True,blank=True)

    parent = models.ForeignKey("self",null=True,blank=True,on_delete = models.SET_NULL)

    def __str__(self):
        return self.name

class Process(models.Model):
    LEVEL_CHOICES = [(4,4),(5,5),(6,6)]

    name = models.CharField(max_length= 255,null=True,blank=True)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)
    description = models.TextField(null=True, blank=True)

    parent = models.ManyToManyField("self",blank=True, symmetrical=True)
    busobj = models.ManyToManyField(BusObj,blank=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    NODE_CHOICES = [
        ("person", "Person"),
        ("busobj", "BusObj"),
        ("process", "Process"),
        ("control", "Control"),
        ("event", "Event"),
        ("action", "Action"),]

    x = models.IntegerField(null=True,blank=True)
    y = models.IntegerField(null=True,blank=True)
    text = models.CharField(max_length= 255,null=True,blank=True)
    description = models.TextField(null=True,blank=True,default="No description")
    type = models.CharField(max_length=255, null=True,blank=True,choices=NODE_CHOICES)
    level = models.IntegerField(null=True,blank=True)
    parent = models.ManyToManyField("self",blank=True, symmetrical=False)
    process = models.ForeignKey(Process,null=True,blank=True,on_delete = models.CASCADE)
    busobj = models.ForeignKey(BusObj,null=True,blank=True,on_delete = models.CASCADE)
    def __str__(self):
        return self.text

class Connection(models.Model):
    a = models.ForeignKey(Node, blank = True, null = True, related_name = "Child", on_delete = models.CASCADE)
    b = models.ForeignKey(Node, blank = True, null = True, on_delete = models.CASCADE)

