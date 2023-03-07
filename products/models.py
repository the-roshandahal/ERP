from django.db import models

# Create your models here.
class Product(models.Model):
    product_type = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255)
    product_price = models.FloatField()
    product_quantity = models.IntegerField(null = True, blank = True)
    product_description = models.TextField(null = True, blank = True)
    def __str__(self):
        return self.product_title
    class Meta:
        verbose_name_plural = "01. Products"