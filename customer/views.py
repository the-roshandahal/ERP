from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages, auth
from account.views import *
from account.models import *

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


def client(request):
    if 'read' in check_permission(request):
        package = Package.objects.all()
        customer = Customer.objects.all()
        context = {
            'package': package,
            'customer': customer
        }
        return render(request,'client/client.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    


def add_client(request):
    if 'create' in check_permission(request):
        if request.method == "POST":
            client_name = request.POST["client_name"]
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            Customer.objects.create(client_name=client_name,
                                    address=address, email=email, contact=contact)
            return redirect('client')
        else:
            return render(request,'client/add_client.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def edit_client(request,id):
    if 'update' in check_permission(request):
        if request.method == "POST":
            client_name = request.POST["client_name"]
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]

            client_data = Customer.objects.filter(id=id)[0]

            client_data.client_name = client_name
            client_data.address = address
            client_data.email = email
            client_data.contact = contact
            client_data.save()
            messages.info(request, "Client edited successfully.")
            return redirect('client')
        else:
            client_data = Customer.objects.filter(id=id)[0]
            context = {
                'client_data':client_data
            }
            return render(request,'client/edit_client.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    
def delete_client(request,id):
    if 'delete' in check_permission(request):
        delete_client = Customer.objects.get(id=id)
        deleted_client = delete_client
        delete_client.delete()
        messages.info(request, f"{deleted_client} Deleted Successfully")
        return redirect('client')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)