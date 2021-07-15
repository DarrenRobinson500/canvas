from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from canvas import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("map/<type>/<id>", views.map, name="map"),
    path("list/<type>/", views.list, name="list"),
    path("new/<type>/", views.new, name="new"),
    path("ind/<type>/<id>", views.ind, name="ind"),
    path("delete/<type>/<id>", views.delete, name="delete"),
    path("update/<type>/<id>", views.update, name="update"),
    path("files/", views.files, name="files"),
    path("upload/", views.upload, name="upload"),
    path("load/<type>/<id>/", views.load, name="load"),
    path("file_delete/<id>/", views.file_delete, name="file_delete"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
