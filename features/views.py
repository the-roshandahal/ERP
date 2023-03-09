from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
# Create your views here.


def todo(request):
    logged_in_user = User.objects.get(username=request.user)
    company_user = CompanyUser.objects.get(user=logged_in_user)
    done_todo = ToDo.objects.filter(task_to = company_user, status = 'done').order_by('priority')
    undone_todo = ToDo.objects.filter(task_to = company_user, status = 'incomplete')
    reassigned_todo = ToDo.objects.filter(task_to = company_user, status = 'reassigned')
    mytasks = ToDo.objects.filter(task_from= company_user)
    
    users = CompanyUser.objects.all()
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
        task_from = CompanyUser.objects.get(user=logged_in_user)
        for assign_to in assign_to:
            assign_to = CompanyUser.objects.get(id=assign_to)
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
    logged_in_user=User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    log_sheet=LogSheet.objects.filter(user=user).order_by('-created')
    context = {
        'log_sheet':log_sheet,
    }
    return render(request,'features/log_sheet.html',context)


def add_log_sheet(request):
    if request.method == "POST":
        punch_out_time = request.POST["punch_out_time"]
        punch_in_time = request.POST["punch_in_time"]
        tasks = request.POST["tasks"]
        meetings = request.POST["meetings"]
        remarks = request.POST["remarks"]

        logged_in_user=User.objects.get(username=request.user)
        user = CompanyUser.objects.get(user=logged_in_user)
        log_data = LogSheet.objects.create(punch_out_time=punch_out_time,punch_in_time=punch_in_time,tasks=tasks,meetings=meetings,remarks=remarks,user=user)
        log_data.save()
        return redirect(log_sheet)
    else:
        return redirect(log_sheet)