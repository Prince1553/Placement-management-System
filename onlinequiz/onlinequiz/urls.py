from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from quiz import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path('company/',include('company.urls')),
    


    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='quiz/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('admin-change-password',views.admin_change_password,name='admin-change-password'),
    path('admin-view-applied-student',views.admin_view_applied_student,name='admin-view-applied-student'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='quiz/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-gallery', views.gallery_view,name='admin-gallery'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher-data/<int:pk>', views.admin_view_teacher_data_view, name='admin-view-teacher-data'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-view-student-data/<int:pk>', views.admin_view_student_data_view, name='admin-view-student-data'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('admin-view-pending-student', views.admin_view_pending_student_view,name='admin-view-pending-student'),
    path('approve-student/<int:pk>', views.approve_student_view, name='approve-student'),
    path('reject-student/<int:pk>', views.reject_student_view, name='reject-student'),

    path('admin-company', views.admin_company_view,name='admin-company'),
    path('admin-view-company', views.admin_view_company_view,name='admin-view-company'),
    path('admin-view-company-data/<int:pk>', views.admin_view_company_data_view, name='admin-view-company-data'),
    path('update-company/<int:pk>', views.update_company_view,name='update-company'),
    path('delete-company/<int:pk>', views.delete_company_view,name='delete-company'),
    path('admin-view-pending-company', views.admin_view_pending_company_view,name='admin-view-pending-company'),
    path('approve-company/<int:pk>', views.approve_company_view, name='approve-company'),
    path('reject-company/<int:pk>', views.reject_company_view, name='reject-company'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
