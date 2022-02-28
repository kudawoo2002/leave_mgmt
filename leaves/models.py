from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    dept_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dept_name


class LeaveType(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender = models.CharField(max_length=20)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.gender


class Employee(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)
    dob = models.DateField()
    emp_code = models.CharField(max_length=200, blank=True)
    emp_gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    emp_picture = models.ImageField(upload_to="employee/pictures", blank=True)
    emp_address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20)
    emp_phone = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=100, blank=True)
    emp_nationality = models.CharField(max_length=200)
    dept_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    started_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}  {self.middle_name}"


class Status(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Leave(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    annual_total_leave = models.IntegerField(default=21)
    numberof_days = models.IntegerField()
    leave_balance = models.IntegerField(blank=True, default=0)
    leavetype = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    leave_comment = models.TextField()
    leave_status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.leave_balance = 0

        leaves = Leave.objects.filter(
            username__username=self.username).values('numberof_days')

        total_leave = 0
        for i in range(len(leaves)):
            total_leave = total_leave + leaves[i].get('numberof_days')

        if self.leave_status.name == 'Approved':
            self.leave_balance = self.annual_total_leave - total_leave
            # self.leave_balance = self.annual_total_leave
            super().save(*args, **kwargs)
        else:
            self.leave_balance = self.annual_total_leave - total_leave
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username.username.capitalize()} have resquested {self.numberof_days} days of leave"
