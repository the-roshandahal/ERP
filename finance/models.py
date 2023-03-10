from django.db import models
from customer.models import *
from products.models import *
# Create your models here.


        
PAYMENT_CHOICES = (('bank_transfer','bank_transfer'),('esewa','esewa'),('cash','cash'))
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    
    misc_name = models.CharField(max_length=255,null = True, blank = True)
    misc_amount = models.FloatField(null = True, blank = True)
    discount = models.FloatField(null = True, blank = True)
    vat_amount = models.FloatField(null = True, blank = True)
    invoice_amount = models.FloatField(null = True, blank = True)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    created_by = models.CharField(max_length = 255, null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.client_name

    class Meta:
        verbose_name_plural = "01. Invoices"


class Receipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paid_amount  = models.FloatField()
    payment_method = models.CharField( choices = PAYMENT_CHOICES, max_length=255)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    payment_receipt = models.FileField(upload_to="receipts",null = True, blank = True)
    created_by = models.CharField(max_length = 255, null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.client_name
    
    class Meta:
        verbose_name_plural = "02. Receipts"

class Statement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    amount = models.FloatField(null = True, blank = True)
    payment = models.FloatField(null = True, blank = True)
    balance = models.FloatField(null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.client_name

    class Meta:
        verbose_name_plural = "05. Statements"
