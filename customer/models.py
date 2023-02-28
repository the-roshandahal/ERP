from django.db import models

# Create your models here.
class Package(models.Model):
    package_name = models.CharField(max_length=255)
    package_description = models.TextField(null = True, blank = True)
    package_price = models.FloatField()
    def __str__(self):
        return self.package_name
    class Meta:
        verbose_name_plural = "01. Packages"

class Customer(models.Model):
    client_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    def __str__(self):
        return self.client_name
    class Meta:
        verbose_name_plural = "02. Clients"