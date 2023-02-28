from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def home(request):
    return render (request,'index.html') 


def admin_dashboard(request):
    roles = Role.objects.all()
    users = CompanyUser.objects.all()
    context = {
        'roles':roles,
        'users':users
    }
    return render (request,'account/admin_dashboard.html',context)


def create_role(request):
    if request.method =="POST":
        role = request.POST["role"]
        
        if 'create_finance' in request.POST:
            create_finance = request.POST['create_finance']
        else:
            create_finance = 0

        if 'read_finance' in request.POST:
            read_finance = request.POST['read_finance']
        else:
            read_finance = 0

        if 'update_finance' in request.POST:
            update_finance = request.POST['update_finance']
        else:
            update_finance = 0

        if 'delete_finance' in request.POST:
            delete_finance = request.POST['delete_finance']
        else:
            delete_finance = 0

        
        if 'create_account' in request.POST:
            create_account = request.POST['create_account']
        else:
            create_account = 0

        if 'read_account' in request.POST:
            read_account = request.POST['read_account']
        else:
            read_account = 0

        if 'update_account' in request.POST:
            update_account = request.POST['update_account']
        else:
            update_account = 0

        if 'delete_account' in request.POST:
            delete_account = request.POST['delete_account']
        else:
            delete_account = 0



        if 'create_leads' in request.POST:
            create_leads = request.POST['create_leads']
        else:
            create_leads = 0

        if 'read_leads' in request.POST:
            read_leads = request.POST['read_leads']
        else:
            read_leads = 0

        if 'update_leads' in request.POST:
            update_leads = request.POST['update_leads']
        else:
            update_leads = 0

        if 'delete_leads' in request.POST:
            delete_leads = request.POST['delete_leads']
        else:
            delete_leads = 0
        try:
            new_role=Role.objects.create( role = role)
            new_role.save()

            roleee = Role.objects.get(role=new_role)

            Permission.objects.create(role=roleee, create_finance =create_finance, read_finance =read_finance, update_finance =update_finance, 
                                    delete_finance =delete_finance, create_account =create_account, read_account =read_account, update_account =update_account,
                                    delete_account =delete_account, create_leads =create_leads, read_leads =read_leads, update_leads =update_leads, 
                                    delete_leads =delete_leads)
        except:
            print('something went wrong')
            return render (request,'account/create_role.html')

        return render (request,'account/create_role.html')
    else:
        return render (request,'account/create_role.html')
    

def create_company_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user=User.objects.create_user(username=username,password=password)
        role=Role.objects.get(id=role)
        CompanyUser.objects.create(user=user,role=role)
        user.save()
        return render(request,'account/create_user.html')
    else:
        role= Role.objects.all()
        context={
            'role':role,
        }
        return render(request,'account/create_user.html',context)