from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  

urlpatterns = [
    path("hrm/", views.hrm, name="hrm"),
    path("hrm_setup/", views.hrm_setup, name="hrm_setup"),
    path("add_designation/", views.add_designation, name="add_designation"),
    path("delete_designation/<int:id>", views.delete_designation, name="delete_designation"),

    path("add_department/", views.add_department, name="add_department"),
    path("delete_department/<int:id>", views.delete_department, name="delete_department"),

    path("add_year/", views.add_year, name="add_year"),
    path("delete_year/<int:id>", views.delete_year, name="delete_year"),
    
    path("add_month/", views.add_month, name="add_month"),
    path("delete_month/<int:id>", views.delete_month, name="delete_month"),

    path("employees/", views.employees, name="employees"),
    path("add_employee/", views.add_employee, name="add_employee"),
    path("edit_employee/<int:id>", views.edit_employee, name="edit_employee"),
    path("delete_employee/<int:id>", views.delete_employee, name="delete_employee"),
    path("view_employee/<int:id>", views.view_employee, name="view_employee"),

    path("attendance/", views.attendance, name="attendance"),
    path("payroll/", views.payroll, name="payroll"),
    path("emp_payslip/", views.emp_payslip, name="emp_payslip"),
    path("pay_salary/", views.pay_salary, name="pay_salary"),
    path("salary_payment/", views.salary_payment, name="salary_payment"),
    path("log_sheet/", views.log_sheet, name="log_sheet"),
    path('punch_in/', views.punch_in, name='punch_in'),
    path('punch_out/', views.punch_out, name='punch_out'),
    path("advance_salary/", views.advance_salary, name="advance_salary"),
    path("leave/", views.leave, name="leave"),
    path("apply_leave/", views.apply_leave, name="apply_leave"),
    path("add_emp_leave/", views.add_emp_leave, name="add_emp_leave"),
    path("emp_leaves/", views.emp_leaves, name="emp_leaves"),
    
    
    path("accept_leave/<int:id>", views.accept_leave, name="accept_leave"),
    path("deny_leave/<int:id>", views.deny_leave, name="deny_leave"),





]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
