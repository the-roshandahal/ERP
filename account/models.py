from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Role(models.Model):
    role = models.CharField(max_length=255)
    def __str__(self):
        return self.role
    
    class Meta:
        verbose_name_plural = "01. Role"

class Permission(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    create_finance = models.BooleanField(default=0)
    read_finance = models.BooleanField(default=0)
    update_finance = models.BooleanField(default=0)
    delete_finance = models.BooleanField(default=0)
    manage_finance = models.BooleanField(default=0)
    
    manage_company = models.BooleanField(default=0)

    create_account = models.BooleanField(default=0)
    read_account = models.BooleanField(default=0)
    update_account = models.BooleanField(default=0)
    delete_account = models.BooleanField(default=0)
    manage_account = models.BooleanField(default=0)
    
    create_leads = models.BooleanField(default=0)
    read_leads = models.BooleanField(default=0)
    update_leads = models.BooleanField(default=0)
    delete_leads = models.BooleanField(default=0)
    manage_leads = models.BooleanField(default=0)
    manage_leads = models.BooleanField(default=0)

    create_hrm = models.BooleanField(default=0)
    read_hrm = models.BooleanField(default=0)
    update_hrm = models.BooleanField(default=0)
    delete_hrm = models.BooleanField(default=0)
    manage_hrm = models.BooleanField(default=0)

    create_products = models.BooleanField(default=0)
    read_products = models.BooleanField(default=0)
    update_products = models.BooleanField(default=0)
    delete_products = models.BooleanField(default=0)
    manage_products = models.BooleanField(default=0)
    def __str__(self):
        return self.role.role
    
    class Meta:
        verbose_name_plural = "02. Permissions"

