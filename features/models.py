from django.contrib.auth.models import User
from django.db import models
from account.models import *
# Create your models here.

class LogSheet(models.Model):
    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    punch_in_time = models.TimeField()
    punch_out_time = models.TimeField(null = True, blank = True)
    tasks = models.TextField(null = True, blank = True)
    meetings = models.TextField(null = True, blank = True)
    remarks = models.TextField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name_plural = "08. Log Sheet"



class ToDo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    task = models.TextField()
    deadline = models.TextField()
    task_from = models.TextField()
    task_to = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    priority = models.TextField()
    status = models.TextField(default = "incomplete")

    def __str__(self):
        return self.task_to.username

    class Meta:
        verbose_name_plural = "08. To Do"