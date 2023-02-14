from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Role(models.Model):
    role = models.CharField(max_length=255)
    def __str__(self):
        return self.role
    class Meta:
        verbose_name_plural = "01. User Types"



class Permission(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    create = models.BooleanField()
    read = models.BooleanField()
    update = models.BooleanField()
    delete = models.BooleanField()

    def __str__(self):
        return self.role.role
    class Meta:
        verbose_name_plural = "02. Permissions"
