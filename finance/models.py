from django.db import models
from customer.models import *
from products.models import *
# Create your models here.

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    misc_name = models.CharField(max_length=255,null = True, blank = True)
    misc_amount = models.FloatField(null = True, blank = True)
    discount = models.FloatField(null = True, blank = True)
    vat_amount = models.FloatField(null = True, blank = True)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    created_by = models.CharField(max_length = 255, null = True, blank = True)
    due_date = models.DateField()
    invoice_amount = models.FloatField(null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.client_name

    class Meta:
        verbose_name_plural = "01. Invoices"

class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    product_quantity = models.IntegerField()
    product_price = models.FloatField()
    def __str__(self):
        return f"{self.product.product_title} x {self.product_quantity}"

class Receipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    paid_amount  = models.FloatField()
    payment_method = models.CharField(max_length=255)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    payment_receipt = models.FileField(upload_to="receipts",null = True, blank = True)
    created_by = models.CharField(max_length = 255, null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.client_name
    
    class Meta:
        verbose_name_plural = "02. Receipts"

class Statement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
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


class ExpenseType(models.Model):
    expense_type=models.CharField(max_length=199)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.expense_type
    class Meta:
        verbose_name_plural = "04. Expense Type"


class Expense(models.Model):
    expense_title = models.TextField()
    expense_amount  = models.FloatField()
    expense_type  = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL,null=True,blank=True)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.expense_title
    
    class Meta:
        verbose_name_plural = "04. Expense"
