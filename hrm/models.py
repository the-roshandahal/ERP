from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    position = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    contact = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    emp_salary = models.CharField(max_length=200,null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "01. Employees"


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255,null=True, blank=True)
    is_absent = models.BooleanField(default=1)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.employee.name

    class Meta:
        verbose_name_plural = "02. Leave"





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
        return self.employee.name

    class Meta:
        verbose_name_plural = "03. Salary"



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
        return self.month
    class Meta:
        verbose_name_plural = "05. Month"