from django.contrib import admin
from .models import Db, Node, Connection, File

admin.site.register(Db)
admin.site.register(Node)
admin.site.register(Connection)
admin.site.register(File)
