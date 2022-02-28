from django.contrib import admin
from .models import Employee, Leave, LeaveType, Department, Status, Gender

# Register your models here.

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(LeaveType)
admin.site.register(Department)
admin.site.register(Status)
admin.site.register(Gender)
