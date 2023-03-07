from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("facebook_leads_callback/", views.facebook_leads_callback, name="facebook_leads_callback"),

    
    path("leads/", views.leads, name="leads"),
    path("stage/", views.stage, name="stage"),
    path("source/", views.source, name="source"),
    path("create_stage/", views.create_stage, name="create_stage"),
    path("create_source/", views.create_source, name="create_source"),
    path("delete_stage/<int:id>", views.delete_stage, name="delete_stage"),
    path("delete_source/<int:id>", views.delete_source, name="delete_source"),
    path("add_lead/", views.add_lead, name="add_lead"),
    path("delete_lead/<int:id>", views.delete_lead, name="delete_lead"),
    path("view_lead/<int:id>", views.view_lead, name="view_lead"),
    path("update_users/<int:id>", views.update_users, name="update_users"),
    path("add_note/<int:id>", views.add_note, name="add_note"),
    path("add_call/<int:id>", views.add_call, name="add_call"),
    path("add_file/<int:id>", views.add_file, name="add_file"),
    path("update_lead_status/<int:id>", views.update_lead_status, name="update_lead_status"),
    path("edit_lead/<int:id>", views.edit_lead, name="edit_lead"),
    path("close_lead/<int:id>", views.close_lead, name="close_lead"),
    path("reopen_lead/<int:id>", views.reopen_lead, name="reopen_lead"),

#     path("upload_leads/", views.upload_leads, name="upload_leads"),

    

#     re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
#     re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
