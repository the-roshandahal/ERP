from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def products(request):
    products = Product.objects.all()
    context={
        'products':products,
    }
    return render (request,'products/products.html',context)


def add_product(request):
    if request.method == "POST":
        product_type = request.POST["product_type"]
        product_title = request.POST["product_title"]
        product_description = request.POST["product_description"]
        product_price = request.POST["product_price"]
        product_quantity = request.POST["product_quantity"]
        
        Product.objects.create(product_type=product_type,product_title=product_title, product_description=product_description, 
                               product_price=product_price, product_quantity=product_quantity)
        return redirect(products)
    else:
        return render (request,'products/add_product.html')


def edit_package(request,id):
    return render (request,'products/edit_package.html')


def delete_package(request,id):
    return render (request,'products/delete_package.html')