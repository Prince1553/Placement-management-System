from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('student-view-company', views.student_view_company_view, name='student-view-company'),
path('student-view-company-data/<int:pk>', views.student_view_company_data_view, name='student-view-company-data'),
path('student-apply-company/<int:pk>', views.student_apply_company_view, name='student-apply-company'),
path('student-data', views.student_view_data, name='student-data'),
path('student-update-data', views.student_update_data, name='student-update-data'),
path('student-company-drive', views.student_company_drive_view,name='student-company-drive'),
path('student-applied-company-drive', views.student_applied_company_drive_view,name='student-applied-company-drive'),
 
path('student-quaries', views.send_email,name='student-quaries'),
path('change-password',views.change_password,name='change-password'),


]