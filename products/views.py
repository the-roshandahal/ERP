from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
from account.views import *
from account.models import *
from django.contrib.auth.models import User

from account.context_processors import custom_data_views
# Create your views here.

 
def products(request):
    if 'read_products' in custom_data_views(request):
        products = Product.objects.all()

        context={
            'products':products,
        }
        return render (request,'products/products.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def services(request):
    if 'read_products' in custom_data_views(request):
        services = Service.objects.all()
        category = ProductCategory.objects.all()
        unit = ProductUnit.objects.all()
        context={
            'services':services,
            'category':category,
            'unit':unit,
        }
        return render (request,'products/services.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    



def product_stock(request):
    if 'read_products' in custom_data_views(request):
        product_batch = ProductBatch.objects.all()
        products = Product.objects.all()
        context={
            'product_batch':product_batch,
            'products':products,
        }
        return render (request,'products/product_stock.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def add_product(request):
    if 'create_products' in custom_data_views(request):
        if request.method == "POST":
            product_title = request.POST["product_title"]
            product_description = request.POST["product_description"]
            category = request.POST["product_category"]
            unit = request.POST["product_unit"]
            is_vatable = request.POST.get('is_vatable', 0)

            product_batch = request.POST["product_batch"]
            product_price = request.POST["product_price"]
            purchase_price = request.POST["purchase_price"]
            product_quantity = request.POST.get('product_quantity',0)

            product_category = ProductCategory.objects.get(id=category)
            product_unit = ProductUnit.objects.get(id=unit)
            
            product_obj=Product.objects.create(product_title=product_title, product_description=product_description, 
                                is_vatable=is_vatable, product_category=product_category,product_unit=product_unit)
            product_obj.save()

            batch_obj = ProductBatch.objects.create(product=product_obj,product_batch=product_batch,product_quantity=product_quantity,
                                                    purchase_price=purchase_price,product_price=product_price)
            batch_obj.save()

            logged_in_user = User.objects.get(username=request.user)
            statement_obj = ProductStatement.objects.create(remarks ="Opening Balance", quantity = int(product_quantity), batch=batch_obj,type = 'credit', created_by = str(logged_in_user))
            statement_obj.save()

            return redirect('products')
        else:
            products = Product.objects.all()
            category = ProductCategory.objects.all()
            unit = ProductUnit.objects.all()
            context={
                'products':products,
                'category':category,
                'unit':unit,
            }
            return render (request,'products/add_product.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_batch(request):
    if request.method == "POST":
        product_id = request.POST["product"]
        product_quantity = request.POST["product_quantity"]
        product_batch = request.POST["product_batch"]
        product_price = request.POST["product_price"]
        purchase_price = request.POST["purchase_price"]
        product = Product.objects.get(id=product_id)
        batch_obj = ProductBatch.objects.create(product=product, product_quantity=product_quantity, product_price=product_price, 
                                                product_batch=product_batch,purchase_price=purchase_price)
        batch_obj.save()

        logged_in_user = User.objects.get(username=request.user)
        statement_obj = ProductStatement.objects.create(remarks ="Batch Added", quantity = int(product_quantity), batch=batch_obj,type = 'credit', created_by = str(logged_in_user))
        statement_obj.save()
        

        return redirect('product_stock')



def edit_product(request,id):
    if 'update_products' in custom_data_views(request):
        if request.method == "POST":
            product_title = request.POST["product_title"]
            product_description = request.POST["product_description"]
            category = request.POST["product_category"]
            unit = request.POST["product_unit"]
            is_vatable = request.POST.get('is_vatable', 0)
            
            
            product_category = ProductCategory.objects.get(id=category)
            product_unit = ProductUnit.objects.get(id=unit)
            product_obj = Product.objects.get(id=id)
            
            product_obj.product_title=product_title
            product_obj.product_description=product_description
            product_obj.is_vatable=is_vatable
            product_obj.product_category=product_category
            product_obj.product_unit=product_unit
            product_obj.save()
            return redirect('products')
        else:
            product = Product.objects.get(id=id)
            category = ProductCategory.objects.all()
            unit = ProductUnit.objects.all()
            context={
                'product':product,
                'category':category,
                'unit':unit,
            }
            return render (request,'products/edit_product.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def delete_product(request,id):
    if 'delete_products' in custom_data_views(request):
        product = Product.objects.get(id=id)
        product.delete()
        messages.info(request, "Product Deleted Successfully")
        return redirect(products)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def product_setup(request):
    if 'read_products' in custom_data_views(request):
        category = ProductCategory.objects.all()
        unit = ProductUnit.objects.all()
        context = {
            'category':category,
            'unit':unit,
        }
        return render (request,'products/product_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def add_product_category(request):
    if 'create_products' in custom_data_views(request):
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
        return redirect('home')
        
def edit_product_category(request,id):
    if 'update_products' in custom_data_views(request):
        return render (request,'products/delete_product.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_product_category(request,id):
    if 'delete_products' in custom_data_views(request):
        category = ProductCategory.objects.get(id=id)
        category.delete()
        messages.info(request, "Product Category Deleted Successfully")
        return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def add_product_unit(request):
    if 'create_products' in custom_data_views(request):
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
        return redirect('home')
    


def edit_product_unit(request,id):
    if 'update_products' in custom_data_views(request):
        return render (request,'products/delete_product.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def delete_product_unit(request,id):
    if 'delete_products' in custom_data_views(request):
        unit = ProductUnit.objects.get(id=id)
        unit.delete()
        messages.info(request, "Product Unit Deleted Successfully")
        return redirect(product_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def update_product_quantity(request):
    if 'update_products' in custom_data_views(request):
        if request.method =="POST":
            product = request.POST["product"]
            update_type = request.POST["update_type"]
            new_product_quantity = request.POST["new_product_quantity"]
            remarks = request.POST["remarks"]
            product_obj = ProductBatch.objects.get(id=product)
            logged_in_user = User.objects.get(username=request.user)

            if update_type == 'debit':
                product_obj.product_quantity=product_obj.product_quantity-int(new_product_quantity)
                product_obj.save()
                statement_obj = ProductStatement.objects.create(remarks = remarks, quantity = int(new_product_quantity), batch=product_obj,type = 'debit', created_by = str(logged_in_user))
                statement_obj.save()
            else:
                product_obj.product_quantity=product_obj.product_quantity+int(new_product_quantity)
                product_obj.save()
                statement_obj = ProductStatement.objects.create(remarks = remarks, quantity = int(new_product_quantity), batch=product_obj,type = 'credit', created_by = str(logged_in_user))
                statement_obj.save()

            messages.info(request, f"Quantity {update_type}ed succesfully.")
            return redirect(product_stock)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def product_statement(request):
    if 'read_products' in custom_data_views(request):
        product_statements = ProductStatement.objects.all()
        context = {
            'product_statements':product_statements
        }
        return render (request,'products/product_statement.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    








def add_service(request):
    if 'create_products' in custom_data_views(request):
        if request.method == "POST":
            service_title = request.POST["service_title"]
            service_price = request.POST["service_price"]
            unit = request.POST["service_unit"]
            category = request.POST["service_category"]
            is_vatable = request.POST.get('is_vatable', 0)

            service_category = ProductCategory.objects.get(id=category)
            service_unit = ProductUnit.objects.get(id=unit)
            
            service_obj=Service.objects.create(service_title=service_title,service_price=service_price,service_unit=service_unit,
                                               service_category=service_category,is_vatable=is_vatable)
            service_obj.save()

            return redirect('services')
        else:
            services = Service.objects.all()
            category = ProductCategory.objects.all()
            unit = ProductUnit.objects.all()
            context={
                'services':services,
                'category':category,
                'unit':unit,
            }
            return render (request,'products/add_service.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_service(request,id):
    if 'update_products' in custom_data_views(request):
        if request.method == "POST":
            service_title = request.POST["service_title"]
            service_price = request.POST["service_price"]
            service_description = request.POST["service_description"]
            category = request.POST["service_category"]
            unit = request.POST["service_unit"]
            is_vatable = request.POST.get('is_vatable', 0)
            
            
            service_category = ProductCategory.objects.get(id=category)
            service_unit = ProductUnit.objects.get(id=unit)
            service_obj = Service.objects.get(id=id)
            
            service_obj.service_title=service_title
            service_obj.service_description=service_description
            service_obj.is_vatable=is_vatable
            service_obj.service_category=service_category
            service_obj.service_unit=service_unit
            service_obj.service_price=service_price
            service_obj.save()
            return redirect('services')
        else:
            service = Service.objects.get(id=id)
            category = ProductCategory.objects.all()
            unit = ProductUnit.objects.all()
            context={
                'service':service,
                'category':category,
                'unit':unit,
            }
            return render (request,'products/edit_service.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

