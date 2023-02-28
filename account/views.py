from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def home(request):
    return render (request,'index.html') 

def role(request):
    roles = Role.objects.all()
    context = {
        'roles':roles,
    }
    return render (request,'account/role.html',context)

def create_role(request):
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
        except:
            print('something went wrong')
            return redirect('role')

        return redirect('role')
    else:
        return redirect('role')
    

def company_user(request):
    company_users = CompanyUser.objects.all()
    roles = Role.objects.all()
    context = {
        'company_users':company_users,
        'roles':roles,
    }
    return render (request,'account/company_user.html',context)

def create_company_user(request):
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