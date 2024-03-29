from django.db import models

# Create your models here.



class ProductCategory(models.Model):
    product_category = models.CharField(max_length=255)
    def __str__(self):
        return self.product_category
    class Meta:
        verbose_name_plural = "02. Products Category"


class ProductUnit(models.Model):
    product_unit = models.CharField(max_length=255)
    def __str__(self):
        return self.product_unit
    class Meta:
        verbose_name_plural = "03. Products Unit"

# class Product(models.Model):
#     product_type = models.CharField(max_length=255)
#     product_title = models.CharField(max_length=255)
#     product_batch = models.CharField(max_length=255, blank=True, null=True)
#     product_price = models.FloatField()
#     product_quantity = models.IntegerField(null = True, blank = True)
#     product_description = models.TextField(null = True, blank = True)
#     product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True,)
#     product_unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, blank=True, null=True,)
#     is_vatable = models.BooleanField(default=True)
#     def __str__(self):
#         return self.product_title
#     class Meta:
#         verbose_name_plural = "01. Products" 
# 
# 


class Product(models.Model):
    product_title = models.CharField(max_length=255)
    product_description = models.TextField(null = True, blank = True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True,)
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, blank=True, null=True,)
    is_vatable = models.BooleanField(default=True)
    def __str__(self):
        return self.product_title
    
    class Meta:
        verbose_name_plural = "01. Products"      

class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_batch = models.CharField(max_length=255, blank=True, null=True)
    product_quantity = models.IntegerField(null = True, blank = True)
    product_price = models.FloatField()
    purchase_price = models.FloatField()

    def __str__(self):
        return self.product_batch
    
    class Meta:
        verbose_name_plural = "01. Product Batch"





class Service(models.Model):
    service_title = models.CharField(max_length=255)
    service_price = models.FloatField()
    service_description = models.TextField(null = True, blank = True)
    service_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True,)
    service_unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, blank=True, null=True,)
    is_vatable = models.BooleanField(default=True)

    def __str__(self):
        return self.service_title
    class Meta:
        verbose_name_plural = "01. Services" 
class ProductStatement(models.Model):
    batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    remarks = models.TextField()
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
    class Meta:
        verbose_name_plural = "10. Product Statement"