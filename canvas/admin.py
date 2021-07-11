from django.contrib import admin
from .models import Process, Node, Connection

admin.site.register(Process)
admin.site.register(Node)
admin.site.register(Connection)
