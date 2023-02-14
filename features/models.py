# from django.contrib.auth.models import User
# from django.db import models

# # Create your models here.

# class Package(models.Model):
#     package_name = models.CharField(max_length=255)
#     package_description = models.TextField(null = True, blank = True)
#     package_price = models.FloatField()
#     no_of_graphics = models.IntegerField(null = True, blank = True)
#     no_of_gif = models.IntegerField(null = True, blank = True)
#     boost_amount = models.IntegerField(null = True, blank = True)
#     def __str__(self):
#         return self.package_name
#     class Meta:
#         verbose_name_plural = "01. Packages"


# class Customer(models.Model):
#     client_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     email = models.EmailField()
#     contact = models.CharField(max_length=100)
#     def __str__(self):
#         return self.client_name
#     class Meta:
#         verbose_name_plural = "02. Clients"

# class Invoice(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     package = models.ForeignKey(Package, on_delete=models.CASCADE,null = True, blank = True)
#     misc_name = models.CharField(max_length=255,null = True, blank = True)
#     misc_amount = models.FloatField(null = True, blank = True)
#     deduction_name = models.CharField(max_length=100, null = True, blank = True)
#     deduction_amount = models.FloatField(null = True, blank = True)
#     discount = models.FloatField(null = True, blank = True)
#     vat_amount = models.FloatField(null = True, blank = True)
#     sub_total = models.FloatField()
#     vatable_amount = models.FloatField()
#     total = models.FloatField()
#     previous_due = models.FloatField(null = True, blank = True)
#     grand_total = models.FloatField(null = True, blank = True)
#     remarks = models.CharField(max_length = 255, null = True, blank = True)
#     created_by = models.CharField(max_length = 255, null = True, blank = True)
#     created = models.DateField(auto_now_add=True)
#     def __str__(self):
#         return self.customer.client_name

#     class Meta:
#         verbose_name_plural = "03. Invoices"

# PAYMENT_CHOICES = (('bank_transfer','bank_transfer'),('esewa','esewa'),('cash','cash'))
# class Receipt(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     payment_method = models.CharField( choices = PAYMENT_CHOICES, max_length=255)
#     paid_amount  = models.FloatField()
#     payment_receipt = models.FileField(upload_to="receipts",null = True, blank = True)
#     remarks = models.CharField(max_length = 255, null = True, blank = True)
#     created_by = models.CharField(max_length = 255, null = True, blank = True)
#     created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.customer.client_name
#     class Meta:
#         verbose_name_plural = "04. Receipts"

# class Statement(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     transaction = models.CharField(max_length=255)
#     details = models.CharField(max_length=255)
#     amount = models.FloatField(null = True, blank = True)
#     payment = models.FloatField(null = True, blank = True)
#     balance = models.FloatField(null = True, blank = True)
#     created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.customer.client_name

#     class Meta:
#         verbose_name_plural = "05. Statements"


# class Followup(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     followup_title = models.CharField(max_length=255,null = True, blank = True)
#     description = models.TextField(null = True, blank = True)
#     remarks = models.TextField(null = True, blank = True)
#     created_by = models.CharField(max_length = 255, null = True, blank = True)
#     created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.customer.client_name

#     class Meta:
#         verbose_name_plural = "06. Followup"


# class CPR(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     package = models.ForeignKey(Package, on_delete=models.CASCADE,null = True, blank = True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     def __str__(self):
#         return self.customer.client_name

#     class Meta:
#         verbose_name_plural = "07. CPR"



# class LogSheet(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     punch_in_time = models.TimeField()
#     punch_out_time = models.TimeField()
#     tasks = models.TextField()
#     meetings = models.TextField(null = True, blank = True)
#     remarks = models.TextField(null = True, blank = True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name_plural = "08. Log Sheet"


# class ToDo(models.Model):
#     date = models.DateTimeField(auto_now_add=True)
#     task = models.TextField()
#     deadline = models.TextField()
#     task_from = models.TextField()
#     task_to = models.ForeignKey(User, on_delete=models.CASCADE)
#     priority = models.TextField()
#     status = models.TextField(default = "incomplete")

#     def __str__(self):
#         return self.task_to.username

#     class Meta:
#         verbose_name_plural = "08. To Do"