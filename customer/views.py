from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages, auth
from account.views import *
from account.models import *
from finance.models import *
from account.context_processors import custom_data_views
# Create your views here.



def client(request):
    if 'read_finance' in custom_data_views(request):
        customer = Customer.objects.all()
        context = {
            'customer': customer
        }
        return render(request,'client/client.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def add_client(request):
    if 'create_finance' in custom_data_views(request):
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
        return redirect('home')
    

def edit_client(request,id):
    if 'update_finance' in custom_data_views(request):
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
        return redirect('home')
    
def delete_client(request,id):
    print('hello')
    if 'delete_finance' in custom_data_views(request):
        delete_client = Customer.objects.get(id=id)
        deleted_client = delete_client
        delete_client.delete()
        messages.info(request, f"{deleted_client} Deleted Successfully")
        return redirect('client')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_client(request,id):
    if 'read_finance' in custom_data_views(request):
        client = Customer.objects.get(id=id)
        invoices = Invoice.objects.filter(customer=id)
        receipts = Receipt.objects.filter(customer=id)
        context = {
            'client': client,
            'invoices': invoices,
            'receipts': receipts,
        }
        return render(request,'client/view_client.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')