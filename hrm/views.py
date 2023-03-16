from django.shortcuts import render,redirect
from .models import *
from features.models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from datetime import date,datetime,timedelta
from django.core.paginator import Paginator
from account.context_processors import custom_data_views
# Create your views here.
from django.db.models import Count



def hrm(request):
    if 'read_hrm' in custom_data_views(request):

        stats = []
        employee = Employee.objects.all().count()
        # present_today = LogSheet.objects.filter(created = date.today()).count()
        present_today = LogSheet.objects.filter(created=date.today()) \
                    .values('user') \
                    .annotate(count=Count('id', distinct=True)) \
                    .count()
        absent_today = employee-present_today
        department = Department.objects.all().count()
        stats.append({
                'employee': employee,
                'present_today': present_today,
                'absent_today': absent_today,
                'department': department,
            })
        stats = stats[0]
        print(stats)
        context = {
            'stats':stats,
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



def log_sheet(request):
    if request.user.is_authenticated:
        logged_in_employee = Employee.objects.get(user=request.user)
        current_log = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).first()
        punched_in = False
        punched_out = False
        today_logs = None
        
        if current_log:
            if current_log.punch_out_time is None:
                punched_in = True
            else:
                punched_out = True
                today_logs = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).order_by('-punch_in_time').first()
        
        time_now = datetime.now().time()
        
        context = {
            'time_now': time_now,
            'today_logs': today_logs,
            'punched_in': punched_in,
            'punched_out': punched_out,
        }
        return render(request, 'hrm/log_sheet.html', context)
    else:
        return redirect('login')


def punch_in(request):
    if request.method == 'POST':
        logged_in = Employee.objects.get(user=request.user)
        today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

        current_date = date.today()
        leave_dates = LeaveDate.objects.filter(date=current_date)
        employees_on_leave = [leave_date.leave.employee for leave_date in leave_dates]

        # employee = Employee.objects.get(id=1)  # Replace with the appropriate employee ID
        is_on_leave = logged_in in employees_on_leave
        if is_on_leave:
            messages.info(request, "You are on leave for today.")
            return redirect('log_sheet')
        else:
            if today_logs.exists():
                messages.info(request, "You have already punched in for today.")
                return redirect('log_sheet')
            else:
                punch = LogSheet(user=logged_in, punch_in_time=datetime.now().time())
                punch.save()
                messages.success(request, "Punched in successfully.")
                return redirect('log_sheet')
    return redirect('log_sheet')


def punch_out(request):
    if request.method == 'POST':
        logged_in = Employee.objects.get(user=request.user)
        today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

        if today_logs.exists() and today_logs.latest('punch_in_time').punch_out_time:
            # User has already punched out for the day, redirect to punch in page
            messages.info(request, "You have already punched out for today.")
            return redirect('punch_in')
        elif today_logs.exists():
            # Update the latest LogSheet instance with user's tasks, meetings, and remarks and punch out time
            punch = today_logs.latest('punch_in_time')
            punch.punch_out_time = datetime.now().time()
            punch.tasks = request.POST['tasks']
            punch.meetings = request.POST['meetings']
            punch.remarks = request.POST['remarks']
            punch.save()
            messages.success(request, "Punched out successfully.")
            return redirect('punch_in')
        else:
            # User has not punched in for the day, redirect to punch in page
            messages.info(request, "You need to punch in before punching out.")
            return redirect('punch_in')
    return redirect('log_sheet')


