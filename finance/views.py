from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render
from decimal import Decimal
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from account.models import *
from products.models import *
from customer.models import *
from .models import *
from account.context_processors import custom_data_views
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Q
from datetime import datetime,date,timedelta
# Create your views here.


def invoice(request):
    if 'read_finance' in custom_data_views(request):
        invoices = Invoice.objects.all()
        print(invoices)
        context={
            'invoices':invoices
            }
        return render (request, 'finance/invoices.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def finance(request):
    if 'read_finance' in custom_data_views(request):
        invoice = Invoice.objects.all()
        receipt = Receipt.objects.all()
        today_invoice_total = Invoice.objects.filter(created=date.today()).aggregate(total=Sum('invoice_amount'))['total'] or 0
        today_receipt_total = Receipt.objects.filter(created=date.today()).aggregate(total=Sum('paid_amount'))['total'] or 0
        today_expense_total = Expense.objects.filter(created=date.today()).aggregate(total=Sum('expense_amount'))['total'] or 0
        
        total_invoice_amt=0
        if invoice:
            for invoice in invoice :
                total_invoice_amt = total_invoice_amt+ invoice.invoice_amount


        total_receipt_amt=0
        if receipt:
            for receipt in receipt :
                total_receipt_amt = total_receipt_amt+ receipt.paid_amount

        today = date.today()
        last_7_days = today - timedelta(days=6)

        context = {
            'totals_by_day': [
                {
                    'date': last_7_days + timedelta(days=i),
                    'invoice_total': Invoice.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('invoice_amount'))['total'] or 0,
                    'receipt_total': Receipt.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('paid_amount'))['total'] or 0,
                    'expense_total': Expense.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('expense_amount'))['total'] or 0,
                }
                for i in range(7)
            ],
            'total_invoice_amt':total_invoice_amt,
            'total_receipt_amt':total_receipt_amt,
            'today_invoice_total':today_invoice_total,
            'today_receipt_total':today_receipt_total,
            'today_expense_total':today_expense_total,
        }
        return render (request, 'finance/dashboard.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def create_invoice(request):
    if 'create_finance' in custom_data_views(request):
        if request.method == "POST":
            customer = request.POST["customer"]
            selected_product_ids = request.POST.getlist("selected_product")
            selected_product_amounts = request.POST.getlist("selected_product_amount")
            selected_product_discounts = request.POST.getlist("selected_product_discount")
            selected_product_quantities = request.POST.getlist("selected_product_quantity")
            misc_name = request.POST["misc_name"]
            misc_amount = Decimal(request.POST["misc_amount"])
            due_date = request.POST["due_date"]
            remarks = request.POST["remarks"]
            customer=Customer.objects.get(id=customer)
            # create the invoice instance
            invoice = Invoice.objects.create(
                customer=customer,
                misc_name=misc_name,
                misc_amount=misc_amount,
                due_date=due_date,
                remarks=remarks,
                created_by=request.user.username,
            )
            
            # calculate the invoice amount
            invoice_amount = misc_amount
            for i in range(len(selected_product_ids)):
                product_id = selected_product_ids[i]
                product_amount = Decimal(selected_product_amounts[i])
                product_discount = Decimal(selected_product_discounts[i])
                product_quantity = int(selected_product_quantities[i])
                product_total = (product_amount - product_discount) * product_quantity
                invoice_amount += product_total
            invoice.invoice_amount = invoice_amount
            
            # calculate the VAT amount
            if selected_product_ids and Product.objects.filter(id__in=selected_product_ids, is_vatable=True).exists():
                vat_rate = Decimal("0.12") # assume VAT rate is 12%
                vat_amount = invoice_amount * vat_rate
                invoice.vat_amount = vat_amount
            
            # save the invoice instance
            invoice.save()
            
            # create the invoice product instances
            for i in range(len(selected_product_ids)):
                product_id = selected_product_ids[i]
                product_amount = Decimal(selected_product_amounts[i])
                product_discount = Decimal(selected_product_discounts[i])
                product_quantity = int(selected_product_quantities[i])
                product = Product.objects.get(id=product_id)
                InvoiceProduct.objects.create(
                    invoice=invoice,
                    product=product,
                    product_quantity=product_quantity,
                    product_price=product_amount - product_discount,
                )
                product.product_quantity = -product_quantity
                product.save()
            details = invoice.id
            details = "INV_NO_"+str(details)
            if(Statement.objects.filter(customer=customer).exists()):

                bal = Statement.objects.filter(
                    customer=customer).order_by('-id')[:1].get()
                initial_balance = bal.balance
                balance = float(initial_balance) + float(invoice_amount)

                Statement.objects.create(
                    customer=customer, transaction='invoice', details=details, amount=invoice_amount, balance=balance)
            else:
                amount = 0
                payment = 0
                balance = 0
                Statement.objects.create(customer=customer, transaction='Opening Balance',
                                        details='--', amount=amount, payment=payment, balance=balance)

                bal = Statement.objects.filter(
                    customer=customer).order_by('-id')[:1].get()
                initial_balance = bal.balance
                balance = float(initial_balance) + float(invoice_amount)

                Statement.objects.create(
                    customer=customer, transaction='invoice', details=details, amount=invoice_amount, balance=balance)
            messages.info(request, "Invoice Created Successfully.")
            return redirect(view_invoice, id=invoice.id)
        else:
            product = Product.objects.all()
            customer = Customer.objects.all()
            context = {
                'product': product,
                'customer': customer
            }
            return render(request, "finance/create_invoice.html", context)


# def create_invoice(request):
#     if 'create_finance' in custom_data_views(request):
#         if request.method == "POST":
#             customer = request.POST["customer"]
#             selected_product = request.POST.getlist("selected_product")
#             selected_product_amount = request.POST.getlist("selected_product_amount")
#             selected_product_discount = request.POST.getlist("selected_product_discount")
#             selected_product_quantity = request.POST.getlist("selected_product_quantity")
#             misc_name = request.POST["misc_name"]
#             misc_amount = request.POST["misc_amount"]
#             discount = request.POST["discount"]
#             due_date = request.POST["due_date"]
#             remarks = request.POST["remarks"]
            

#             product_vatable_amount = 0
#             for i in range(len(selected_product)):
#                 for selected_product in selected_product:
#                     product = Product.objects.get(id = selected_product)
#                     if product.is_vatable == True:
#                         vatable_amount = product.product_price

#             vatable_amount = product_vatable_amount+misc_amount

#             total_vat_amount = vatable_amount*0.13


#             total_product_amount = sum(float(amount) for amount in selected_product_amount)

#             sub_total = float(total_product_amount) + float(misc_amount)

#             vatable_amount = sub_total - float(discount)

#             if product.is_vatable == True:
#                 vat_amount = vatable_amount*0.13
#             else:
#                 vat_amount = 0

#             total = vatable_amount + float(vat_amount)
#             customer = Customer.objects.get(id=customer)
#             created_by_user = User.objects.get(username=request.user)
#             created_by = str(created_by_user)

        
#             invoice_1 = Invoice.objects.create(customer=customer,  misc_name=misc_name, misc_amount=misc_amount, discount=discount,
#                                             vat_amount=vat_amount, remarks=remarks, created_by = created_by, invoice_amount = total)
#             # invoice_1.product.set(selected_product)
#             invoice_1.save()

#             details = invoice_1.id
#             details = "INV_NO_"+str(details)

#             if(Statement.objects.filter(customer=customer).exists()):

#                 bal = Statement.objects.filter(
#                     customer=customer).order_by('-id')[:1].get()
#                 initial_balance = bal.balance
#                 balance = float(initial_balance) + float(total)

#                 Statement.objects.create(
#                     customer=customer, transaction='invoice', details=details, amount=total, balance=balance)
#             else:
#                 amount = 0
#                 payment = 0
#                 balance = 0
#                 Statement.objects.create(customer=customer, transaction='Opening Balance',
#                                         details='--', amount=amount, payment=payment, balance=balance)

#                 bal = Statement.objects.filter(
#                     customer=customer).order_by('-id')[:1].get()
#                 initial_balance = bal.balance
#                 balance = float(initial_balance) + float(total)

#                 Statement.objects.create(
#                     customer=customer, transaction='invoice', details=details, amount=total, balance=balance)
#             messages.info(request, "Invoice Created Successfully.")
#             return redirect(view_invoice, id=invoice_1.id)
#         else:
#             product = Product.objects.all()
#             customer = Customer.objects.all()
#             context = {
#                 'product': product,
#                 'customer': customer
#             }
#             return render(request, "finance/create_invoice.html", context)
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect('home')
    

def view_invoice(request, id):
    if 'read_finance' in custom_data_views(request):
        invoice = Invoice.objects.get(id=id)
        product = InvoiceProduct.objects.filter(invoice_id=id)
        context = {
            'product':product,
            'invoice': invoice,
        }
        return render(request, 'finance/view_invoice.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

    

def statement(request):
    if 'read_finance' in custom_data_views(request):
        customer = Customer.objects.all()
        context = {
            'customer': customer
        }
        return render(request, 'finance/statement.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def single_statement(request, id):
    if 'read_finance' in custom_data_views(request):
        statements = Statement.objects.filter(customer=id)

        calc_statements = Statement.objects.filter(customer=id)
        amt_total = 0.0
        for calc_statements in calc_statements:
            if type(calc_statements.amount) is float:
                amt_total = amt_total+calc_statements.amount

        calc_statements_2 = Statement.objects.filter(customer=id)
        total_payment = 0.0
        for calc_statements_2 in calc_statements_2:
            if type(calc_statements_2.payment) is float:
                total_payment = total_payment+calc_statements_2.payment

        balance_due = amt_total-total_payment

        customer = Customer.objects.get(id=id)
        context = {
            'customer': customer,
            'balance_due': balance_due,
            'statements': statements,
        }
        return render(request, 'finance/single_statement.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')





def receipt(request):
    if 'read_finance' in custom_data_views(request):
        receipts = Receipt.objects.all()
        searched_receipts = receipts
        query = request.GET.get("query", "")
        if query != "":
            receipts = searched_receipts.filter(Q(id__icontains=query))

        all_receipts = Receipt.objects.all()

        receipt_summary = 0
        for all_receipts in all_receipts:
            receipt_summary = receipt_summary+all_receipts.paid_amount

        context = {
            'query': query,
            'id': id,
            'receipt_summary': receipt_summary,
            'receipts': receipts,
        }
        return render(request, 'finance/receipts.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def create_receipt(request):
    if 'create_finance' in custom_data_views(request):
        if request.method == "POST":
            customer = request.POST["customer"]
            payment_method = request.POST["payment_method"]
            paid_amount = request.POST["paid_amount"]
            remarks = request.POST["remarks"]
            if request.FILES and request.FILES["payment_receipt"]:
                payment_receipt = request.FILES["payment_receipt"]
            else:
                payment_receipt = None

            customer = Customer.objects.get(id=customer)
            created_by_user = User.objects.get(username=request.user)

            created_by = str(created_by_user)
            receipt_1 = Receipt.objects.create(customer=customer, payment_method=payment_method, paid_amount=paid_amount,
                                            payment_receipt=payment_receipt, remarks=remarks, created_by = created_by)
            receipt_1.save()
            details = receipt_1.id
            details = "REC_NO_"+str(details)

            bal = Statement.objects.filter(customer=customer).order_by('-id')[:1].get()
            initial_balance = bal.balance
            balance = float(initial_balance) - float(paid_amount)
            Statement.objects.create(customer=customer, transaction='receipt',
                                    details=details, payment=paid_amount, balance=balance)
            return redirect(single_statement, id=customer.id)
        else:
            customer = Customer.objects.all()
            context = {
                'customer': customer
            }
            return render(request, "finance/create_receipt.html", context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def view_receipt(request, id):
    if 'read_finance' in custom_data_views(request):
        receipt = Receipt.objects.get(id=id)
        context = {
            'receipt': receipt,
        }
        return render(request, 'finance/view_receipt.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def expenses(request):
    if 'read_finance' in custom_data_views(request):
        expense = Expense.objects.all()
        expense_type= ExpenseType.objects.all()
        
        context = {
            'expense': expense,
            'expense_type': expense_type,
        }
        return render(request, 'finance/expenses.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def create_expense(request):
    if 'read_finance' in custom_data_views(request):
        if request.method == "POST":
            expense_title = request.POST['expense_title']
            expense_amount  = request.POST['expense_amount']
            type = request.POST['expense_type']
            remarks = request.POST['remarks']

            expense_type = ExpenseType.objects.get(id=type)
            Expense.objects.create(expense_title = expense_title, expense_amount = expense_amount, 
                                   expense_type = expense_type,remarks = remarks)
            return redirect('expenses')
        else:
            
            return render(request, 'finance/expenses.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

















