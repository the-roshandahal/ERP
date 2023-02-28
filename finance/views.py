from django.shortcuts import render

from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.models import *
# Create your views here.

def check_permission(request):
    logged_in_user = User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    role=Role.objects.get(role=user.permission)
    permission=Permission.objects.get(role=role)
    if permission.create_finance or permission.read_finance or permission.update_finance or permission.delete_finance:
        return True
    else:
        return False

def invoice(request):
    if check_permission(request):
        return render (request, 'finance/invoices.html')
    else:
        return render (request, '404.html')

def receipt(request):
    if check_permission(request):
        return render (request, 'finance/receipts.html')
    else:
        return render (request, '404.html')