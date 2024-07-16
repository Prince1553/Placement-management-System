from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib.auth import login
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from company import models as CMODEL
from company import forms as CFORM
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from .forms import ImageForm
from .models import Image



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'quiz/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_company(user):
    return user.groups.filter(name='COMPANY').exists()

def afterlogin_view(request):
    if is_student(request.user):
        accountapproval1 = SMODEL.Student.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval1:
            return redirect('student/student-dashboard')
        else:
            return render(request, 'student/student_wait_for_approval.html')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')

    elif is_company(request.user):
        accountapproval2= CMODEL.Company.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval2:
            return redirect('company/company-data')
        else:
            return render(request,'company/company_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().filter(status=True).count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_company':CMODEL.Company.objects.all().filter(status=True).count(),
    'total_applied':SMODEL.Resume.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_applied_student(request):
    applied_student=SMODEL.Resume.objects.all()
    return render(request,'quiz/admin_view_applied_student.html',{'applied_student': applied_student})



@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),

    }
    return render(request,'quiz/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
def admin_view_teacher_data_view(request,pk):
    teacher= TMODEL.Teacher.objects.get(id=pk)
    return render(request,'quiz/admin_view_teacher_data.html',{'teacher':teacher })


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'quiz/update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

 



@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().filter(status=True).count(),
    'pending_student': SMODEL.Student.objects.all().filter(status=False).count(),
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students = SMODEL.Student.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
def admin_view_student_data_view(request,pk):
    student = SMODEL.Student.objects.get(id=pk)
    return render(request,'quiz/admin_view_student_data.html',{'student':student })



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_view_pending_student_view(request):
    students= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_student.html',{'students': students})


@login_required(login_url='adminlogin')
def approve_student_view(request,pk):
    student = SMODEL.Student.objects.get(id=pk)
    student.status=True
    student.save()
    return HttpResponseRedirect('/admin-view-pending-student')


@login_required(login_url='adminlogin')
def reject_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-pending-student')


@login_required(login_url='adminlogin')
def admin_company_view(request):
    dict={
    'total_company':CMODEL.Company.objects.all().filter(status=True).count(),
    'pending_company': CMODEL.Company.objects.all().filter(status=False).count(),
    }
    return render(request,'quiz/admin_company.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_company_view(request):
    company = CMODEL.Company.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_company.html',{'company':company })

@login_required(login_url='adminlogin')
def admin_view_company_data_view(request,pk):
    company=CMODEL.Company.objects.get(id=pk)
    return render(request,'quiz/admin_view_company_data.html',{'company':company })



@login_required(login_url='adminlogin')
def update_company_view(request,pk):
    company=CMODEL.Company.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=company.user_id)
    userForm=CFORM.CompanyUserForm(instance=user)
    companyForm=CFORM.CompanyForm(request.FILES,instance=company)
    mydict={'userForm':userForm,'companyForm':companyForm}
    if request.method=='POST':
        userForm=CFORM.CompanyUserForm(request.POST,instance=user)
        companyForm=CFORM.CompanyForm(request.POST,request.FILES,instance=company)
        if userForm.is_valid() and companyForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            companyForm.save()
            return redirect('admin-view-company')
    return render(request,'quiz/update_company.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_company_view(request,pk):
    company=CMODEL.Company.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-company')


@login_required(login_url='adminlogin')
def admin_view_pending_company_view(request):
    company = CMODEL.Company.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_company.html',{'company': company})


@login_required(login_url='adminlogin')
def approve_company_view(request,pk):
    company = CMODEL.Company.objects.get(id=pk)
    company.status=True
    company.save()
    return HttpResponseRedirect('/admin-view-pending-company')


@login_required(login_url='adminlogin')
def reject_company_view(request,pk):
    company=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-pending-company')

@login_required(login_url='adminlogin')
def gallery_view(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = ImageForm()
    img = Image.objects.all()
    return render(request, 'quiz/gallery.html', {'img': img, 'form': form})




def aboutus_view(request):
    img = Image.objects.all()
    return render(request,'quiz/g2.html', {'img': img})

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})

@login_required(login_url='adminlogin')
def admin_change_password(request):
    context = {}
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
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
    return render(request, "quiz/admin_change_password.html", context)
