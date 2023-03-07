from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("products/", views.products, name="products"),
    path("add_product/", views.add_product, name="add_product"),
    path("edit_package/<int:id>", views.edit_package, name="edit_package"),
    path("delete_package/<int:id>", views.delete_package, name="delete_package"),

]