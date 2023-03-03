from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Leads)
admin.site.register(LeadCall)
admin.site.register(LeadNotes)
admin.site.register(LeadLog)
admin.site.register(LeadFiles)