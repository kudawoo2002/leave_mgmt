
from django.shortcuts import render, redirect
from .models import Leave, LeaveType, Employee, Department, Status, Gender
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Count
# Create your views here.


def index(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'site/index.html')
    return render(request, 'site/index.html')


def logout_page(request):
    logout(request)
    return render(request, 'site/logout.html')


@login_required(login_url='index')
def dashboard(request):
    leave_pending = Leave.objects.filter(
        leave_status__name__icontains='Pending').count()
    print(leave_pending)
    count_emp_per_dept = Employee.objects.values(
        'dept_name').annotate(count=Count('dept_name'))
    user_id = request.user.id

    leave_bal = 0

    try:
        leave_bal = Leave.objects.filter(
            username=user_id).order_by('-applied_date')[0]

    except:
        pass

    # print(leave_balance.leave_balance)
    # for item in count_emp_per_dept:
    #     print(item)
    employees = Employee.objects.all()
    count_emp = employees.count()
    depts = Department.objects.all()
    count_dept = depts.count()

    context = {
        'count_emp': count_emp,
        'count_dept': count_dept,
        'leave_bal': leave_bal,
        'leave_pending': leave_pending,

    }
    return render(request, 'site/dashboard.html', context)


@ login_required(login_url='index')
def leave_req(request):
    leaves = Leave.objects.all()
    leave_type = LeaveType.objects.all()
    employees = Employee.objects.all()
    current_user = request.user
    leave_status = Status.objects.all()

    context = {
        'leave_type': leave_type,
        'employees': employees,
        'current_user': current_user,
        # 'single_leave': single_leave,
        'leave_status': leave_status,
    }

    if request.method == 'POST':

        annual_total_leave = int(request.POST.get('annual_leave'))
        username_id = request.user.id
        username = User.objects.get(pk=username_id)
        full_name = request.POST.get("full_name")
        d = request.POST.get("start_date")
        start_date = datetime.strptime(d, "%Y-%m-%d")
        x = request.POST.get("end_date")
        end_date = datetime.strptime(x, "%Y-%m-%d")
        n_of_day = request.POST.get('n_of_day')
        leave_type_id = request.POST.get('leave_type')
        leave_type = LeaveType.objects.get(pk=leave_type_id)
        reason = request.POST.get('reason')
        leave_status_id = request.POST.get('leave_status')
        leave_status = Status.objects.get(pk=leave_status_id)
        d = Leave(username=username, full_name=full_name, start_date=start_date, end_date=end_date,
                  numberof_days=n_of_day, leavetype=leave_type, leave_comment=reason, leave_status=leave_status, annual_total_leave=annual_total_leave)

        d.save()
        return redirect('leave-report')

    return render(request, 'site/leave-req.html', context)


@ login_required(login_url='index')
def leave_report(request):
    reports = Leave.objects.all()
    user_report = Leave.objects.filter(username=request.user)
    context = {
        'reports': reports,
        'user_report': user_report,
    }
    return render(request, 'site/leave_report.html', context)


@ login_required(login_url='index')
def leave_pend_report(request):
    pending_leave = Leave.objects.filter(
        leave_status__name__icontains='Pending')
    for i in range(len(pending_leave)):
        print(pending_leave[i].pk)
    user_report = Leave.objects.filter(username=request.user)
    context = {
        'pending_leave': pending_leave,
    }
    return render(request, 'site/leave_report.html', context)


@ login_required(login_url='index')
def leave_detail(request, pk):
    leave_detail = Leave.objects.get(pk=pk)
    context = {
        'leave_detail': leave_detail,
    }
    return render(request, 'site/leave_detail.html', context)


@ login_required(login_url='index')
def leave_edit(request, pk):
    leave_edit = Leave.objects.get(pk=pk)
    leave_status = Status.objects.all()
    leave_type = LeaveType.objects.all()
    context = {
        'leave_edit': leave_edit,
        'leave_status': leave_status,
        'leave_type': leave_type,
    }
    if request.method == 'POST':

        annual_total_leave = int(request.POST.get('annual_leave'))
        username_id = request.POST.get('username')
        username = User.objects.get(pk=username_id)
        full_name = request.POST.get("full_name")
        d = request.POST.get("start_date")
        start_date = datetime.strptime(d, "%Y-%m-%d")
        x = request.POST.get("end_date")
        end_date = datetime.strptime(x, "%Y-%m-%d")
        n_of_day = request.POST.get('n_of_day')
        leave_type_id = request.POST.get('leavetype')
        leavetype = LeaveType.objects.get(pk=leave_type_id)

        comment = request.POST.get('reason')
        leave_status_id = request.POST.get('leavestatus')
        leavestatus = Status.objects.get(pk=leave_status_id)
        leave_edit.annual_total_leave = annual_total_leave
        leave_edit.username = username
        leave_edit.full_name = full_name
        leave_edit.start_date = start_date
        leave_edit.end_date = end_date
        leave_edit.leavetype = leavetype
        leave_edit. leave_status = leavestatus
        leave_edit.leave_comment = comment
        leave_edit.save()
        return redirect('leave-report')

    return render(request, 'site/leave_edit.html', context)


