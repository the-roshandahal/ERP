from django.shortcuts import render,redirect
from .models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *

from account.context_processors import custom_data_views
# Create your views here.

def crm_setup(request):
    if 'read_leads' in custom_data_views(request):
        lead_stage = LeadStage.objects.all()
        lead_source = LeadSource.objects.all()
        context = {
            'lead_source':lead_source,
            'lead_stage':lead_stage,
        }
        return render (request,'leads/crm_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_stage(request):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_stage = request.POST['lead_stage']
            LeadStage.objects.create(stage=lead_stage)
            messages.info(request, "Lead Stage Created Successfully.")
            return redirect('crm_setup')
        else:
            return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_stage(request,id):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_stage = request.POST['lead_stage']
            lead = LeadStage.objects.get(id=id)
            lead.stage = lead_stage
            lead.save()
            messages.info(request, "Lead Stage Updated Successfully.")
            return redirect('crm_setup')
        else:
            stage = LeadStage.objects.get(id=id)
            context={
                'stage':stage
            }
            return render(request,'leads/edit_stage.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_stage(request,id):
    if 'delete_leads' in custom_data_views(request):
        stage_data = LeadStage.objects.get(id=id)
        deleted_role = stage_data.stage
        stage_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_source(request):
    if 'create_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_source = request.POST['lead_source']
            LeadSource.objects.create(source=lead_source)
            messages.info(request, "Lead Source Created Successfully.")
            return redirect('crm_setup')
        else:
            return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_source(request,id):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_source = request.POST['lead_source']
            lead = LeadSource.objects.get(id=id)
            lead.source = lead_source
            lead.save()
            messages.info(request, "Lead Source Updated Successfully.")
            return redirect('crm_setup')
        else:
            source = LeadSource.objects.get(id=id)
            context={
                'source':source
            }
            return render(request,'leads/edit_source.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
      
def delete_source(request,id):
    if 'delete_leads' in custom_data_views(request):
        source_data = LeadSource.objects.get(id=id)
        deleted_role = source_data.source
        source_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def leads(request):
    if 'read_leads' in custom_data_views(request):
        leads = Leads.objects.filter(active=1).order_by('-created')
        closed_leads = Leads.objects.filter(active=0).order_by('-created')
        stage = LeadStage.objects.all()
        source = LeadSource.objects.all()

        filtered_users = Employee.objects.all()

        assign_to_user = []
        for filtered_users in filtered_users:
            if (filtered_users.permission.create_leads or filtered_users.permission.read_leads or 
                filtered_users.permission.update_leads or filtered_users.permission.delete_leads):
                assign_to_user.append(filtered_users.id)
        all_users = Employee.objects.all()

        data_list=[]
        
        for all_users in all_users:
            if all_users.id in assign_to_user:
                
                data_list.append({
                    'user': all_users,
                })
        if request.user.is_superuser:
            context = {
                'leads':leads,
                'closed_leads':closed_leads,
                'source':source,
                'stage':stage,
                'data_list':data_list,
            }
            return render (request,'leads/leads.html',context)
        else:
            logged_in_user = User.objects.get(username=request.user)
            company_user = Employee.objects.get(user=logged_in_user)
            my_leads = Leads.objects.filter(active=1,assigned_to = company_user).order_by('-created')

            context = {
                'leads':leads,
                'closed_leads':closed_leads,
                'my_leads':my_leads,
                'source':source,
                'stage':stage,
                'data_list':data_list,
            }
            return render (request,'leads/leads.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_lead(request):
    if 'create_leads' in custom_data_views(request):
        if request.method =="POST":
            title = request.POST['title']
            lead_name = request.POST['lead_name']
            email = request.POST['email']
            address = request.POST['address']
            company_name = request.POST['company_name']
            source = request.POST['source']
            stage = request.POST['stage']
            assigned_to = request.POST.getlist("assigned_to")
            contact = request.POST['contact']

            lead_stage = LeadStage.objects.get(stage=stage)
            lead_source = LeadSource.objects.get(source=source)
            
            lead = Leads.objects.create(title=title,lead_name=lead_name,email=email,address=address,
            company_name=company_name,source=lead_source,stage=lead_stage,contact=contact,active=1)
            lead.assigned_to.set(assigned_to)
            lead.save()
            user = User.objects.get(username=request.user)
            changed_by = user.username
            lead = Leads.objects.filter(id=lead.id)[0]
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=f'Added {title}')
            messages.info(request, "Lead Added")

            return redirect(leads)
        else:
            return redirect(leads)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_lead(request,id):
    if 'delete_leads' in custom_data_views(request):
        lead = Leads.objects.get(id=id)
        lead.delete()
        messages.info(request, "Lead Deleted")
        return redirect('leads')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def view_lead(request,id):
    if 'read_leads' in custom_data_views(request):
        lead = Leads.objects.get(id=id)
        lead_calls = LeadCall.objects.filter(lead=id)
        lead_activity = LeadLog.objects.filter(lead=id)
        lead_notes = LeadNotes.objects.filter(leads_id=id)
        lead_files = LeadFiles.objects.filter(leads_id=id)

        stage = LeadStage.objects.all()
        source = LeadSource.objects.all()
        filtered_users = Employee.objects.all()

        assign_to_user = []
        for filtered_users in filtered_users:
            if (filtered_users.permission.create_leads or filtered_users.permission.read_leads or 
                filtered_users.permission.update_leads or filtered_users.permission.delete_leads):
                assign_to_user.append(filtered_users.id)
        all_users = Employee.objects.all()

        data_list=[]
        for all_users in all_users:
            if all_users.id in assign_to_user:
                data_list.append({
                    'user': all_users,
                })


        context = {
            'lead':lead,
            'stage':stage,
            'source':source,
            'lead_activity':lead_activity,
            'data_list':data_list,
            'lead_calls':lead_calls,
            'lead_notes':lead_notes,
            'lead_files':lead_files
        }
        return render(request,'leads/view_lead.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def update_users(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.method =='POST':
            assigned_to = request.POST.getlist("assigned_to")
            lead = Leads.objects.get(id=id)
            lead.assigned_to.set(assigned_to)
            lead.save()
            messages.info(request, "Users updated successfully.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'updated users'
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)


            return redirect(view_lead,id)
        else:
            return redirect(view_lead,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def add_note(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            note = request.POST['note']
            user = User.objects.get(username=request.user)
            changed_by = user.username

            lead = Leads.objects.filter(id=id)[0]

            LeadNotes.objects.create(leads=lead, notes=note)
            
            messages.info(request, "Note Added Successfully")

            activity = ' added note ' + note
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
            return redirect(view_lead,id)
        else:
            assigned_lead = Leads.objects.get(id=id)
            lead_assigned_users=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for lead_assigned_users in lead_assigned_users:
                if str(lead_assigned_users) == str(employees):
                    assigned=True
            
            if (assigned == True):
                if request.method =='POST':
                    note = request.POST['note']
                    user = User.objects.get(username=request.user)
                    changed_by = user.username

                    lead = Leads.objects.filter(id=id)[0]

                    LeadNotes.objects.create(leads=lead, notes=note)
                    
                    messages.info(request, "Note Added Successfully")

                    activity = ' added note ' + note
                    LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
                    return redirect(view_lead,id)
                else:
                    return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)

    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    




def add_call(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            purpose = request.POST['purpose']
            duration = request.POST['duration']
            summary = request.POST['summary']
            user = User.objects.get(username=request.user)
            called_by = user.username

            lead = Leads.objects.get(id=id)
            LeadCall.objects.create(lead=lead,purpose=purpose,duration=duration,summary=summary,called_by=called_by)
            messages.info(request, "Call Added Successfully")

            LeadLog.objects.create(lead=lead,changed_by=called_by,activity='added call data')
            return redirect(view_lead,id)
        else:
            
            assigned_lead = Leads.objects.get(id=id)
            lead_assigned_users=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for lead_assigned_users in lead_assigned_users:
                if str(lead_assigned_users) == str(employees):
                    assigned=True
            
            if (assigned == True):
                if request.method =='POST':
                    purpose = request.POST['purpose']
                    duration = request.POST['duration']
                    summary = request.POST['summary']
                    user = User.objects.get(username=request.user)
                    called_by = user.username

                    lead = Leads.objects.get(id=id)
                    LeadCall.objects.create(lead=lead,purpose=purpose,duration=duration,summary=summary,called_by=called_by)
                    messages.info(request, "Call Added Successfully")

                    LeadLog.objects.create(lead=lead,changed_by=called_by,activity='added call data')
                    return redirect(view_lead,id)
                else:
                    return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)

    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def add_file(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            if request.method =='POST':
                title = request.POST['title']
                file = request.FILES['file']
            
                user = User.objects.get(username=request.user)
                added_by = user.username

                lead = Leads.objects.get(id=id)
                LeadFiles.objects.create(leads=lead,title=title,file=file,added_by=added_by)
                messages.info(request, "File Added Successfully")

                LeadLog.objects.create(lead=lead,changed_by=added_by,activity='added file data')
                return redirect(view_lead,id)
            else:
                return redirect(view_lead,id)
        else:
            assigned_lead = Leads.objects.get(id=id)
            lead_assigned_users=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for lead_assigned_users in lead_assigned_users:
                if str(lead_assigned_users) == str(employees):
                    assigned=True
            
            if (assigned == True):
                if request.method =='POST':
                    title = request.POST['title']
                    file = request.FILES['file']
                
                    user = User.objects.get(username=request.user)
                    added_by = user.username

                    lead = Leads.objects.get(id=id)
                    LeadFiles.objects.create(leads=lead,title=title,file=file,added_by=added_by)
                    messages.info(request, "File Added Successfully")

                    LeadLog.objects.create(lead=lead,changed_by=added_by,activity='added file data')
                    return redirect(view_lead,id)
                else:
                    return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)

    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

 
def update_lead_status(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            if request.method =='POST':
                stage = request.POST['stage']
                lead_stage = LeadStage.objects.get(id=stage)

                user = User.objects.get(username=request.user)
                changed_by = user.username

                lead = Leads.objects.filter(id=id)[0]
                lead.stage = lead_stage
                lead.save()
                messages.info(request, "Lead stage updated")
                activity = 'updated lead stage to '+str(lead_stage)
                LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
                return redirect(view_lead,id)
            else:
                return redirect(view_lead,id)
        else:
            assigned_lead = Leads.objects.get(id=id)
            assignedddd=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for assignedddd in assignedddd:
                if str(assignedddd) == str(employees):
                    assigned=True
            
            if assigned == True:
                if request.method =='POST':
                    stage = request.POST['stage']
                    lead_stage = LeadStage.objects.get(id=stage)

                    user = User.objects.get(username=request.user)
                    changed_by = user.username

                    lead = Leads.objects.filter(id=id)[0]
                    lead.stage = lead_stage
                    lead.save()
                    messages.info(request, "Lead stage updated")
                    activity = 'updated lead stage to '+str(lead_stage)
                    LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
                    return redirect(view_lead,id)
                else:
                    return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def edit_lead(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.method == 'POST':
            source=request.POST['source']
            lead_data = Leads.objects.get(id=id)
            lead_source = LeadSource.objects.get(source=source)
            lead_data.title = request.POST.get("title")
            lead_data.lead_name = request.POST.get("lead_name")
            lead_data.email = request.POST.get("email")
            lead_data.address = request.POST.get("address")
            lead_data.company_name = request.POST.get("company_name")
            lead_data.source = lead_source
            lead_data.contact = request.POST.get("contact")
            lead_data.save()
            messages.info(request, "Lead Edited Successfully.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            lead = Leads.objects.filter(id=id)[0]
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=' edited lead details ')
            return redirect(view_lead,id)
        else:
            return redirect(view_lead,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def close_lead(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            lead = Leads.objects.get(id=id)
            lead.active=0
            lead.save()
            messages.info(request, "Lead closed.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' closed lead '
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
            return redirect(view_lead,id)
        else:
            assigned_lead = Leads.objects.get(id=id)
            assignedddd=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for assignedddd in assignedddd:
                if str(assignedddd) == str(employees):
                    assigned=True
            
            if assigned == True:
                lead = Leads.objects.get(id=id)
                lead.active=0
                lead.save()
                messages.info(request, "Lead closed.")

                user = User.objects.get(username=request.user)
                changed_by = user.username
                activity = ' closed lead '
                LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
                return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def reopen_lead(request,id):
    if 'update_leads' in custom_data_views(request):
        if request.user.is_superuser:
            lead = Leads.objects.get(id=id)
            lead.active=1
            lead.save()
            messages.info(request, "Lead reopened.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' reopened lead '
            LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
            return redirect(view_lead,id)
        else:
            assigned_lead = Leads.objects.get(id=id)
            assignedddd=assigned_lead.assigned_to.all()
            logged_in_user = User.objects.get(username=request.user)
            employees = Employee.objects.get(user=logged_in_user)

            assigned=False
            for assignedddd in assignedddd:
                if str(assignedddd) == str(employees):
                    assigned=True
            
            if assigned == True:
                lead = Leads.objects.get(id=id)
                lead.active=1
                lead.save()
                messages.info(request, "Lead reopened.")

                user = User.objects.get(username=request.user)
                changed_by = user.username
                activity = ' reopened lead '
                LeadLog.objects.create(lead=lead,changed_by=changed_by,activity=activity)
                return redirect(view_lead,id)
            else:
                messages.info(request, "You are not assigned to this lead.")
                return redirect(view_lead,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest
# from django.http import HttpResponse
# import requests
# import json
 
# @csrf_exempt
def facebook_leads_callback(request):
    pass
#     if request.method == 'POST':
#         print('hello')
#         # Define your Facebook app credentials
#         facebook_app_id = '1628117010947627'
#         facebook_app_secret = 'de2a509c315fdc852b2c51ce9392f1dd'
#         facebook_access_token = 'dbe96db68e6b9d6e51bbaf63eb8d61b3'

#         # Get the lead data from the callback
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             leadgen_id = data['entry'][0]['changes'][0]['value']['leadgen_id']
#         except (KeyError, ValueError):
#             return HttpResponseBadRequest()

#         # Verify the authenticity of the request
#         signed_request = data['entry'][0]['changes'][0]['value']['signed_request']
#         expected_signature = hmac.new(
#             facebook_app_secret.encode('utf-8'),
#             signed_request.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         encoded_sig, payload = signed_request.split('.', 1)
#         decoded_payload = base64.urlsafe_b64decode(
#             payload + '=' * (4 - len(payload) % 4)
#         ).decode('utf-8')
#         decoded_payload = json.loads(decoded_payload)
#         if decoded_payload.get('algorithm').upper() != 'HMAC-SHA256':
#             return HttpResponseBadRequest()
#         if encoded_sig != expected_signature:
#             return HttpResponseBadRequest()

#         # Retrieve the lead information using the Graph API
#         api_url = 'https://graph.facebook.com/v12.0/' + leadgen_id + '?fields=full_name,email,phone_number'
#         request_url = api_url + '&access_token=' + facebook_access_token
#         response = requests.get(request_url)
#         lead_info = response.json()

#         # Save the lead information to your database
#         full_name = lead_info.get('full_name')
#         email = lead_info.get('email')
#         phone_number = lead_info.get('phone_number')
#         if full_name and email and phone_number:
#             lead = Leads.objects.create(lead_name=full_name, email=email, contact=phone_number)
#             lead.save()

#         # Send a response back to Facebook
#         return HttpResponse('Lead information saved successfully.')
#     else:
#         return HttpResponseBadRequest()