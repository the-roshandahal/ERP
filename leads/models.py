# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# class LeadFile(models.Model):
#     file = models.FileField(upload_to='leads')

#     def __str__(self):
#         return self.file

#     class Meta:
#         verbose_name_plural = "01. Lead Files"



# class Leads(models.Model):
#     title = models.CharField(max_length=200,null=True, blank=True)
#     lead_name = models.CharField(max_length=200,null=True, blank=True)
#     email = models.CharField(max_length=200,null=True, blank=True)
#     contact = models.CharField(max_length=200,null=True, blank=True)
#     address = models.CharField(max_length=200,null=True, blank=True)
#     company_name = models.CharField(max_length=200,null=True, blank=True)
#     source = models.CharField(max_length=200,null=True, blank=True)
#     stage = models.CharField(max_length=100,null=True, blank=True)
#     assigned_to = models.ManyToManyField(User)
#     active = models.BooleanField(default=1)
#     date_modified = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = "01. Leads"


# class LeadLog(models.Model):
#     lead = models.ForeignKey(Leads,on_delete=models.CASCADE)
#     changed_by = models.CharField(max_length=200)
#     activity = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.lead.lead_name

#     class Meta:
#         verbose_name_plural = "02. Activity Log"


# class LeadCall(models.Model):
#     lead = models.ForeignKey(Leads,on_delete=models.CASCADE)
#     purpose = models.CharField(max_length=200)
#     called_by = models.CharField(max_length=200)
#     duration = models.CharField(max_length=200)
#     summary = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.lead.lead_name

#     class Meta:
#         verbose_name_plural = "03. Lead Call"


# class LeadStage(models.Model):
#     stage = models.CharField(max_length=200)
#     def __str__(self):
#         return self.stage

#     class Meta:
#         verbose_name_plural = "04. Lead Stage"

# class LeadNotes(models.Model):
#     leads = models.ForeignKey(Leads,on_delete=models.CASCADE)
#     notes = models.TextField()
#     def __str__(self):
#         return self.leads.lead_name

#     class Meta:
#         verbose_name_plural = "05. Lead Notes"