@ login_required(login_url='index')
def leave_del(request, pk):
    leave_del = Leave.objects.get(pk=pk)

    context = {
        'leave_del': leave_del,
    }
    if request.method == 'POST':
        leave_del.delete()
        return redirect('leave-report')
    return render(request, 'site/leave_delete.html', context)


@ login_required(login_url='index')
def leave_type(request):
    if request.method == 'POST':
        leave_name = request.POST["leavetype"]
        data = LeaveType(name=leave_name)
        data.save()
        return redirect('leave-type-report')
    else:
        return render(request, 'site/leavetype.html')
    return render(request, 'site/leavetype.html')


@ login_required(login_url='index')
def leavetype_report(request):
    leavetype_report = LeaveType.objects.all()
    context = {
        'leavetype_report': leavetype_report,
    }
    return render(request, 'site/leavetype-report.html', context)


@ login_required(login_url='index')
def del_leav_type(request, pk):
    del_leave = LeaveType.objects.get(pk=pk)

    context = {
        'del_leave': del_leave,
    }
    if request.method == 'POST':
        del_leave.delete()
        return redirect('leave-type-report')
    return render(request, 'site/leavetype_del.html', context)


@ login_required(login_url='index')
def edite_leave_type(request, pk):
    leavetype_edit = LeaveType.objects.get(pk=pk)
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        leavetype_edit.name = leavetype
        leavetype_edit.save()
        return redirect('leave-type-report')
    context = {
        'leavetype_edit': leavetype_edit,
    }

    return render(request, 'site/leavtype_edit.html', context)


@ login_required(login_url='index')
def leavetype_detail(request, pk):
    leavetype_detail = LeaveType.objects.get(pk=pk)

    context = {
        'leavetype_detail': leavetype_detail,
    }
    return render(request, 'site/leave_type_detail.html', context)


@ login_required(login_url='index')
def employee(request):
    depts = Department.objects.all()
    username_id = request.user.id
    username = User.objects.get(pk=username_id)
    users = User.objects.all()
    genders = Gender.objects.all()

    context = {
        'depts': depts,
        'username': username,
        'users': users,
        'genders': genders,
    }
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        middlename = request.POST['middlename']
        empcode = request.POST['empcode'].upper()
        username_id = request.POST.get('username')
        username = User.objects.get(pk=username_id)
        gender_id = request.POST.get('gender')
        gender = Gender.objects.get(pk=gender_id)
        address = request.POST['address']
        city = request.POST['city']
        email = request.POST['email']
        phone = request.POST['phone']
        d = request.POST.get('dob')
        dob = datetime.strptime(d, "%Y-%m-%d")
        nationality = request.POST['nationality']
        st = request.POST.get('start_date')
        start_date = datetime.strptime(st, '%Y-%m-%d')
        department_id = request.POST.get('department')
        department = Department.objects.get(pk=department_id)
        emp_image = request.FILES.get('emp_image')
        # is_active = request.POST.get('is_active')
        data = Employee(first_name=fname, last_name=lname, middle_name=middlename, emp_code=empcode, emp_gender=gender, emp_address=address,
                        city=city, emp_phone=phone, email_address=email, emp_nationality=nationality, dept_name=department, emp_picture=emp_image, username=username, dob=dob, started_date=start_date)
        data.save()
        return redirect('employee-report')

    return render(request, 'site/employee.html', context)


@ login_required(login_url='index')
def employee_report(request):
    # employee_report = Employee.objects.all()
    employee_report = Employee.objects.filter(is_active=True)
    context = {
        'employee_report': employee_report,
    }
    return render(request, 'site/employee_report.html', context)


@ login_required(login_url='index')
def employee_detail(request, pk):
    emp_detail = Employee.objects.get(pk=pk)
    context = {
        'emp_detail': emp_detail,
    }
    return render(request, 'site/employee_detail.html', context)


