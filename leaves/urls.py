from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.logout_page, name="logout-page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('leave/form/', views.leave_req, name="leave-request"),
    path('leave/detail/<pk>/', views.leave_detail, name="leave-detail"),
    path('leave/edit/<pk>/', views.leave_edit, name="leave-edit"),
    path('leaver/report/', views.leave_report, name="leave-report"),
    path('leaver/pending/report/', views.leave_pend_report,
         name="leave-pending-report"),
    path('leaver/report/delete/<pk>/', views.leave_del, name="leave-delete"),
    path('leave/type/', views.leave_type, name="leave-type"),
    path('leave/type/report/', views.leavetype_report, name="leave-type-report"),
    path('leave-type/detail/<pk>/',
         views.leavetype_detail, name="leave-type-detail"),
    path('delete-leavetype/<pk>/',
         views.del_leav_type, name="delete-leave-type"),
    path('edite_leavetype/<pk>/',
         views.edite_leave_type, name="leave-type-edit"),
    path('employee/', views.employee, name="employee"),
    path('employee/report/', views.employee_report, name='employee-report'),
    path('employee/detail/<pk>', views.employee_detail, name="employee-detail"),
    path('employee/edit/<pk>', views.employee_edit, name="employee-edit"),
    path('employee/del/<pk>', views.emp_del, name="employee-delete"),
    path('employee/department/', views.department, name='create-department'),
    path('employee/department/report/',
         views.department_report, name='department-report'),
    path('employee/department/detail/<pk>/',
         views.department_detail, name='department-detail'),
    path('employee/department/edit/<pk>/',
         views.department_edit, name="department-edit"),
    path('employee/department/delete/<pk>/',
         views.del_dept, name="department-delete"),
    path('employee/create/gender/', views.emp_gender, name="create-gender"),
    path('employee/gender/report/', views.gender_report, name="gender-report"),
    path('employee/gender/detail/<pk>/',
         views.gender_detail, name="gender-detail"),
    path('employee/gender/edit/<pk>/',
         views.gender_edit, name="gender-edit"),
    path('employee/gender/delete/<pk>/',
         views.gender_del, name="gender-delete"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
