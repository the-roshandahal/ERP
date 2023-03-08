from django.db import models

# Create your models here.


class Customer(models.Model):
    client_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.client_name
    class Meta:
        verbose_name_plural = "01. Clients"