from django.shortcuts import render, redirect
from account.models import *
# Create your views here.

def home(request):
    return render (request,'index.html') 