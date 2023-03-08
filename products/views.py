from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def products(request):
    products = Product.objects.all()
    category = ProductCategory.objects.all()
    unit = ProductUnit.objects.all()
    context={
        'products':products,
        'category':category,
        'unit':unit,
    }
    return render (request,'products/products.html',context)


def add_product(request):
    if request.method == "POST":
        product_type = request.POST["product_type"]
        product_title = request.POST["product_title"]
        product_description = request.POST["product_description"]
        product_price = request.POST["product_price"]
        product_quantity = request.POST["product_quantity"]
        category = request.POST["product_category"]
        unit = request.POST["product_unit"]
        product_category = ProductCategory.objects.get(id=category)
        product_unit = ProductUnit.objects.get(id=unit)
        
        Product.objects.create(product_type=product_type,product_title=product_title, product_description=product_description, 
                               product_price=product_price, product_quantity=product_quantity,product_category=product_category,product_unit=product_unit)
        return redirect(products)
    else:
        return render (request,'products/add_product.html')


def edit_product(request,id):
    return render (request,'products/edit_product.html')


def delete_product(request,id):
    return render (request,'products/delete_product.html')


def product_setup(request):
    category = ProductCategory.objects.all()
    unit = ProductUnit.objects.all()
    context = {
        'category':category,
        'unit':unit,
    }
    return render (request,'products/product_setup.html',context)

def add_product_category(request):
    if request.method =="POST":
        product_category = request.POST['product_category']
        if ProductCategory.objects.filter(product_category=product_category).exists():
            messages.info(request, "category already exixts")
            return redirect(product_setup)
        else:
            ProductCategory.objects.create(product_category=product_category)
            messages.info(request, "category Added Successfully")
            return redirect(product_setup)
        
def edit_product_category(request,id):
    return render (request,'products/delete_product.html')


def delete_product_category(request,id):
    category = ProductCategory.objects.get(id=id)
    category.delete()
    messages.info(request, "Product Category Deleted Successfully")
    return redirect(product_setup)



def add_product_unit(request):
    if request.method =="POST":
        product_unit = request.POST['product_unit']
        if ProductUnit.objects.filter(product_unit=product_unit).exists():
            messages.info(request, "unit already exixts")
            return redirect(product_setup)
        else:
            ProductUnit.objects.create(product_unit=product_unit)
            messages.info(request, "unit Added Successfully")
            return redirect(product_setup)
        
def edit_product_unit(request,id):
    return render (request,'products/delete_product.html')


def delete_product_unit(request,id):
    unit = ProductUnit.objects.get(id=id)
    unit.delete()
    messages.info(request, "Product Unit Deleted Successfully")
    return redirect(product_setup)
    
