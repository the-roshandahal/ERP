from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import datetime


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user is None:
                messages.info(request, "Invalid credentials")
                return redirect("login")
                
            if user is not None and user.is_superuser:
                auth.login(request, user)
                messages.info(request, "Logged in successfully.")
                return redirect("admin:index")

            if user is not None:
                auth.login(request, user)
                messages.info(request, "Logged in successfully.")
                return redirect(home)
        else:
            return render (request,'account/login.html')

def logout(request):
    auth.logout(request)
    return redirect(login)

def home(request):
    if request.user.is_authenticated:
        return render (request,'index.html') 
    else:
        return redirect('login')


def check_permission(request):
    logged_in_user = User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    role=Role.objects.get(role=user.permission)
    permission=Permission.objects.get(role=role)
    permissions = []

    if permission.create_account:
        permissions.append('create')
    if permission.read_account:
        permissions.append('read')
    if permission.update_account:
        permissions.append('update')
    if permission.delete_account:
        permissions.append('delete')
    return permissions



def role(request):
    if 'read' in check_permission(request):
        roles = Permission.objects.all()
        context = {
            'roles':roles,
        }
        return render (request,'account/role.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def create_role(request):
    if 'create' in check_permission(request):
        if request.method == "POST":
            role = request.POST["role"]
            create_finance = request.POST.get('create_finance', 0)
            read_finance = request.POST.get('read_finance', 0)
            update_finance = request.POST.get('update_finance', 0)
            delete_finance = request.POST.get('delete_finance', 0)
            create_account = request.POST.get('create_account', 0)
            read_account = request.POST.get('read_account', 0)
            update_account = request.POST.get('update_account', 0)
            delete_account = request.POST.get('delete_account', 0)
            create_leads = request.POST.get('create_leads', 0)
            read_leads = request.POST.get('read_leads', 0)
            update_leads = request.POST.get('update_leads', 0)
            delete_leads = request.POST.get('delete_leads', 0)
            try:
                new_role=Role.objects.create( role = role)
                new_role.save()

                role_obj = Role.objects.get(role=new_role)

                Permission.objects.create(role=role_obj, create_finance =create_finance, read_finance =read_finance, update_finance =update_finance, 
                                        delete_finance =delete_finance, create_account =create_account, read_account =read_account, update_account =update_account,
                                        delete_account =delete_account, create_leads =create_leads, read_leads =read_leads, update_leads =update_leads, 
                                        delete_leads =delete_leads)
                return redirect('role')

            except Exception:
                print('something went wrong')
                return redirect('role')
        else:
            return redirect('role')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def edit_role(request, id):
    if 'update' in check_permission(request):
        permission = Permission.objects.get(id=id)
        new_role = Role.objects.get(role = permission.role)
        if request.method == "POST":
            new_role.role = request.POST["role"]
            permission.create_finance = request.POST.get('create_finance', 0)
            permission.read_finance = request.POST.get('read_finance', 0)
            permission.update_finance = request.POST.get('update_finance', 0)
            permission.delete_finance = request.POST.get('delete_finance', 0)

            permission.create_account = request.POST.get('create_account', 0)
            permission.read_account = request.POST.get('read_account', 0)
            permission.update_account = request.POST.get('update_account', 0)
            permission.delete_account = request.POST.get('delete_account', 0)

            permission.create_leads = request.POST.get('create_leads', 0)
            permission.read_leads = request.POST.get('read_leads', 0)
            permission.update_leads = request.POST.get('update_leads', 0)
            permission.delete_leads = request.POST.get('delete_leads', 0)
            try:
                permission.save()
                new_role.save()
            except Exception:
                print('something went wrong')
                return redirect('role')
            return redirect('role')
        else:
            role_data = Permission.objects.get(id=id)
            context={
                'role_data':role_data,
            }
            return render(request, 'account/edit_role.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

def delete_role(request,id):
    if 'delete' in check_permission(request):
        role_data = Role.objects.get(id=id)
        print(role_data)
        deleted_role = role_data.role
        role_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('role')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def company_user(request):
    if 'read' in check_permission(request):
        company_users = CompanyUser.objects.all()
        roles = Role.objects.all()
        context = {
            'company_users':company_users,
            'roles':roles,
        }
        return render (request,'account/company_user.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def create_company_user(request):
    if 'create' in check_permission(request):
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            role = request.POST['role']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            permission=Permission.objects.get(role=role)
            CompanyUser.objects.create(user=user,permission=permission)
            user.save()
            return redirect('company_user')
        else:
            return redirect('company_user')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    



def edit_company_user(request,id):
    if 'update' in check_permission(request):
        if request.method =="POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            role = request.POST['role']
            user_data = CompanyUser.objects.get(id=id)
            permission=Permission.objects.get(role=role)

            user = User.objects.get(username=username)
            user.username=username
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            user_data.permission=permission
            user_data.save()
            return redirect('company_user')
        else:
            user_data = CompanyUser.objects.get(id=id)
            roles = Role.objects.all()
            context={
                'user_data':user_data,
                'roles':roles,
            }
            return render (request,'account/edit_company_user.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def delete_company_user(request,id):
    if 'delete' in check_permission(request):
        user_data = CompanyUser.objects.get(id=id)
        user = User.objects.get(username=user_data.user.username)
        print(user)
        if (user.is_superuser==True):
            messages.info(request, "This user can't be deleted.")
        else:
            user.delete()
            user_data.delete()
            messages.info(request, "User Deleted Successfully")
        return redirect('company_user')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)