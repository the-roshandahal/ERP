from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("", views.home, name="home"),
    # path("clients/", views.clients, name="clients"),
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    # path("add_client/", views.add_client, name="add_client"),
    # path("package/", views.package, name="package"),
    # path("add_package/", views.add_package, name="add_package"),
    # path("invoice/", views.invoice, name="invoice"),
    # path("receipt/", views.receipt, name="receipt"),
    # path("create_invoice/", views.create_invoice, name="create_invoice"),   
    # path("create_receipt/", views.create_receipt, name="create_receipt"),
    # path("statement/", views.statement, name="statement"),
    # path("cpr/", views.cpr, name="cpr"),
    # path("followup/", views.followup, name="followup"),
    # path("single_statement/<int:id>", views.single_statement, name="single_statement"),

    # path("view_invoice/<int:id>", views.view_invoice, name="view_invoice"),
    # path("view_receipt/<int:id>", views.view_receipt, name="view_receipt"),

    # path("single_invoice/<int:id>", views.single_invoice, name="single_invoice"),
    # path("single_receipt/<int:id>", views.single_receipt, name="single_receipt"),



    # path("edit_package/<int:id>", views.edit_package, name="edit_package"),
    # path("delete_package/<int:id>", views.delete_package, name="delete_package"),
    # path("edit_client/<int:id>", views.edit_client, name="edit_client"),
    # path("edit_cpr/<int:id>", views.edit_cpr, name="edit_cpr"),

    # path("log_sheet/", views.log_sheet, name="log_sheet"),
    # path("add_log_sheet/", views.add_log_sheet, name="add_log_sheet"),

    # path("todo/", views.todo, name="todo"),
    # path("add_todo/", views.add_todo, name="add_todo"),
    # path("change_status/<int:id>", views.change_status, name="change_status"),
    
    # path("reassign/<int:id>", views.reassign, name="reassign"),

    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
