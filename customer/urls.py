from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("client/", views.client, name="client"),
    path("add_client/", views.add_client, name="add_client"),
    path("edit_client/<int:id>", views.edit_client, name="edit_client"),
    path("delete_client/<int:id>", views.delete_client, name="delete_client"),
    path("view_client/<int:id>", views.view_client, name="view_client"),

]