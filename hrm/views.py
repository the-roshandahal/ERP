from django.shortcuts import render,redirect
from .models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from features.views import *
import datetime
from django.core.paginator import Paginator

# Create your views here.

def check_permission(request):
    logged_in_user = User.objects.get(username=request.user)
    user = CompanyUser.objects.get(user=logged_in_user)
    role=Role.objects.get(role=user.permission)
    permission=Permission.objects.get(role=role)
    permissions = []

    if permission.create_hrm:
        permissions.append('create')
    if permission.read_hrm:
        permissions.append('read')
    if permission.update_hrm:
        permissions.append('update')
    if permission.delete_hrm:
        permissions.append('delete')
    return permissions

def hrm(request):
    if 'read' in check_permission(request):
        return render (request,'hrm/hrm.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

def hrm_setup(request):
    if 'read' in check_permission(request):
        month = MonthSetup.objects.all()
        year = YearSetup.objects.all()
        context = {
            'month':month, 
            'year':year,
        }
        return render (request,'hrm/hrm_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

def add_year(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            year = request.POST['year']
            if YearSetup.objects.filter(year=year).exists():
                messages.info(request, "Year already exixts")
                return redirect(hrm_setup)
            else:
                YearSetup.objects.create(year=year)
                messages.info(request, "Year Added Successfully")
                return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    

def add_month(request):
    if 'create' in check_permission(request):
        if request.method =="POST":
            year = request.POST['year']
            month = request.POST['month']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            year = YearSetup.objects.get(id=year)
            MonthSetup.objects.create(year=year,month=month,start_date=start_date,end_date=end_date)
            messages.info(request, "Year Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    


def employees(request):
    if 'read' in check_permission(request):
        employees = Employee.objects.all()
        context = {
            'employees':employees,
        }
        return render (request,'hrm/employees.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def add_employee(request):
    if 'create' in check_permission(request):
        if request.method=="POST":
            name = request.POST['name']
            position = request.POST['position']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            salary = request.POST['salary']
            date_joined = request.POST['date_joined']
            Employee.objects.create(name =name,position =position,email =email,contact =contact,address =address,emp_salary =salary,date_joined = date_joined)
            messages.info(request, "Employee Added Successfully")

            return redirect('employees')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)


def attendance (request):
    if 'create' in check_permission(request):
        employees = Employee.objects.all()
        current_datetime = datetime.date.today()  
        leaves = Leave.objects.all()
        today_leave = Leave.objects.filter(created=current_datetime)
        context = {
            'employees':employees,
            'leaves':leaves,
            'today_leave':today_leave
        }
        return render (request, 'hrm/attendance.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)

    
def add_leave(request):
    if 'create' in check_permission(request):
        if request.method=="POST":
            reason = request.POST['reason']
            emp = request.POST['employee']
            employe = Employee.objects.get(id=emp)
            current_datetime = datetime.date.today()

            if Leave.objects.filter(employee = employe):
                leaves = Leave.objects.filter(employee = employe).order_by('created')[0]
            else:
                leaves=None

            if leaves:
                if leaves.created ==current_datetime:
                    messages.info(request,f"Already added for today ({current_datetime})")
                    return redirect('attendance')
                else:
                    Leave.objects.create(employee=employe,reason =reason)
                    messages.info(request, "Leave Added Successfully")
                    return redirect('attendance')
            else:
                Leave.objects.create(employee=employe,reason =reason)
                messages.info(request, "Leave Added Successfully")
                return redirect('attendance')
        else:
            return redirect('attendance')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)
    




def salary (request):
    if 'create' in check_permission(request):
        if request.method == 'POST':
            month = request.POST['month']

            monthhhh = MonthSetup.objects.get(id=month)
            from_date_obj = monthhhh.start_date
            to_date_obj = monthhhh.end_date

            employees = Employee.objects.all()
            current_datetime = datetime.date.today()               
            date_object = current_datetime
            today_date = date_object.strftime('%Y-%m-%d')
            

            months = MonthSetup.objects.all()
            if 'employee' in request.POST:
                selected_employee = request.POST['employee']
            else:
                selected_employee=None

            data_list=[]


            if selected_employee:
                selected_employee = Employee.objects.get(id=selected_employee)
                total_salary = selected_employee.emp_salary


                diff = to_date_obj - from_date_obj
                difference = diff.days+1

                leave = Leave.objects.filter(employee=selected_employee).filter(created__range=(from_date_obj, to_date_obj)).count()
                total_present_days = difference-leave


                daily_salary = int(total_salary)/difference
                leave_deduction = leave*daily_salary

                salary = daily_salary*total_present_days


                if (salary<=33000):
                    tax_deduction = salary*0.01
                elif(salary<=100000):
                    tax_deduction=(33000*0.01)+(salary-33000)*0.1
                else:
                    tax_deduction=0
                final_salary = salary-tax_deduction


                data_list.append({
                    'name': selected_employee,
                    'total_salary': total_salary,
                    'final_salary': final_salary,
                    'difference': difference,
                    'leave': leave,
                    'leave_deduction': leave_deduction,
                    'tax_deduction': tax_deduction,
                    'final_salary': final_salary,
            })
            else:
                for employees in employees:
                    total_salary = employees.emp_salary

                    diff = to_date_obj - from_date_obj
                    difference = diff.days+1

                    leave = Leave.objects.filter(employee=employees).filter(created__range=(from_date_obj, to_date_obj)).count()
                    total_present_days = difference-leave


                    daily_salary = int(total_salary)/difference
                    leave_deduction = leave*daily_salary

                    salary = daily_salary*total_present_days


                    if (salary<=33000):
                        tax_deduction = salary*0.01
                    elif(salary<=100000):
                        tax_deduction=(33000*0.01)+(salary-33000)*0.1
                    else:
                        tax_deduction=0
                    final_salary = salary-tax_deduction
                    salary_status = Salary.objects.filter(employee = employees,month=monthhhh.month,type='salary')
                    if salary_status:
                        status='paid'
                    else:
                        status='unpaid'
                    data_list.append({
                        'name': employees,
                        'total_salary': total_salary,
                        'final_salary': final_salary,
                        'difference': difference,
                        'leave': leave,
                        'leave_deduction': leave_deduction,
                        'tax_deduction': tax_deduction,
                        'final_salary': final_salary,
                        'status':status,
                        'type':'salary'
                })
                    

            employeessss = Employee.objects.all()
            context={
                'months':months,
                'monthhhh':monthhhh,
                'data_list':data_list,
                'from_date_obj':from_date_obj,
                'to_date_obj':to_date_obj,
                'today_date':today_date,
                'employeessss':employeessss,
            }

            return render(request,'hrm/salary.html',context)

        else:
            months = MonthSetup.objects.all()
            current_datetime = datetime.date.today()
            date_object = current_datetime
            today_date = date_object.strftime('%Y-%m-%d')
            employeessss = Employee.objects.all()
            recent_salary = Salary.objects.all().order_by('created')
            paginator = Paginator(recent_salary, 10)
            page_number = request.GET.get('page')
            recent_salary = paginator.get_page(page_number)
            context = {
                'months':months,
                'today_date':today_date,
                'employeessss':employeessss,
                'recent_salary':recent_salary,
            }
            return render(request,'hrm/salary.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect(home)







def pay_salary(request):
    if request.method =="POST":
        selected_salary = request.POST.getlist("selected_salary")
        sel=selected_salary
       
        for sel in sel:
            x_list = sel.split(",")
            name, month, leave_deduction, tax_deduction, paid_salary = x_list
            employee = Employee.objects.get(name=name)
            prev_salary = Salary.objects.filter(month=month,employee=employee,type='salary')
            advance_salary = Salary.objects.filter(month=month,employee=employee).filter(type='advance')
            if prev_salary:
                pass
            else:
                if advance_salary:
                    advance_amount = 0
                    for advance_salary in advance_salary:
                        amount = advance_salary.paid_salary
                        advance_amount = advance_amount+amount

                    final_salary = float(paid_salary)-advance_amount
                    Salary.objects.create(employee=employee,month=month,leave_deduction=leave_deduction,tax_deduction=tax_deduction,paid_salary=final_salary)
                else:
                    Salary.objects.create(employee=employee,month=month,leave_deduction=leave_deduction,tax_deduction=tax_deduction,paid_salary=paid_salary)
                
        return redirect('salary')
    else:
        return redirect('salary')

def advance_salary(request):
    if request.method =="POST":
        month = request.POST['month']
        employee = request.POST['employee']
        amount = request.POST['amount']
        type='advance'
        leave_deduction=0
        tax_deduction=0

        employee=Employee.objects.get(id=employee)
        Salary.objects.create(employee=employee,month=month,paid_salary=amount,type=type,leave_deduction=leave_deduction,tax_deduction=tax_deduction)
        return redirect('salary')
    else:
        return redirect('salary')