@ login_required(login_url='index')
def employee_edit(request, pk):
    emp_edit = Employee.objects.get(pk=pk)
    users = User.objects.all()
    genders = Gender.objects.all()
    depts = Department.objects.all()
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        middlename = request.POST['middlename']
        empcode = request.POST['empcode'].upper()
        username_id = request.POST.get('username')
        username = User.objects.get(pk=username_id)
        gender_id = request.POST.get('gender')
        gender = Gender.objects.get(pk=gender_id)
        address = request.POST['address']
        city = request.POST['city']
        email = request.POST['email']
        phone = request.POST['phone']
        d = request.POST.get('dob')
        dob = datetime.strptime(d, "%Y-%m-%d")
        nationality = request.POST['nationality']
        st = request.POST.get('start_date')
        start_date = datetime.strptime(st, '%Y-%m-%d')
        department_id = request.POST.get('department')
        department = Department.objects.get(pk=department_id)
        emp_image = request.FILES.get('emp_image')

        emp_edit.username = username
        emp_edit.first_name = fname
        emp_edit.last_name = lname
        emp_edit.middle_name = middlename
        emp_edit.dob = dob
        emp_edit.emp_code = empcode
        emp_edit.emp_gender = gender
        emp_edit.emp_picture = emp_image
        emp_edit.emp_address = address
        emp_edit.city = city
        emp_edit.emp_phone = phone
        emp_edit.email_address = email
        emp_edit.emp_nationality = nationality
        emp_edit.dept_name = department
        emp_edit.started_date = start_date
        emp_edit.save()
        return redirect('employee-report')

    context = {
        'emp_edit': emp_edit,
        'users': users,
        'genders': genders,
        'depts': depts,
    }
    return render(request, 'site/employee-edit.html', context)


@ login_required(login_url='index')
def emp_del(request, pk):
    emp_del = Employee.objects.get(pk=pk)

    context = {
        'emp_del': emp_del,
    }
    if request.method == 'POST':
        emp_del.delete()
        return redirect("employee-report")
    return render(request, 'site/employee_del.html', context)


@ login_required(login_url='index')
def department(request):
    dept = Department.objects.all()
    count_dept = dept.count()

    context = {
        'count_dept': count_dept,
    }
    if request.method == 'POST':
        department = request.POST.get('department')
        data = Department(dept_name=department)
        data.save()
        return redirect('department-report')

    return render(request, 'site/department.html', context)


@ login_required(login_url='index')
def department_report(request):
    reports = Department.objects.all()
    context = {
        'reports': reports
    }
    return render(request, 'site/department_report.html', context)


@ login_required(login_url='index')
def department_detail(request, pk):
    dept_detail = Department.objects.get(pk=pk)
    context = {
        'dept_detail': dept_detail,
    }

    return render(request, 'site/dept_detail.html', context)


@ login_required(login_url='index')
def department_edit(request, pk):
    dept_edit = Department.objects.get(pk=pk)
    if request.method == "POST":
        dept = request.POST.get('dept')
        dept_edit.dept_name = dept
        dept_edit.save()
        return redirect('department-report')
    context = {
        'dept_edit': dept_edit,
    }
    return render(request, 'site/dept_edit.html', context)


@ login_required(login_url='index')
def del_dept(request, pk):
    del_dept = Department.objects.get(pk=pk)
    context = {
        'del_dept': del_dept,
    }
    if request.method == "POST":
        del_dept.delete()
        return redirect('department-report')
    return render(request, 'site/department_delete.html', context)


@ login_required(login_url='index')
def emp_gender(request):
    if request.method == "POST":
        gender = request.POST.get('gender')
        data = Gender(gender=gender)
        data.save()
        return redirect('gender-report')
    return render(request, 'site/gender.html')


@ login_required(login_url='index')
def gender_report(request):
    genders = Gender.objects.all()

    context = {
        'genders': genders,
    }
    return render(request, 'site/gender_report.html', context)


@ login_required(login_url='index')
def gender_detail(request, pk):
    gender_detail = Gender.objects.get(pk=pk)
    context = {
        'gender_detail': gender_detail,
    }
    return render(request, 'site/gender_detail.html', context)


@ login_required(login_url='index')
def gender_edit(request, pk):
    g_edit = Gender.objects.get(pk=pk)

    if request.method == "POST":
        gender = request.POST.get('gender')
        g_edit.gender = gender
        g_edit.save()
        return redirect('gender-report')

    context = {
        'g_edit': g_edit,
    }
    return render(request, 'site/gender_edit.html', context)


@ login_required(login_url='index')
def gender_del(request, pk):
    g_del = Gender.objects.get(pk=pk)

    context = {
        'g_del': g_del,
    }

    if request.method == "POST":
        g_del.delete()

        return redirect('gender-report')
    return render(request, 'site/gender_del.html', context)
