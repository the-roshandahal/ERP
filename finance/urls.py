from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("invoice/", views.invoice, name="invoice"),
    # path("create_invoice/", views.create_invoice, name="create_invoice"),   
    # path("view_invoice/<int:id>", views.view_invoice, name="view_invoice"),
    # path("single_invoice/<int:id>", views.single_invoice, name="single_invoice"),

    path("receipt/", views.receipt, name="receipt"),
    # path("create_receipt/", views.create_receipt, name="create_receipt"),
    # path("view_receipt/<int:id>", views.view_receipt, name="view_receipt"),
    # path("single_receipt/<int:id>", views.single_receipt, name="single_receipt"),

    # path("clients/", views.clients, name="clients"),
    # path("add_client/", views.add_client, name="add_client"),

    # path("statement/", views.statement, name="statement"),
    # path("single_statement/<int:id>", views.single_statement, name="single_statement"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)