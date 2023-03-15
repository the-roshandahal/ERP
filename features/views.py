from datetime import date,datetime
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
from django.utils import timezone
from account.context_processors import *

def home(request):
    if request.user.is_authenticated:
        return render (request,'index.html') 
    else:
        return redirect('login')

def todo(request):
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
    status_update = ToDo.objects.filter(id=id)[0]
    status_update.status = "reassigned"
    status_update.save()
    messages.info(request, "Status Changed to Resassigned")
    return redirect(todo)



def log_sheet(request):
    if request.user.is_authenticated:
        logged_in_employee = Employee.objects.get(user=request.user)
        current_log = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).first()
        punched_in = False
        punched_out = False
        today_logs = None
        
        if current_log:
            if current_log.punch_out_time is None:
                punched_in = True
            else:
                punched_out = True
                today_logs = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).order_by('-punch_in_time').first()
        
        time_now = datetime.now().time()
        
        context = {
            'time_now': time_now,
            'today_logs': today_logs,
            'punched_in': punched_in,
            'punched_out': punched_out,
        }
        return render(request, 'features/log_sheet.html', context)
    else:
        return redirect('login')


def punch_in(request):
    if request.method == 'POST':
        logged_in = Employee.objects.get(user=request.user)
        today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

        if today_logs.exists():
            messages.info(request, "You have already punched in for today.")
            return redirect('log_sheet')
        else:
            punch = LogSheet(user=logged_in, punch_in_time=datetime.now().time())
            punch.save()
            messages.success(request, "Punched in successfully.")
            return redirect('log_sheet')
    return redirect('log_sheet')


def punch_out(request):
    if request.method == 'POST':
        logged_in = Employee.objects.get(user=request.user)
        today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

        if today_logs.exists() and today_logs.latest('punch_in_time').punch_out_time:
            # User has already punched out for the day, redirect to punch in page
            messages.info(request, "You have already punched out for today.")
            return redirect('punch_in')
        elif today_logs.exists():
            # Update the latest LogSheet instance with user's tasks, meetings, and remarks and punch out time
            punch = today_logs.latest('punch_in_time')
            punch.punch_out_time = datetime.now().time()
            punch.tasks = request.POST['tasks']
            punch.meetings = request.POST['meetings']
            punch.remarks = request.POST['remarks']
            punch.save()
            messages.success(request, "Punched out successfully.")
            return redirect('punch_in')
        else:
            # User has not punched in for the day, redirect to punch in page
            messages.info(request, "You need to punch in before punching out.")
            return redirect('punch_in')
    return redirect('log_sheet')






def company_setup(request):
    if 'manage_company' in custom_data_views(request):
        company_setup= Company.objects.all().order_by('-created').first()
        context = {
            'company_setup':company_setup
        }
        return render (request,'features/company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


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
            context = {
            'setup':setup
            }
            return render(request,'features/edit_company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')