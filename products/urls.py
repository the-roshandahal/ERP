from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("products/", views.products, name="products"),
    path("add_product/", views.add_product, name="add_product"),
    path("edit_product/<int:id>", views.edit_product, name="edit_product"),
    path("delete_product/<int:id>", views.delete_product, name="delete_product"),

    path("product_setup/", views.product_setup, name="product_setup"),

    path("add_product_category/", views.add_product_category, name="add_product_category"),
    path("edit_product_category/<int:id>", views.edit_product_category, name="edit_product_category"),
    path("delete_product_category/<int:id>", views.delete_product_category, name="delete_product_category"),

    path("add_product_unit/", views.add_product_unit, name="add_product_unit"),
    path("edit_product_unit/<int:id>", views.edit_product_unit, name="edit_product_unit"),
    path("delete_product_unit/<int:id>", views.delete_product_unit, name="delete_product_unit"),

]