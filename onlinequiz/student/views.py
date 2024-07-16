from django.shortcuts import render,redirect,reverse
from . import forms,models
from .forms import ResumeForm
from .models import Resume
from .models import Student
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail
from datetime import date, timedelta
from student import models as SMODEL
from student import forms as SFORM
from quiz import models as QMODEL
from company import models as CMODEL
from teacher import models as TMODEL
from django.contrib.auth.models import User


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    'total_company':CMODEL.Company.objects.all().filter(status=True).count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_company_view(request):
    company = CMODEL.Company.objects.all().filter(status=True)
    return render(request,'student/student_view_company.html',{'company':company })

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_company_data_view(request,pk):
    company=CMODEL.Company.objects.get(id=pk)
    return render(request,'student/student_view_company_data.html',{'company':company })

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_apply_company_view(request,pk):
     context = {}
     company = CMODEL.Company.objects.get(id=pk)
     form=forms.ResumeForm()
     if request.method == 'POST':
         form = ResumeForm(request.POST, request.FILES)
         if form.is_valid():
           resume = form.save(commit=False)
           student = SMODEL.Student.objects.get(user=request.user.id)
           resume.student = student
           resume.company= company
           resume.save()
           context["msz"] = "Applied Successfully!!!"
           context["col"] = "alert-success"
     return render(request, 'student/student_apply_company.html', {'form': form})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_data(request):
    student = SMODEL.Student.objects.get(user=request.user.id)
    return render(request,'student/student_view_data.html',{'student':student})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_update_data(request):
    student=SMODEL.Student.objects.get(user=request.user.id)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'studentForm':studentForm}
    if request.method=='POST':
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if studentForm.is_valid():
            studentForm.save()
            return redirect('student-data')
    return render(request,'student/update_student.html',context=mydict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_company_drive_view(request):
    student = SMODEL.Student.objects.get(user=request.user.id)
    dict = {
        'total_company': CMODEL.Company.objects.all().filter(status=True).count(),
        'total_company_applied':SMODEL.Resume.objects.all().filter(student=student).count(),
    }
    return render(request,'student/student_company_drive.html',context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_applied_company_drive_view(request):
    student = SMODEL.Student.objects.get(user=request.user.id)
    applied_companies = CMODEL.Company.objects.all().filter(resume__student=student)
    return render(request,'student/student_view_applied_company.html',{'applied_companies':applied_companies })

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def send_email(request):
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = 'your_email@gmail.com'  # replace with your actual email address
        recipient_list = [student.email]
        send_mail(subject, message, from_email, recipient_list)
    return render(request, 'student/send_email.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def change_password(request):
    context = {}
    student = SMODEL.Student.objects.get(user_id=request.user.id)

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = SMODEL.User.objects.get(id=request.user.id)
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
    return render(request, "student/change_password.html", context)