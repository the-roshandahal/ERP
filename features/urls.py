from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("", views.home, name="home"),
    path("company_setup/", views.company_setup, name="company_setup"),
    path("add_company_setup/", views.add_company_setup, name="add_company_setup"),
    path("edit_company_setup/<int:id>", views.edit_company_setup, name="edit_company_setup"),
    path("todo/", views.todo, name="todo"),
    path("add_todo/", views.add_todo, name="add_todo"),
    path("change_status/<int:id>", views.change_status, name="change_status"),
    path("reassign/<int:id>", views.reassign, name="reassign"),


    

    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
