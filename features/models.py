from django.contrib.auth.models import User
from django.db import models
from account.models import *
import pytz
from django.utils import timezone



# Create your models here.

class LogSheet(models.Model):
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    punch_in_time = models.TimeField()
    punch_out_time = models.TimeField(null = True, blank = True)
    tasks = models.TextField(null = True, blank = True)
    meetings = models.TextField(null = True, blank = True)
    remarks = models.TextField(null = True, blank = True)
    # created = models.DateTimeField(default=timezone.now().astimezone(pytz.timezone('Asia/Kathmandu')))
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name_plural = "01. Log Sheet"



class ToDo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    task = models.TextField()
    deadline = models.TextField()
    task_from = models.TextField()
    task_to = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    priority = models.TextField()
    status = models.TextField(default = "incomplete")

    def __str__(self):
        return self.task_to.user.username

    class Meta:
        verbose_name_plural = "02. To Do"



class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_email = models.CharField(max_length=255)
    company_contact_number = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_images/')
    payment_terms = models.TextField()
    payment_details = models.TextField()
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "03. Company Setup"