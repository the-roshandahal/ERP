from django.shortcuts import render,redirect
from .models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from features.views import *
# Create your views here.

def check_permission(request):
    logged_in_user = User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    role=Role.objects.get(role=user.permission)
    permission=Permission.objects.get(role=role)
    permissions = []

    if permission.create_leads:
        permissions.append('create')
    if permission.read_leads:
        permissions.append('read')
    if permission.update_leads:
        permissions.append('update')
    if permission.delete_leads:
        permissions.append('delete')
    return permissions

def stage(request):
    if 'read' in check_permission(request):
        lead_stage = LeadStage.objects.all()
        context = {
            'lead_stage':lead_stage,
        }
        return render (request,'leads/stage.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

def create_stage(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            lead_stage = request.POST['lead_stage']
            LeadStage.objects.create(stage=lead_stage)
            messages.info(request, "Lead Stage Created Successfully.")
            return redirect('stage')
        else:
            return redirect('stage')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    
def delete_stage(request,id):
    if 'delete' in check_permission(request):
        stage_data = LeadStage.objects.get(id=id)
        deleted_role = stage_data.stage
        stage_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('stage')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

def source(request):
    if 'create' in check_permission(request):
        lead_source = LeadSource.objects.all()
        context = {
            'lead_source':lead_source,
        }
        return render (request,'leads/source.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def create_source(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            lead_source = request.POST['lead_source']
            LeadSource.objects.create(source=lead_source)
            messages.info(request, "Lead Source Created Successfully.")
            return redirect('source')
        else:
            return redirect('source')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

   
def delete_source(request,id):
    if 'delete' in check_permission(request):
        source_data = LeadSource.objects.get(id=id)
        deleted_role = source_data.source
        source_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('source')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def leads(request):
    if 'read' in check_permission(request):
        leads = Leads.objects.filter(active=1).order_by('-created')
        stage = LeadStage.objects.all()
        source = LeadSource.objects.all()
        filtered_users = CompanyUser.objects.all()

        assign_to_user = []
        for filtered_users in filtered_users:
            if (filtered_users.permission.create_leads or filtered_users.permission.read_leads or 
                filtered_users.permission.update_leads or filtered_users.permission.delete_leads):
                assign_to_user.append(filtered_users.id)
        all_users = CompanyUser.objects.all()

        data_list=[]
        for all_users in all_users:
            if all_users.id in assign_to_user:
                
                data_list.append({
                    'user': all_users,
                })
        print(data_list)
        context = {
            'leads':leads,
            'leads':leads,
            'source':source,
            'stage':stage,
            'data_list':data_list,
        }
        return render (request,'leads/leads.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


































# def create_leads(request, file_name):
#     df = pd.read_csv(file_name, delimiter=',')
#     print(df)
#     lead_list = [list(row) for row in df.values]
#     for l in lead_list:
#         # Leads.objects.create(title=l[0],lead_name=l[1],email=l[2],address=l[3],company_name=l[4],source=l[5],contact=l[6])
#         try:
#             Leads.objects.create(title=l[0],lead_name=l[1],email=l[2],address=l[3],company_name=l[4],source=l[5],contact=l[6])
#             messages.info(request, "Leads Uploaded.")
#         except:
#             messages.info(request, "Invalid File Format.")

    


# def upload_leads(request):
#     if request.user.is_staff:
#         if request.method =="POST":
#             file = request.FILES['file']
#             lead_file=LeadFile.objects.create(file=file)
            
#             create_leads(request, lead_file.file)
#             lead_file.save()
#             return redirect(leads)
#         else:
#             return redirect(leads)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)


# def add_lead(request):
#     if request.user.is_staff:
#         if request.method =="POST":
#             title = request.POST['title']
#             lead_name = request.POST['lead_name']
#             email = request.POST['email']
#             address = request.POST['address']
#             company_name = request.POST['company_name']
#             source = request.POST['source']
#             notes = request.POST['notes']
#             stage = request.POST['stage']
#             assigned_to = request.POST.getlist("assigned_to")
#             contact = request.POST['contact']


#             lead = Leads.objects.create(title=title,lead_name=lead_name,email=email,address=address,
#             company_name=company_name,source=source,stage=stage,contact=contact,active=1)
#             lead.assigned_to.set(assigned_to)
#             lead.save()
#             LeadNotes.objects.create(leads=lead,notes=notes,)
#             return redirect(leads)
#         else:
#             return redirect(leads)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)



# def delete_lead(request,id):
#     if request.user.is_staff:
#         if request.user.is_superuser:
#             lead = Leads.objects.get(id=id)
#             lead.delete()
#             return redirect(leads)
#         else:
#             messages.info(request, "Unauthorized access.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)

# def view_lead(request,id):
#     if request.user.is_staff:
#         lead = Leads.objects.get(id=id)
#         call_data = LeadCall.objects.filter(lead=id)
#         activity = LeadLog.objects.filter(lead=id)
#         stage = LeadStage.objects.all()
#         users = User.objects.filter(is_staff=True)
#         notes = LeadNotes.objects.filter(leads_id=id)
#         context = {
#             'lead':lead,
#             'stage':stage,
#             'activity':activity,
#             'users':users,
#             'call_data':call_data,
#             'notes':notes
#         }
#         return render(request,'view_lead.html',context)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)

# def add_call(request,id):
#     if request.user.is_staff:
#         assigned_lead = Leads.objects.get(id=id)
#         assignedddd=assigned_lead.assigned_to.all()
#         logged_in_user = User.objects.get(username=request.user)

#         assigned=False
#         for assignedddd in assignedddd:
#             if assignedddd == logged_in_user:
#                 assigned=True
        
#         if assigned == True:
#             if request.method =='POST':
#                 purpose = request.POST['purpose']
#                 duration = request.POST['duration']
#                 summary = request.POST['summary']
#                 user = User.objects.get(username=request.user)
#                 called_by = user.username

#                 lead = Leads.objects.get(id=id)
#                 LeadCall.objects.create(lead=lead,purpose=purpose,duration=duration,summary=summary,called_by=called_by)
#                 LeadLog.objects.create(lead=lead,changed_by=called_by,activity='added call data')
#                 return redirect(view_lead,id)
#             else:
#                 return redirect(view_lead,id)
#         else:
#             messages.info(request, "You are not assigned to this lead.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)

# def update_lead_status(request,id):
#     if request.user.is_staff:
#         assigned_lead = Leads.objects.get(id=id)
#         assignedddd=assigned_lead.assigned_to.all()
#         logged_in_user = User.objects.get(username=request.user)

#         assigned=False
#         for assignedddd in assignedddd:
#             if assignedddd == logged_in_user:
#                 assigned=True
        
#         if assigned == True:
#             if request.method =='POST':
#                 status = request.POST['status']
#                 user = User.objects.get(username=request.user)
#                 changed_by = user.username

#                 lead = Leads.objects.filter(id=id)[0]
#                 lead.stage = status
#                 lead.save()
#                 messages.info(request, "Lead status updated")
#                 activity = 'updated lead status to '+status
#                 LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
#                 return redirect(view_lead,id)
#             else:
#                 return redirect(view_lead,id)
#         else:
#             messages.info(request, "You are not assigned to this lead.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)



# def update_users(request,id):
#     if request.user.is_staff:
#         if request.method =='POST':
#             assigned_to = request.POST.getlist("assigned_to")
#             lead = Leads.objects.get(id=id)
#             lead.assigned_to.set(assigned_to)
#             lead.save()
#             messages.info(request, "Lead status updated")


#             user = User.objects.get(username=request.user)
#             changed_by = user.username
#             activity = 'updated users'
#             LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)


#             return redirect(view_lead,id)
#         else:
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(view_lead,id)
# def add_note(request,id):
#     if request.user.is_staff:
#         assigned_lead = Leads.objects.get(id=id)
#         assignedddd=assigned_lead.assigned_to.all()
#         logged_in_user = User.objects.get(username=request.user)

#         assigned=False
#         for assignedddd in assignedddd:
#             if assignedddd == logged_in_user:
#                 assigned=True
        
#         if assigned == True:
#             if request.method =='POST':
#                 note = request.POST['note']
#                 user = User.objects.get(username=request.user)
#                 changed_by = user.username

#                 lead = Leads.objects.filter(id=id)[0]

#                 LeadNotes.objects.create(leads=lead, notes=note)
                
#                 messages.info(request, "Note Added Successfully")

#                 activity = ' added note ' + note
#                 LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
#                 return redirect(view_lead,id)
#             else:
#                 return redirect(view_lead,id)
#         else:
#             messages.info(request, "You are not assigned to this lead.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)


# def edit_lead(request,id):
#     if request.user.is_staff:
#         if request.method =='POST':
#             title = request.POST.get("title")
#             lead_name = request.POST.get("lead_name")
#             email = request.POST.get("email")
#             address = request.POST.get("address")
#             company_name = request.POST.get("company_name")
#             source = request.POST.get("contact")
#             contact = request.POST.get("contact")
            
#             lead_data = Leads.objects.get(id=id)
#             lead_data.title = title
#             lead_data.lead_name = lead_name
#             lead_data.email = email
#             lead_data.address = address
#             lead_data.company_name = company_name
#             lead_data.source = source
#             lead_data.contact = contact
#             lead_data.save()

#             user = User.objects.get(username=request.user)
#             changed_by = user.username
#             lead = Leads.objects.filter(id=id)[0]

            
#             messages.info(request, "Lead Edited Successfully.")

#             activity = ' edited lead details '
#             LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
#             return redirect(view_lead,id)
#         else:
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)


# def close_lead(request,id):
#     if request.user.is_staff:
#         assigned_lead = Leads.objects.get(id=id)
#         assignedddd=assigned_lead.assigned_to.all()
#         logged_in_user = User.objects.get(username=request.user)

#         assigned=False
#         for assignedddd in assignedddd:
#             if assignedddd == logged_in_user:
#                 assigned=True
        
#         if assigned == True:
#             lead = Leads.objects.get(id=id)
#             lead.active=0
#             lead.save()
#             messages.info(request, "Lead closed.")

#             user = User.objects.get(username=request.user)
#             changed_by = user.username
#             activity = ' closed lead '
#             LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
#             return redirect(view_lead,id)
#         else:
#             messages.info(request, "You are not assigned to this lead.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)



# def reopen_lead(request,id):
#     if request.user.is_staff:
#         assigned_lead = Leads.objects.get(id=id)
#         assignedddd=assigned_lead.assigned_to.all()
#         logged_in_user = User.objects.get(username=request.user)

#         assigned=False
#         for assignedddd in assignedddd:
#             if assignedddd == logged_in_user:
#                 assigned=True
        
#         if assigned == True:
#             lead = Leads.objects.get(id=id)
#             lead.active=1
#             lead.save()
#             messages.info(request, "Lead reopened.")

#             user = User.objects.get(username=request.user)
#             changed_by = user.username
#             activity = ' reopened lead '
#             LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
#             return redirect(view_lead,id)
#         else:
#             messages.info(request, "You are not assigned to this lead.")
#             return redirect(view_lead,id)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect(home)