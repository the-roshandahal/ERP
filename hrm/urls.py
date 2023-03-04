from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  

urlpatterns = [
    path("hrm/", views.hrm, name="hrm"),
    path("hrm_setup/", views.hrm_setup, name="hrm_setup"),
    path("employees/", views.employees, name="employees"),
    path("add_year/", views.add_year, name="add_year"),
    path("add_month/", views.add_month, name="add_month"),
    path("add_employee/", views.add_employee, name="add_employee"),
    path("attendance/", views.attendance, name="attendance"),
    path("add_leave/", views.add_leave, name="add_leave"),
    path("salary/", views.salary, name="salary"),
    path("pay_salary/", views.pay_salary, name="pay_salary"),
    path("advance_salary/", views.advance_salary, name="advance_salary"),

    # path("edit_employee/<int:id>", views.edit_employee, name="edit_employee"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
