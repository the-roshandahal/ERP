from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("log_sheet/", views.log_sheet, name="log_sheet"),
    path("add_log_sheet/", views.add_log_sheet, name="add_log_sheet"),
    path("todo/", views.todo, name="todo"),
    path("add_todo/", views.add_todo, name="add_todo"),
    path("change_status/<int:id>", views.change_status, name="change_status"),
    path("reassign/<int:id>", views.reassign, name="reassign"),

    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
