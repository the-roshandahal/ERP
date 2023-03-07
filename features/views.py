from django.shortcuts import render, redirect
from account.models import *
# Create your views here.

def home(request):
    return render (request,'index.html') 

def page_not_found_view(request, exception):
    return render(request, "error404.html")