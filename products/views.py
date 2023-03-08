from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
from account.views import *
from account.models import *
from django.contrib.auth.models import User

# Create your views here.
def check_permission(request):
    logged_in_user = User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    role=Role.objects.get(role=user.permission)
    permission=Permission.objects.get(role=role)
    permissions = []

    if permission.create_products:
        permissions.append('create')
    if permission.read_products:
        permissions.append('read')
    if permission.update_products:
        permissions.append('update')
    if permission.delete_products:
        permissions.append('delete')
    return permissions

    
def products(request):
    if 'read' in check_permission(request):
        products = Product.objects.all()
        category = ProductCategory.objects.all()
        unit = ProductUnit.objects.all()
        context={
            'products':products,
            'category':category,
            'unit':unit,
        }
        return render (request,'products/products.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def add_product(request):
    if 'create' in check_permission(request):
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
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def edit_product(request,id):
    if 'update' in check_permission(request):
        return render (request,'products/edit_product.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def delete_product(request,id):
    if 'delete' in check_permission(request):
        product = Product.objects.get(id=id)
        product.delete()
        messages.info(request, "Product Deleted Successfully")
        return redirect(products)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def product_setup(request):
    if 'read' in check_permission(request):
        category = ProductCategory.objects.all()
        unit = ProductUnit.objects.all()
        context = {
            'category':category,
            'unit':unit,
        }
        return render (request,'products/product_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def add_product_category(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            product_category = request.POST['product_category']
            if ProductCategory.objects.filter(product_category=product_category).exists():
                messages.info(request, "category already exixts")
                return redirect(product_setup)
            else:
                ProductCategory.objects.create(product_category=product_category)
                messages.info(request, "category Added Successfully")
                return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
        
def edit_product_category(request,id):
    if 'update' in check_permission(request):
        return render (request,'products/delete_product.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def delete_product_category(request,id):
    if 'delete' in check_permission(request):
        category = ProductCategory.objects.get(id=id)
        category.delete()
        messages.info(request, "Product Category Deleted Successfully")
        return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)



def add_product_unit(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            product_unit = request.POST['product_unit']
            if ProductUnit.objects.filter(product_unit=product_unit).exists():
                messages.info(request, "unit already exixts")
                return redirect(product_setup)
            else:
                ProductUnit.objects.create(product_unit=product_unit)
                messages.info(request, "unit Added Successfully")
                return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    


def edit_product_unit(request,id):
    if 'update' in check_permission(request):
        return render (request,'products/delete_product.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def delete_product_unit(request,id):
    if 'delete' in check_permission(request):
        unit = ProductUnit.objects.get(id=id)
        unit.delete()
        messages.info(request, "Product Unit Deleted Successfully")
        return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    