def attendance (request):
    if 'read_hrm' in custom_data_views(request):
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            employee_id = request.POST.get('employee')
            start_date=start_date
            end_date=end_date
            if employee_id == 'all':
                att_data = LogSheet.objects.filter(created__range=[start_date, end_date])
            else:
                att_data = LogSheet.objects.filter(user_id=employee_id, created__range=[start_date, end_date])
            employees = Employee.objects.all()
            searched = True
            context = {
            'start_date':start_date,
            'end_date':end_date,
            'att_data':att_data,
            'employees':employees,
            'searched':searched
        }
            return render(request, 'hrm/attendance.html',context)
        else:
            att_data=LogSheet.objects.all()
            employees = Employee.objects.all()
            context = {
                'att_data':att_data,
                'employees':employees
            }
            return render (request, 'hrm/attendance.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def payroll(request):
    months = MonthSetup.objects.all()
    current_datetime = date.today()
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
    return render(request,'hrm/payroll.html',context)


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
        return redirect('payroll')
    else:
        return redirect('payroll')
    






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
    
def emp_payslip(request):
    employee = Employee.objects.get(user=request.user)
    payments_made = Salary.objects.filter(employee=employee )
    context = {
        'payments_made':payments_made,
        }
    return render(request,'hrm/emp_payslip.html',context)




def leave(request):
    employee = Employee.objects.get(user=request.user)
    approved_leaves = Leave.objects.filter(employee=employee)
    approved_leave_dates = LeaveDate.objects.filter(leave__in=approved_leaves)
    context = {
        'approved_leaves':approved_leaves,
        'approved_leave_dates':approved_leave_dates
        }
    return render (request,'hrm/leave.html',context)
    

def apply_leave(request):
    if request.method == "POST":
        reason = request.POST['reason']
        dates = request.POST['daterange']
        employee = Employee.objects.get(user=request.user)
        leave = Leave.objects.create(reason=reason,status='pending',employee=employee)
        leave.save()


        start_date_str, end_date_str = dates.split(" - ")
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
        end_date = datetime.strptime(end_date_str, "%m/%d/%Y").date()
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date)
            current_date += timedelta(days=1)

        for date in date_list:
            LeaveDate.objects.create(leave=leave,date=date)

        return redirect('leave')
    else:
        return redirect('leave')


def emp_leaves(request):
    if 'read_hrm' in custom_data_views(request):
        employees =Employee.objects.all()
        pending_leaves = Leave.objects.filter(status='pending')
        pending_leaves_dates = LeaveDate.objects.filter(leave__in=pending_leaves)

        approved_leaves = Leave.objects.filter(status='accepted')
        approved_leaves_dates = LeaveDate.objects.filter(leave__in=approved_leaves)
        
        denied_leaves = Leave.objects.filter(status='denied')
        denied_leaves_dates = LeaveDate.objects.filter(leave__in=denied_leaves)

        context = {
            'employees':employees,
            'pending_leaves':pending_leaves,
            'pending_leaves_dates':pending_leaves_dates,

            'approved_leaves':approved_leaves,
            'approved_leaves_dates':approved_leaves_dates,
            
            'denied_leaves':denied_leaves,
            'denied_leaves_dates':denied_leaves_dates,
        }
        return render (request,'hrm/emp_leaves.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def add_emp_leave(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method=="POST":
            emp = request.POST['employee']
            reason = request.POST['reason']
            days = request.POST['dates']
            employee = Employee.objects.get(id=emp)
            date_list = [date.strip() for date in days.split(",")]
            leave = Leave.objects.create(reason=reason,status='accepted',employee=employee)
            leave.save()
            for date in date_list:
                LeaveDate.objects.create(leave=leave,date=date)
            return redirect('emp_leaves')
        else:
            return redirect('emp_leaves')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def accept_leave(request,id):
    leave = Leave.objects.get(id=id)
    leave.status = 'accepted'
    leave.save()
    return redirect('emp_leaves')

def deny_leave(request,id):
    leave = Leave.objects.get(id=id)
    leave.status = 'denied'
    leave.save()
    return redirect('emp_leaves')
    

def salary_payment(request):
    if request.method =="POST":
        month = request.POST['month']
        employee = request.POST['employee']
        selected_month = MonthSetup.objects.get(id=month)
        start_date = selected_month.start_date
        end_date = selected_month.end_date

        if employee == 'all':
            pass
        else:
            data_list=[]
            emp_to_pay = Employee.objects.get(id = employee)
            
            logs = LogSheet.objects.filter(user=emp_to_pay.id, created__range=(start_date, end_date))
            present_days = logs.count()

            leaves = Leave.objects.filter(employee = emp_to_pay,status='accepted')
            absent_days = 0
            leave_days =[]
            for leave in leaves:
                leave_dates = LeaveDate.objects.filter(leave=leave)
                for leave_date in leave_dates:
                    if start_date <= leave_date.date <= end_date:
                        absent_days += 1
                        leave_days.append(leave_date.date)
            
            holiday_dates = []
            holidays = Holidays.objects.filter(month=month)
            for holidays in holidays:
                holiday_dates.append(holidays.holiday)

            payable = [x for x in holiday_dates if x not in leave_days]
            unpayable_holidays = [x for x in leave_days if x in holiday_dates]

            # date1 = datetime(start_date)
            # date2 = datetime(end_date)
            total_month_dates = end_date-start_date
            diff = total_month_dates.days
            print(diff)
            payable_days = diff-len(unpayable_holidays)
            print(payable_days)
        context = {
            'holiday_dates':holiday_dates,
            'unpayable':unpayable_holidays,
         }
    return render(request,'hrm/salary_payment.html',context)