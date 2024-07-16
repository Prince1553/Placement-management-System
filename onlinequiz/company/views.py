from django.shortcuts import render
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from student import models as SMODEL
from company import forms as CFORM
from quiz import models as QMODEL
from company import models as CMODEL
from teacher import models as TMODEL
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

def companyclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'company/companyclick.html')

def company_signup_view(request):
    userForm=forms.CompanyUserForm()
    companyForm=forms.CompanyForm()
    mydict={'userForm':userForm,'companyForm':companyForm}
    if request.method=='POST':
        userForm=forms.CompanyUserForm(request.POST)
        companyForm=forms.CompanyForm(request.POST,request.FILES)
        if userForm.is_valid() and companyForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            company=companyForm.save(commit=False)
            company.user=user
            company.save()
            my_company_group = Group.objects.get_or_create(name='COMPANY')
            my_company_group[0].user_set.add(user)
        return HttpResponseRedirect('companylogin')
    return render(request,'company/companysignup.html',context=mydict)

def is_company(user):
    return user.groups.filter(name='COMPANY').exists()


# @login_required(login_url='companylogin')
# @user_passes_test(is_company)
# def company_dashboard_view(request):
#     return render(request, 'company/company_dashboard.html')


@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_view_data(request):
    company = CMODEL.Company.objects.get(user=request.user.id)
    return render(request,'company/company_view_data.html',{'company':company})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_update_data(request):
    company=CMODEL.Company.objects.get(user=request.user.id)
    companyForm=CFORM.CompanyForm(request.FILES,instance=company)
    mydict={'companyForm':companyForm}
    if request.method=='POST':
        companyForm=CFORM.CompanyForm(request.POST,request.FILES,instance=company)
        if companyForm.is_valid():
            companyForm.save()
            return redirect('company-data')
    return render(request,'company/update_company.html',context=mydict)

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_applied_student_data(request):
    company=CMODEL.Company.objects.get(user=request.user.id)
    applied_students = SMODEL.Resume.objects.all().filter(company=company)
    return render(request, 'company/company_view_applied_student.html', {'applied_students': applied_students})



 

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_change_password(request):
    context = {}
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = CMODEL.User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request, user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"
    return render(request, "company/change_password.html", context)