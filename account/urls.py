from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("role/", views.role, name="role"),
    path("create_role/", views.create_role, name="create_role"),
    path("edit_role/<int:id>", views.edit_role, name="edit_role"),
    path("delete_role/<int:id>", views.delete_role, name="delete_role"),

    path("company_user/", views.company_user, name="company_user"),
    path("create_company_user/", views.create_company_user, name="create_company_user"),
    path("edit_company_user/<int:id>", views.edit_company_user, name="edit_company_user"),
    path("delete_company_user/<int:id>", views.delete_company_user, name="delete_company_user"),


    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
