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
from zk import ZK, const
from datetime import datetime
from django.utils.timezone import make_aware


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
        months = MonthSetup.objects.all()

    # Create a list of dictionaries with month details and holiday count
        month_list = []
        for month in months:
            holidays = month.holidays.all()
            holiday_count = holidays.count()
            month_dict = {
                'month': month,
                'holidays': holidays,
                'holiday_count': holiday_count,
            }
            month_list.append(month_dict)

            
        holidays = Holidays.objects.all()
        year = YearSetup.objects.all()
        department = Department.objects.all()
        designation = Designation.objects.all()


        if DeviceData.objects.all().exists():
            device_data = DeviceData.objects.order_by('created')[0]
            can_add = False
        else:
            device_data = None
            can_add = True
        
        context = {
            'month_list':month_list, 
            'holidays':holidays, 
            'year':year,
            'department':department, 
            'designation':designation,
            'device_data':device_data,
            'can_add':can_add,
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
    
def edit_year(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            year = request.POST['year']
            year_obj = YearSetup.objects.get(id=id)
            year_obj.year=year
            year_obj.save()
            messages.info(request, "Year Edited Successfully")
            return redirect(hrm_setup)
        else:
            year_data = YearSetup.objects.get(id=id)
            context= {
                'year_data':year_data,
            }
            return render(request,'hrm/edit_year.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_year(request,id):
    if 'delete_hrm' in custom_data_views(request):
        year = YearSetup.objects.get(id=id)
        year.delete()
        messages.info(request, "Year Deleted")
        return redirect('hrm_setup')
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
            for holiday in date_list:
                Holidays.objects.create(month = month, holiday = holiday)

            messages.info(request, "Year Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def edit_month(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            year = request.POST['year']
            month = request.POST['month']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            holidays = request.POST['holidays']
            is_active = request.POST.get('is_active', 0)
            year = YearSetup.objects.get(id=year)

            month_obj = MonthSetup.objects.get(id=id)
            month_obj.year=year
            month_obj.month=month
            month_obj.start_date=start_date
            month_obj.end_date=end_date
            month_obj.is_active=is_active
            month_obj.save()

            prev_holidays = Holidays.objects.filter(month=id)
            prev_holidays.delete()
            date_list = [date.strip() for date in holidays.split(",")]
            for holiday in date_list:
                Holidays.objects.create(month = month_obj, holiday = holiday)

            messages.info(request, "Year Edited Successfully")
            return redirect(hrm_setup)
        else:
            year = YearSetup.objects.all()
            month_data = MonthSetup.objects.get(id=id)
            print(month_data.is_active)
            month_holidays = Holidays.objects.filter(month = month_data.id)
            context= {
                'year':year,
                'month_data':month_data,
                'month_holidays':month_holidays,
            }
            return render(request,'hrm/edit_month.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_month(request,id):
    if 'delete_hrm' in custom_data_views(request):
        month = MonthSetup.objects.get(id=id)
        month.delete()
        messages.info(request, "Month Deleted")
        return redirect('hrm_setup')
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


def edit_department(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            department = request.POST['department']
            department_obj = Department.objects.get(id=id)

            department_obj = Department.objects.get(id=id)
            department_obj.department=department
            department_obj.save()
            messages.info(request, "Department Edited Successfully")
            return redirect(hrm_setup)
        else:
            department_data = Department.objects.get(id=id)
            context= {
                'department_data':department_data,
            }
            return render(request,'hrm/edit_department.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_department(request,id):
    if 'delete_hrm' in custom_data_views(request):
        department = Department.objects.get(id=id)
        employee = Employee.objects.filter(department=department)
        if employee:
            messages.info(request, "Assign employees to another department to delete this department.")
            return redirect('hrm_setup')
        else:
            department.delete()
            messages.info(request, "Department Deleted")
            return redirect('hrm_setup')
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

def edit_designation(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            department = request.POST['department']
            designation = request.POST['designation']
            department = Department.objects.get(id=department)

            designation_obj = Designation.objects.get(id=id)
            designation_obj.department=department
            designation_obj.designation=designation
            designation_obj.save()
            messages.info(request, "Designation Edited Successfully")
            return redirect(hrm_setup)
        else:
            department = Department.objects.all()
            designation_data = Designation.objects.get(id=id)
            context= {
                'designation_data':designation_data,
                'department':department,
            }
            return render(request,'hrm/edit_designation.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_designation(request,id):
    if 'delete_hrm' in custom_data_views(request):
        designation = Designation.objects.get(id=id)
        employee = Employee.objects.filter(designation=designation)
        if employee:
            messages.info(request, "Assign employees to another designation to delete this designation.")
            return redirect('hrm_setup')
        else:
            designation.delete()
            messages.info(request, "Designation Deleted")
            return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def log_sheet(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = {

            }
            return render(request, 'hrm/log_sheet.html', context)
        else:
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
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
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
    if 'read_hrm' in custom_data_views(request):
        months = MonthSetup.objects.filter(is_active = True)      
        current_datetime = date.today()
        date_object = current_datetime
        today_date = date_object.strftime('%Y-%m-%d')
        all_employees = Employee.objects.all()
        recent_salary = Salary.objects.all().order_by('created')
        

        # paginator = Paginator(recent_salary, 10)
        # page_number = request.GET.get('page')
        # recent_salary = paginator.get_page(page_number)
        context = {
            'months':months,
            'today_date':today_date,
            'all_employees':all_employees,
            'recent_salary':recent_salary,
        }
        return render(request,'hrm/payroll.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def advance_salary(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            month = request.POST['month']
            employee = request.POST['employee']
            amount = request.POST['amount']
            adv_type = request.POST['adv_type']
            type='advance'
            leave_deduction=0
            tax_deduction=0
            employee=Employee.objects.get(id=employee)
            sel_month=MonthSetup.objects.get(month=month)
            salary_obj = Salary.objects.filter(employee=employee,month=sel_month,type='salary')
            if salary_obj:
                messages.info(request, "You have already paid the salary of this employee for this month. Please select another month for advance payment.")
            else:
                if adv_type == "addition":
                    Salary.objects.create(employee=employee,month=sel_month,paid_salary=amount,type=type,leave_deduction=leave_deduction,tax_deduction=tax_deduction)
                else:
                    print('HERE')
                    amount = float(amount) * -1
                    print(amount)
                    Salary.objects.create(employee=employee,month=sel_month,paid_salary=amount,type=type,leave_deduction=leave_deduction,tax_deduction=tax_deduction)

                messages.info(request, "Advance issued successfully.")

            return redirect('payroll')
        else:
            return redirect('payroll')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    






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
            pass_obj= password
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            permission=Permission.objects.get(role=role)
            designation = Designation.objects.get(id=designation)
            department = designation.department
            
            Employee.objects.create(user=user,emp_password=pass_obj,permission=permission,designation =designation,department =department,email =email,contact =contact,address =address,emp_salary =salary,date_joined = date_joined)
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
    if 'update_hrm' in custom_data_views(request):
        if request.method =="POST":
            designation = request.POST['designation']
            department = request.POST['department']
            contact = request.POST['contact']
            address = request.POST['address']
            salary = request.POST['salary']
            date_joined = request.POST.get('date_joined', '')
            
            password = request.POST['password']
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            role = request.POST['role']
            pass_obj= password


            user_data = Employee.objects.get(id=id)
            permission=Permission.objects.get(role=role)
            department=Department.objects.get(id=department)
            designation=Designation.objects.get(id=designation)

            emp_user = user_data.user
            user=User.objects.get(username = emp_user)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            if password:
                user.set_password(password)
            user.save()

            user_data.permission=permission
            user_data.designation = designation
            user_data.department = department
            user_data.contact = contact
            user_data.address = address
            user_data.emp_salary = salary
            user_data.email = email
            if password:
                user_data.emp_password=pass_obj
            if date_joined:
                user_data.date_joined = date_joined
            user_data.save()
            messages.info(request, "Employee Edited Successfully.")
            return redirect('employees')
        else:
            user_data = Employee.objects.get(id=id)
            designation = Designation.objects.all()
            department = Department.objects.all()
            roles = Role.objects.all()
            context={
                'user_data':user_data,
                'roles':roles,
                'designation':designation,
                'department':department,
            }
            return render (request,'hrm/edit_employees.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_employee(request,id):
    if 'delete_hrm' in custom_data_views(request):
        employee = Employee.objects.get(id=id)
        payments_made = Salary.objects.filter(employee=employee )
        context = {
            'employee':employee,
            'payments_made':payments_made,
            }
        return render(request,'hrm/view_employee.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
    
def delete_employee(request,id):
    if 'delete_hrm' in custom_data_views(request):
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
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = {
            }
            return render(request,'hrm/emp_payslip.html',context)
            
        else:
            employee = Employee.objects.get(user=request.user)
            payments_made = Salary.objects.filter(employee=employee )
            context = {
                'payments_made':payments_made,
                }
            return render(request,'hrm/emp_payslip.html',context)




def leave(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = {
            }
            return render (request,'hrm/leave.html',context)
        else:
            employee = Employee.objects.get(user=request.user)
            approved_leaves = Leave.objects.filter(employee=employee)
            approved_leave_dates = LeaveDate.objects.filter(leave__in=approved_leaves)
            context = {
                'approved_leaves':approved_leaves,
                'approved_leave_dates':approved_leave_dates
                }
            return render (request,'hrm/leave.html',context)
    

def apply_leave(request):
    if request.user.is_authenticated:
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
    if 'update_hrm' in custom_data_views(request):
        leave = Leave.objects.get(id=id)
        leave.status = 'accepted'
        leave.save()
        return redirect('emp_leaves')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def deny_leave(request,id):
    if 'update_hrm' in custom_data_views(request):
        leave = Leave.objects.get(id=id)
        leave.status = 'denied'
        leave.save()
        return redirect('emp_leaves')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def salary_payment(request):
    if 'read_hrm' in custom_data_views(request):
        if request.method =="POST":
            month = request.POST['month']
            employee = request.POST['employee']
            source = request.POST['source']

            selected_month = MonthSetup.objects.get(id=month)
            all_employees = Employee.objects.all()
            months = MonthSetup.objects.all()
            start_date = selected_month.start_date
            end_date = selected_month.end_date
            print(start_date,end_date)
            data_list=[]



            if source  == 'leaves':
                if employee == 'all':
                    all_emp = Employee.objects.all()
                    for emp_to_pay in all_emp:
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
                        holidays = Holidays.objects.filter(month=selected_month)
                        for holidays in holidays:
                            holiday_dates.append(holidays.holiday)
                        unpayable_holidays = [x for x in leave_days if x in holiday_dates]
                        total_month_dates = end_date-start_date
                        diff = total_month_dates.days+1
                        payable_days = diff-len(unpayable_holidays)-len(leave_days)

                        # payable_days = present_days+len(holiday_dates)-len(leave_days)
                        salary=emp_to_pay.emp_salary
                        emp_daily_salary = int(salary)/diff
                        salary_to_pay = emp_daily_salary*payable_days


                        
                        if salary_to_pay <= 41666.66:
                            tax_deduction = salary_to_pay * 0.01
                        elif salary_to_pay <= 58333.33:
                            tax_deduction = 500 + (salary_to_pay - 41666.66) * 0.1
                        elif salary_to_pay <= 83333.33:
                            tax_deduction = 2500 + (salary_to_pay - 58333.33) * 0.2
                        elif salary_to_pay <= 166666.67:
                            tax_deduction = 6500 + (salary_to_pay - 83333.33) * 0.3
                        else:
                            tax_deduction = 24166.67 + (salary_to_pay - 166666.67) * 0.36



                        leave_deduction = len(leave_days) * emp_daily_salary
                        advance_this_month =0
                        advance_obj = Salary.objects.filter(employee = emp_to_pay,type='advance',month=selected_month)
                        for adv in advance_obj:
                            print(adv.paid_salary)
                            advance_this_month = advance_this_month + adv.paid_salary
                        final_salary = salary_to_pay-tax_deduction-leave_deduction-advance_this_month
                        salary_status = Salary.objects.filter(employee = emp_to_pay,month=selected_month,type='salary')
                        if salary_status:
                            status='paid'
                        else:
                            status='unpaid'
                        
                        data_list.append({
                            'emp_id':emp_to_pay,
                            'month':selected_month.month,
                            'employee':str(emp_to_pay.user.first_name +' '+ emp_to_pay.user.last_name),
                            'present_days': present_days,
                            'absent_days':absent_days,
                            'payable_days':payable_days,
                            'salary':salary,
                            'final_salary':final_salary,
                            'tax_deduction':tax_deduction,
                            'leave_deduction':leave_deduction,
                            'status':status,
                            'advance_this_month':advance_this_month
                        })
                    context = {
                        'data_list':data_list,
                        'months':months,
                        'month':selected_month.month,
                        'all_employees':all_employees,
                    }
                
                
                
                else:
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
                    holidays = Holidays.objects.filter(month=selected_month)
                    for holidays in holidays:
                        holiday_dates.append(holidays.holiday)
                    unpayable_holidays = [x for x in leave_days if x in holiday_dates]
                    total_month_dates = end_date-start_date
                    diff = total_month_dates.days+1
                    payable_days = diff-len(unpayable_holidays)-len(leave_days)

                    # payable_days = present_days+len(holiday_dates)-len(leave_days)
                    salary=emp_to_pay.emp_salary
                    emp_daily_salary = int(salary)/diff
                    salary_to_pay = emp_daily_salary*payable_days



                    if salary_to_pay <= 41666.66:
                        tax_deduction = salary_to_pay * 0.01
                    elif salary_to_pay <= 58333.33:
                        tax_deduction = 500 + (salary_to_pay - 41666.66) * 0.1
                    elif salary_to_pay <= 83333.33:
                        tax_deduction = 2500 + (salary_to_pay - 58333.33) * 0.2
                    elif salary_to_pay <= 166666.67:
                        tax_deduction = 6500 + (salary_to_pay - 83333.33) * 0.3
                    else:
                        tax_deduction = 24166.67 + (salary_to_pay - 166666.67) * 0.36


                    leave_deduction = len(leave_days) * emp_daily_salary

                    advance_this_month = 0
                    advance_obj = Salary.objects.filter(employee = emp_to_pay,type='advance',month=selected_month)
                    print(advance_obj)
                    for adv in advance_obj:
                        advance_this_month = advance_this_month + adv.paid_salary
                    final_salary = salary_to_pay-tax_deduction-leave_deduction-advance_this_month
                    salary_status = Salary.objects.filter(employee = employee,month=selected_month,type='salary')
                    if salary_status:
                        status='paid'
                    else:
                        status='unpaid'

                    all_employees = Employee.objects.all()
                    months = MonthSetup.objects.all()
                    data_list.append({
                        'emp_id':emp_to_pay,
                        'month':selected_month.month,
                        'employee':str(emp_to_pay.user.first_name +' '+ emp_to_pay.user.last_name),
                        'present_days': present_days,
                        'absent_days':absent_days,
                        'payable_days':payable_days,
                        'salary':salary,
                        'final_salary':final_salary,
                        'tax_deduction':tax_deduction,
                        'leave_deduction':leave_deduction,
                        'status':status,
                        'advance_this_month':advance_this_month
                    })
                    context = {
                        'data_list':data_list,
                        'months':months,
                        'month':selected_month.month,
                        'all_employees':all_employees,
                    }
            elif source  == 'attendance_device':
                if employee == 'all':
                    all_emp = Employee.objects.all()
                    for emp_to_pay in all_emp:
                        attendance_employee = Employee.objects.get(id = emp_to_pay.id)

                        device_obj = DeviceAttendanceUser.objects.get(employee = attendance_employee)
                        attendance_record = DeviceAttendance.objects.filter(att_user=device_obj, date__range=(start_date, end_date))
                        present_days = attendance_record.count()
                        holiday_dates = []
                        holidays = Holidays.objects.filter(month=selected_month)
                        for holidays in holidays:
                            holiday_dates.append(holidays.holiday)

                        holiday_count  = Holidays.objects.filter(month=selected_month).count()
                        total_month_dates = end_date-start_date
                        diff = total_month_dates.days+1
                        payable_days = present_days +holiday_count

                        absent_days = diff - payable_days
                        salary=emp_to_pay.emp_salary
                        emp_daily_salary = int(salary)/diff
                        salary_to_pay = emp_daily_salary*diff
                        taxable_salary = emp_daily_salary*payable_days



                        if taxable_salary <= 41666.66:
                            tax_deduction = taxable_salary * 0.01
                        elif taxable_salary <= 58333.33:
                            tax_deduction = 500 + (taxable_salary - 41666.66) * 0.1
                        elif taxable_salary <= 83333.33:
                            tax_deduction = 2500 + (taxable_salary - 58333.33) * 0.2
                        elif taxable_salary <= 166666.67:
                            tax_deduction = 6500 + (taxable_salary - 83333.33) * 0.3
                        else:
                            tax_deduction = 24166.67 + (taxable_salary - 166666.67) * 0.36



                        leave_days = diff - payable_days
                        leave_deduction = leave_days * emp_daily_salary
                        advance_this_month =0
                        advance_obj = Salary.objects.filter(employee = emp_to_pay,type='advance',month=selected_month)
                        for adv in advance_obj:
                            advance_this_month = advance_this_month + adv.paid_salary
                        final_salary = salary_to_pay-tax_deduction-leave_deduction-advance_this_month
                        salary_status = Salary.objects.filter(employee = emp_to_pay,month=selected_month,type='salary')
                        if salary_status:
                            status='paid'
                        else:
                            status='unpaid'
                        
                        data_list.append({
                            'emp_id':emp_to_pay,
                            'month':selected_month.month,
                            'employee':str(emp_to_pay.user.first_name +' '+ emp_to_pay.user.last_name),
                            'present_days': present_days,
                            'absent_days':absent_days,
                            'payable_days':payable_days,
                            'salary':salary,
                            'final_salary':final_salary,
                            'tax_deduction':tax_deduction,
                            'leave_deduction':leave_deduction,
                            'status':status,
                            'advance_this_month':advance_this_month
                        })
                    context = {
                        'data_list':data_list,
                        'months':months,
                        'month':selected_month.month,
                        'all_employees':all_employees,
                    }
                else:
                    attendance_employee = Employee.objects.get(id = employee)

                    device_obj = DeviceAttendanceUser.objects.get(employee = attendance_employee)
                    attendance_record = DeviceAttendance.objects.filter(att_user=device_obj, date__range=(start_date, end_date))
                    present_days = attendance_record.count()
                    holiday_dates = []
                    holidays = Holidays.objects.filter(month=selected_month)
                    for holidays in holidays:
                        holiday_dates.append(holidays.holiday)

                    holiday_count  = Holidays.objects.filter(month=selected_month).count()
                    total_month_dates = end_date-start_date
                    diff = total_month_dates.days+1
                    payable_days = present_days + holiday_count

                    absent_days = diff - payable_days
                    salary=attendance_employee.emp_salary
                    emp_daily_salary = int(salary)/diff
                    salary_to_pay = emp_daily_salary*diff
                    taxable_salary = emp_daily_salary*payable_days



                    if taxable_salary <= 41666.66:
                        tax_deduction = taxable_salary * 0.01
                    elif taxable_salary <= 58333.33:
                        tax_deduction = 500 + (taxable_salary - 41666.66) * 0.1
                    elif taxable_salary <= 83333.33:
                        tax_deduction = 2500 + (taxable_salary - 58333.33) * 0.2
                    elif taxable_salary <= 166666.67:
                        tax_deduction = 6500 + (taxable_salary - 83333.33) * 0.3
                    else:
                        tax_deduction = 24166.67 + (taxable_salary - 166666.67) * 0.36




                    leave_days = diff - payable_days
                    leave_deduction = leave_days * emp_daily_salary
                    advance_this_month =0
                    advance_obj = Salary.objects.filter(employee = attendance_employee,type='advance',month=selected_month)
                    for adv in advance_obj:
                        advance_this_month = advance_this_month + adv.paid_salary

                    print(salary_to_pay,leave_deduction,advance_this_month,tax_deduction)
                    final_salary = salary_to_pay-tax_deduction-leave_deduction-advance_this_month
                    salary_status = Salary.objects.filter(employee = attendance_employee,month=selected_month,type='salary')
                    if salary_status:
                        status='paid'
                    else:
                        status='unpaid'

                    all_employees = Employee.objects.all()
                    months = MonthSetup.objects.all()
                    
                    data_list.append({
                        'emp_id':attendance_employee,
                        'month':selected_month.month,
                        'employee':str(attendance_employee.user.first_name +' '+ attendance_employee.user.last_name),
                        'present_days': present_days,
                        'absent_days':absent_days,
                        'payable_days':payable_days,
                        'salary':salary,
                        'final_salary':final_salary,
                        'tax_deduction':tax_deduction,
                        'leave_deduction':leave_deduction,
                        'status':status,
                        'advance_this_month':advance_this_month
                    })
                    context = {
                        'data_list':data_list,
                        'months':months,
                        'month':selected_month.month,
                        'all_employees':all_employees,
                    }
            else:
                context=None
                return redirect('payroll')
        return render(request,'hrm/salary_payment.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def pay_salary(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            selected_employees = request.POST.getlist("selected_employees")
            leave_deduction = request.POST.getlist("leave_deduction")
            tax_deduction = request.POST.getlist("tax_deduction")
            final_salary = request.POST.getlist("final_salary")
            month = request.POST["month"]
            print(month)
            company_deduction = request.POST.getlist("company_deduction")
            for i in range(len(selected_employees)):
                employee=Employee.objects.get(id=selected_employees[i])
                month=MonthSetup.objects.get(month=month)
                salary = Salary.objects.create(
                    employee=employee,
                    month=month,
                    leave_deduction=leave_deduction[i],
                    tax_deduction=tax_deduction[i],
                    company_deduction=company_deduction[i],
                    paid_salary=final_salary[i],
                    type='salary',
                )
                salary.save()
            return redirect('payroll')      
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    





def add_device_data(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method=="POST":
            ip_address = request.POST['ip_address']
            port = request.POST['port']
            data = DeviceData.objects.create(ip_address=ip_address, port=port)
            data.save()
            return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_device_data(request,id):
    if 'manage_hrm' in custom_data_views(request):
        if request.method=="POST":
            ip_address = request.POST['ip_address']
            port = request.POST['port']
            data = DeviceData.objects.get(id=id)
            data.ip_address = ip_address
            data.port = port
            data.save()
            return redirect('hrm_setup')
        else:
            device_data = DeviceData.objects.get(id=id)
            return render (request, 'hrm/edit_device_data.html', {'device_data':device_data})
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def delete_device_data(request,id):
    if 'delete_hrm' in custom_data_views(request):
        device_data = DeviceData.objects.get(id=id)
    
        device_data.delete()
        messages.info(request, "Device Data Deleted")
        return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def device_attendance(request):
    today = datetime.today().strftime('%Y-%m-%d')
    
    att_user_data = DeviceAttendanceUser.objects.all().order_by('uid')
    att_user_att_data = DeviceAttendance.objects.filter(date = today).order_by('-punchin_timestamp')
    # shuvam = DeviceAttendanceUser.objects.get(uid=11)
    # all_attendance = DeviceAttendance.objects.filter(att_user = shuvam)
    all_attendance = DeviceAttendance.objects.all().order_by('-date', '-punchin_timestamp')[:30]
    employee = Employee.objects.all()
    context = {
        'att_user_att_data':att_user_att_data,
        'att_user_data':att_user_data,
        'all_attendance':all_attendance,
        'employee':employee,
    }
    return render (request, 'hrm/device_attendance.html',context)


def get_zkusers(request):
    conn = None
    device_data = DeviceData.objects.all()[:1].get()
    ip = device_data.ip_address
    port = int(device_data.port)
    zk = ZK(ip, port=port, timeout=5)
    
    try:
        conn = zk.connect()
        users = conn.get_users()
        
        for user in users:
            deviceuser, created = DeviceAttendanceUser.objects.get_or_create(uid=user.uid, defaults={'name': user.name})
            if created:
                deviceuser.save()

    except Exception as e:
        print("Exception occurred: ", e)

    finally:
        if conn:
            conn.disconnect()
    return redirect('device_attendance')




from django.db.models import Max
from datetime import datetime

def get_zkattendance(request):
    conn = None
    device_data = DeviceData.objects.all()[:1].get()
    ip = device_data.ip_address
    port = int(device_data.port)
    
    zk = ZK(ip, port=port, timeout=5)
    try:
        conn = zk.connect()
        attendances = conn.get_attendance()
        
        # Get the latest attendance date from DeviceAttendance model
        latest_attendance_date = DeviceAttendance.objects.aggregate(max_date=Max('date'))['max_date']

        if latest_attendance_date is None:
            latest_attendance_date = datetime.min.date()

        attendance_data = [a for a in attendances if a.timestamp.date() >= latest_attendance_date]

        
        # Filter the attendance data to include only records after the latest attendance date
        attendance_data = [a for a in attendances if a.timestamp.date() >= latest_attendance_date]
        
        # Loop through the attendance data and update the DeviceAttendance model as needed
        for attendance in attendance_data:
            user_id = attendance.user_id
            punch_time = attendance.timestamp
            punch_time = make_aware(punch_time)  
            attendance_date = punch_time.date()
            
            try:
                # Get the DeviceAttendance object for the user and date
                att_data = DeviceAttendance.objects.get(att_user__uid=user_id, date=attendance_date)
                
                # If the punchout time has not been recorded, update it
                if att_data.punchout_timestamp is None:
                    if att_data.punchin_timestamp != punch_time.time():
                        att_data.punchout_timestamp = punch_time.time()
                        att_data.save()
                else:
                    # If the punchout time has already been recorded, update it only if the new time is later
                    att_data.punchout_timestamp = max(att_data.punchout_timestamp, punch_time.time())
                    att_data.save()
                    
            except DeviceAttendance.DoesNotExist:
                try:
                    att_user = DeviceAttendanceUser.objects.get(uid=user_id)
                except DeviceAttendanceUser.DoesNotExist:
                    att_user = DeviceAttendanceUser.objects.create(uid=user_id)
                
                # Create a new DeviceAttendance object if one does not already exist for the user and date
                DeviceAttendance.objects.create(att_user=att_user, date=attendance_date, punchin_timestamp=punch_time.time())

    except Exception as e:
        print("Exception occurred: ", e)

    finally:
        if conn:
            conn.disconnect()
    
    return redirect('device_attendance')




def edit_att_user(request,id):
    if 'manage_hrm' in custom_data_views(request):
        if request.method=="POST":
            name = request.POST['name']
            emp_id = request.POST['employee']
            employee = Employee.objects.get(id=emp_id)
            data = DeviceAttendanceUser.objects.get(id=id)
            data.employee=employee
            data.name = name
            data.save()
            return redirect('device_attendance')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def delete_att_user(request,id):
    if 'delete_hrm' in custom_data_views(request):
        device_user_data = DeviceAttendanceUser.objects.get(id=id)
    
        device_user_data.delete()
        messages.info(request, "Device User Deleted")
        return redirect('device_attendance')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
