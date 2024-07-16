from django.urls import path
from company import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('companyclick', views.companyclick_view),
path('companylogin', LoginView.as_view(template_name='company/companylogin.html'),name='companylogin'),
path('companysignup', views.company_signup_view,name='companysignup'),
path('company-data', views.company_view_data, name='company-data'),
path('company-update-data', views.company_update_data, name='company-update-data'),
path('student-applied-company', views.company_applied_student_data,name='student-applied-company'),
 
path('company-change-password',views.company_change_password,name='company-change-password'),
]
