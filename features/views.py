from datetime import date,datetime
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
from customer.models import *
from django.utils import timezone
from account.context_processors import *
import json
import urllib.parse
import urllib.request

def homepage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        return render (request,'homepage.html')

def home(request):
    if request.user.is_authenticated:
        return render (request,'index.html') 
    else:
        return redirect('login')
    

def add_company_setup(request):
    if 'manage_company' in custom_data_views(request):
        if Company.objects.all().exists():
            messages.info(request, "You have already added a setup.")
            return redirect('company_setup')
        else:
            if request.method=='POST':
                company_name = request.POST['company_name']
                company_address = request.POST['company_address']
                company_email = request.POST['company_email']
                company_contact_number = request.POST['company_contact_number']
                company_logo = request.FILES['company_logo']
                payment_terms = request.POST['payment_terms']
                payment_details = request.POST['payment_details']

                Company.objects.create(company_name = company_name,company_address = company_address,
                                    company_email = company_email,company_contact_number = company_contact_number,company_logo = company_logo,
                                    payment_terms = payment_terms,payment_details = payment_details)
                return redirect('company_setup')
            else:
                return render(request,'features/add_company_setup.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def edit_company_setup(request,id):
    if 'manage_company' in custom_data_views(request):
        if request.method=='POST':
            setup = Company.objects.get(id=id)
            setup.company_name = request.POST['company_name']
            setup.company_address = request.POST['company_address']
            setup.company_email = request.POST['company_email']
            setup.company_contact_number = request.POST['company_contact_number']
            setup.payment_terms = request.POST['payment_terms']
            setup.payment_details = request.POST['payment_details']

            if request.FILES and request.FILES['company_logo']:
                setup.company_logo = request.FILES['company_logo']
            setup.save()
            return redirect('company_setup')
        else:
            setup = Company.objects.get(id=id)
            print(setup.company_name)
            context = {
            'setup':setup
            }
            return render(request,'features/edit_company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def todo(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users = Employee.objects.all()
            context = {
                'users':users,
            }
            return render (request, 'features/todo.html',context)
        else:
            logged_in_user = User.objects.get(username=request.user)
            company_user = Employee.objects.get(user=logged_in_user)
            done_todo = ToDo.objects.filter(task_to = company_user, status = 'done').order_by('priority')
            undone_todo = ToDo.objects.filter(task_to = company_user, status = 'incomplete')
            reassigned_todo = ToDo.objects.filter(task_to = company_user, status = 'reassigned')
            mytasks = ToDo.objects.filter(task_from= company_user)
            
            users = Employee.objects.all()

            context = {
                'reassigned_todo':reassigned_todo,
                'done_todo':done_todo,
                'undone_todo':undone_todo,
                'mytasks':mytasks,
                'users':users,
            }
            return render (request, 'features/todo.html',context)


def add_todo(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.info(request, "Superuser can't add tasks. Please use your employee account to continue.")

            return redirect(todo)
        else:
            if request.method == "POST":
                task = request.POST["task"]
                deadline = request.POST["deadline"]
                priority = request.POST["priority"]
                assign_to = request.POST.getlist("selected")


                logged_in_user = User.objects.get(username=request.user)
                task_from = Employee.objects.get(user=logged_in_user)
                for assign_to in assign_to:
                    assign_to = Employee.objects.get(id=assign_to)
                    ToDo.objects.create(task=task,deadline=deadline,priority=priority,task_to=assign_to,task_from=task_from)
                return redirect(todo)
            return redirect (todo)


def change_status(request,id):
    if request.user.is_authenticated:
        todo_data = ToDo.objects.get(id=id)
        if todo_data.status == 'incomplete':
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "done"
            status_update.save()
            messages.info(request, "Status Changed to Done")
            return redirect(todo)

        elif todo_data.status =='reassigned':
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "done"
            status_update.save()
            messages.info(request, "Status Changed to Done")
            return redirect(todo)

        else:
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "incomplete"
            status_update.save()
            messages.info(request, "Status Changed to Incomplete")
            return redirect(todo)

def reassign(request,id):
    if request.user.is_authenticated:
        status_update = ToDo.objects.filter(id=id)[0]
        status_update.status = "reassigned"
        status_update.save()
        messages.info(request, "Status Changed to Resassigned")
        return redirect(todo)


def company_setup(request):
    if 'manage_company' in custom_data_views(request):
        company_setup= Company.objects.all().order_by('-created').first()
        credentials= Credentials.objects.all().order_by('-created').first()
        context = {
            'company_setup':company_setup,
            'credentials':credentials
        }
        return render (request,'features/company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    















def add_company_credentials(request):
    if 'manage_company' in custom_data_views(request):
        if Credentials.objects.all().exists():
            messages.info(request, "You have already added credentials.")
            return redirect('company_setup')
        else:
            if request.method=='POST':
                host = request.POST['host']
                port = request.POST['port']
                email = request.POST['email']
                password = request.POST['password']
                api_key = request.POST['api_key']
                campaign = request.POST['campaign']
                route = request.POST['route']

                Credentials.objects.create(host = host,port = port,
                                    email = email,password = password,api_key = api_key,
                                    campaign = campaign,route=route)
                return redirect('company_setup')
            else:
                return render(request,'features/add_company_credentials.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def edit_company_credentials(request,id):
    if 'manage_company' in custom_data_views(request):
        if request.method=='POST':
            credentials = Credentials.objects.get(id=id)

            credentials.host = request.POST['host']
            credentials.port = request.POST['port']
            credentials.email = request.POST['email']
            credentials.password = request.POST['password']

            credentials.api_key = request.POST['api_key']
            credentials.campaign = request.POST['campaign']
            credentials.route = request.POST['route']
            credentials.save()
            return redirect('company_setup')
        else:
            credentials = Credentials.objects.get(id=id)
            context = {
            'credentials':credentials
            }
            return render(request,'features/edit_company_credentials.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def send_message(request):
    if request.method == "POST":
        number = request.POST['number']
        message = request.POST['message']
        credentials = Credentials.objects.all().order_by('-created').first()

        api_key = f'{credentials.api_key}'
        route_id = f'{credentials.route}'
        campaign = f'{credentials.campaign}'
        contacts = f'{number}'
        sms_text = f'{message}'

        api_url = "https://spellcpaas.com/api/smsapi"
        
        # Prepare the data for the request body
        data = {
            'key': api_key,
            'campaign': campaign,
            'routeid': route_id,
            'type': 'text',
            'contacts': contacts,
            'msg': sms_text
        }
        
        # Encode the data as JSON
        encoded_data = json.dumps(data).encode('utf-8')
        
        # Prepare the request
        req = urllib.request.Request(api_url, data=encoded_data, method='POST')
        
        # Set the content type header
        req.add_header('Content-Type', 'application/json')
        
        # Submit the request
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            print(response_text)
        
        return redirect("send_message")
    else:
        return render(request,'features/send_message.html')





def message_emp_client(request):
    if request.method == "POST":
        message = request.POST['message']
        send_to = request.POST['send_to']
        credentials = Credentials.objects.all().order_by('-created').first()

        api_key = f'{credentials.api_key}'
        route_id = f'{credentials.route}'
        campaign = f'{credentials.campaign}'
        
        if send_to == 'employees':
            employees = Employee.objects.all()
            contact_numbers = [employee.contact for employee in employees]
            contacts = ",".join(contact_numbers)

        elif send_to == 'client':
            clients = Customer.objects.all()
            contact_numbers = [client.contact for client in clients]
            contacts = ",".join(contact_numbers)
        else:
            contacts =''
        sms_text = f'{message}'

        api_url = "https://spellcpaas.com/api/smsapi"
        
        data = {
            'key': api_key,
            'campaign': campaign,
            'routeid': route_id,
            'type': 'text',
            'contacts': contacts,
            'msg': sms_text
        }
        
        encoded_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(api_url, data=encoded_data, method='POST')
        
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            print(response_text)
        
        return redirect("message_emp_client")
    else:
        return render (request,'features/message_emp_client.html')