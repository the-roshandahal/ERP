from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Statement)
admin.site.register(Invoice)
admin.site.register(Receipt)
admin.site.register(ExpenseType)
admin.site.register(Expense)
