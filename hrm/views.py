from django.shortcuts import render,redirect
from .models import *
from features.models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
import datetime
from django.core.paginator import Paginator

from account.context_processors import custom_data_views
# Create your views here.

def hrm(request):
    if 'read_hrm' in custom_data_views(request):
        att_data=LogSheet.objects.all()
        context = {
            'att_data':att_data,
        }
        return render (request,'hrm/hrm.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def hrm_setup(request):
    if 'read_hrm' in custom_data_views(request):
        month = MonthSetup.objects.all()
        holidays = Holidays.objects.all()
        year = YearSetup.objects.all()
        department = Department.objects.all()
        designation = Designation.objects.all()
        context = {
            'month':month, 
            'holidays':holidays, 
            'year':year,
            'department':department, 
            'designation':designation,
        }
        return render (request,'hrm/hrm_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_year(request):
    if 'create_hrm' in custom_data_views(request):
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
        return redirect('home')
    

def add_month(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            year = request.POST['year']
            month = request.POST['month']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            holidays = request.POST['holidays']

            year = YearSetup.objects.get(id=year)
            month = MonthSetup.objects.create(year=year,month=month,start_date=start_date,end_date=end_date)
            month.save()
            date_list = [date.strip() for date in holidays.split(",")]
            print(date_list)
            for holiday in date_list:
                Holidays.objects.create(month = month, holiday = holiday)

            messages.info(request, "Year Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def add_department(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            department = request.POST['department']
            Department.objects.create(department=department)
            messages.info(request, "Department Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_designation(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            department = request.POST['department']
            designation = request.POST['designation']
            department = Department.objects.get(id=department)
            Designation.objects.create(department=department,designation=designation)
            messages.info(request, "Designation Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def attendance (request):
    if 'read_hrm' in custom_data_views(request):
        att_data=LogSheet.objects.all()
        context = {
            'att_data':att_data,
        }
        return render (request, 'hrm/attendance.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

    

def salary (request):
    if 'create_hrm' in custom_data_views(request):
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
                    

            all_employees = Employee.objects.all()
            context={
                'months':months,
                'monthhhh':monthhhh,
                'data_list':data_list,
                'from_date_obj':from_date_obj,
                'to_date_obj':to_date_obj,
                'today_date':today_date,
                'all_employees':all_employees,
            }

            return render(request,'hrm/salary.html',context)

        else:
            months = MonthSetup.objects.all()
            current_datetime = datetime.date.today()
            date_object = current_datetime
            today_date = date_object.strftime('%Y-%m-%d')
            all_employees = Employee.objects.all()
            recent_salary = Salary.objects.all().order_by('created')
            paginator = Paginator(recent_salary, 10)
            page_number = request.GET.get('page')
            recent_salary = paginator.get_page(page_number)
            context = {
                'months':months,
                'today_date':today_date,
                'all_employees':all_employees,
                'recent_salary':recent_salary,
            }
            return render(request,'hrm/salary.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')







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
    






def employees(request):
    if 'read_hrm' in custom_data_views(request):
        employees = Employee.objects.all()
        context = {
            'employees':employees,
        }
        return render (request,'hrm/employees.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def add_employee(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method=="POST":
            designation = request.POST['designation']
            department = request.POST['department']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            salary = request.POST['salary']
            date_joined = request.POST['date_joined']
            

            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            role = request.POST['role']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            permission=Permission.objects.get(role=role)
            designation = Designation.objects.get(id=designation)
            department = designation.department
            
            Employee.objects.create(user=user,permission=permission,designation =designation,department =department,email =email,contact =contact,address =address,emp_salary =salary,date_joined = date_joined)
            messages.info(request, "Employee Added Successfully")

            return redirect('employees')
        else:
            designation = Designation.objects.all()
            department = Department.objects.all()
            roles = Role.objects.all()
            context = {
            'roles':roles,
            'designation':designation,
            'department':department,
        }
            return render(request,'hrm/add_employee.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_employee(request,id):
    if 'update_account' in custom_data_views(request):
        if request.method =="POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            role = request.POST['role']
            user_data = Employee.objects.get(id=id)
            permission=Permission.objects.get(role=role)

            user = User.objects.get(username=username)
            user.username=username
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            user_data.permission=permission
            user_data.save()
            return redirect('company_user')
        else:
            user_data = Employee.objects.get(id=id)
            roles = Role.objects.all()
            context={
                'user_data':user_data,
                'roles':roles,
            }
            return render (request,'account/edit_company_user.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_employee(request,id):
    if 'delete_account' in custom_data_views(request):
        user_data = Employee.objects.get(id=id)
        user = User.objects.get(username=user_data.user.username)
        print(user)
        if (user.is_superuser==True):
            messages.info(request, "This user can't be deleted.")
        else:
            user.delete()
            user_data.delete()
            messages.info(request, "User Deleted Successfully")
        return redirect('employees')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    





# def add_leave(request):
#     if 'create_hrm' in custom_data_views(request):
#         if request.method=="POST":
#             reason = request.POST['reason']
#             emp = request.POST['employee']
#             employe = Employee.objects.get(id=emp)
#             current_datetime = datetime.date.today()
#             print(current_datetime)

#             if Leave.objects.filter(employee = employe):
#                 leaves = Leave.objects.filter(employee = employe).order_by('-created')[0]
#                 print(leaves.created)
#             else:
#                 leaves=None

#             if leaves:
#                 if leaves.created ==current_datetime:
#                     messages.info(request,f"Already added for today ({current_datetime})")
#                     return redirect('attendance')
#                 else:
#                     Leave.objects.create(employee=employe,reason =reason)
#                     messages.info(request, "Leave Added Successfully")
#                     return redirect('attendance')
#             else:
#                 Leave.objects.create(employee=employe,reason =reason)
#                 messages.info(request, "Leave Added Successfully")
#                 return redirect('attendance')
#         else:
#             return redirect('attendance')
#     else:
#         messages.info(request, "Unauthorized access.")
#         return redirect('home')
    



