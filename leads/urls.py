from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("leads/", views.leads, name="leads"),
#     path("upload_leads/", views.upload_leads, name="upload_leads"),
#     path("add_lead/", views.add_lead, name="add_lead"),
#     path("delete_lead/<int:id>", views.delete_lead, name="delete_lead"),
#     path("view_lead/<int:id>", views.view_lead, name="view_lead"),
#     path("add_call/<int:id>", views.add_call, name="add_call"),
#     path("update_lead_status/<int:id>", views.update_lead_status, name="update_lead_status"),
#     path("update_users/<int:id>", views.update_users, name="update_users"),
#     path("add_note/<int:id>", views.add_note, name="add_note"),

#     path("edit_lead/<int:id>", views.edit_lead, name="edit_lead"),
#     path("close_lead/<int:id>", views.close_lead, name="close_lead"),
#     path("reopen_lead/<int:id>", views.reopen_lead, name="reopen_lead"),
    

#     re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
#     re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
