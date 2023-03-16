from django.db import models
from django.contrib.auth.models import User
from account.models import *
# from django.contrib.auth.models import User
# Create your models here.

class YearSetup(models.Model):
    year = models.CharField(max_length=255)
    def __str__(self):
        return self.year
    class Meta:
        verbose_name_plural = "04. Year"



class MonthSetup(models.Model):
    year = models.ForeignKey(YearSetup, on_delete=models.CASCADE)
    month = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.year.year} - {self.month} ({self.start_date.strftime('%b %d, %Y')})"


    class Meta:
        verbose_name_plural = "05. Month"

class Holidays(models.Model):
    month = models.ForeignKey(MonthSetup,on_delete=models.CASCADE)
    holiday = models.DateField(blank=True)

    def __str__(self):
        return self.month.month
    class Meta:
        verbose_name_plural = "05. Holiday"


class Department(models.Model):
    department = models.CharField(max_length=255)
    def __str__(self):
        return self.department
    class Meta:
        verbose_name_plural = "05. Department"


class Designation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    def __str__(self):
        return self.designation
    class Meta:
        verbose_name_plural = "05. Designation"

class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    contact = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    emp_salary = models.CharField(max_length=200,null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "01. Employees"

class LogSheet(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    punch_in_time = models.TimeField()
    punch_out_time = models.TimeField(null = True, blank = True)
    tasks = models.TextField(null = True, blank = True)
    meetings = models.TextField(null = True, blank = True)
    remarks = models.TextField(null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name_plural = "01. Log Sheet"
class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=100)
    leave_deduction = models.FloatField(max_length=255,null=True, blank=True)
    tax_deduction = models.FloatField(max_length=255,null=True, blank=True)
    company_deduction = models.FloatField(max_length=255,null=True, blank=True)
    paid_salary = models.FloatField(max_length=255,null=True, blank=True)
    type = models.CharField(max_length=255,null=True, blank=True, default='salary')
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.employee.user.first_name

    class Meta:
        verbose_name_plural = "03. Salary"

        
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255,null=True, blank=True)
    status = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.employee.user.username

    class Meta:
        verbose_name_plural = "02. Leave"

class LeaveDate(models.Model):
    leave = models.ForeignKey(Leave,on_delete=models.CASCADE)
    date = models.DateField(max_length=220)
    def __str__(self):
        return self.leave.employee.user.username

    class Meta:
        verbose_name_plural = "02. Leave Dates"

