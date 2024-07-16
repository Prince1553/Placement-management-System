from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-data', views.teacher_view_data, name='teacher-data'),
path('teacher-update-data', views.teacher_update_data, name='teacher-update-data'),
path('delete-student/<int:pk>', views.delete_student_view, name='delete-student'),
path('teacher-view-pending-student', views.teacher_view_pending_student_view, name='teacher-view-pending-student'),
path('teacher-student', views.teacher_student_view, name='teacher-student'),
path('teacher-view-student', views.teacher_view_student_view, name='teacher-view-student'),
path('approve-student/<int:pk>', views.approve_student_view, name='approve-student'),
path('reject-student/<int:pk>', views.reject_student_view, name='reject-student'),
path('teacher-view-company', views.teacher_view_company_view, name='teacher-view-company'),
path('teacher-view-company-data/<int:pk>', views.teacher_view_company_data_view, name='teacher-view-company-data'),
path('teacher-change-password',views.teacher_change_password,name='teacher-change-password'),
]