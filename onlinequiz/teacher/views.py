from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from company import models as CMODEL
from teacher import forms as TFORM
from django.contrib.auth.models import User
from django.contrib.auth import login

#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
        'total_student': SMODEL.Student.objects.all().filter(status=True  ).count(),

        'total_company': CMODEL.Company.objects.all().filter(status=True).count(),

    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_data(request):
    teacher = TMODEL.Teacher.objects.get(user=request.user.id)
    return render(request,'teacher/teacher_view_data.html',{'teacher':teacher})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_update_data(request):
    teacher = TMODEL.Teacher.objects.get(user=request.user.id)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'teacherForm':teacherForm}
    if request.method=='POST':
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if teacherForm.is_valid():
            teacherForm.save()
            return redirect('teacher-data')
    return render(request,'teacher/update_teacher.html',context=mydict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().filter(status=True).count(),
    'pending_student': SMODEL.Student.objects.all().filter(status=False).count(),
    }
    return render(request,'teacher/teacher_student.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_view(request):
    students = SMODEL.Student.objects.all().filter(status=True)
    return render(request,'teacher/teacher-view-student.html',{'students':students})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/teacher-view-student')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_pending_student_view(request):
    students= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'teacher/teacher_view_pending_student.html',{'students': students})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def approve_student_view(request,pk):
    student = SMODEL.Student.objects.get(id=pk)
    student.status=True
    student.save()
    return HttpResponseRedirect('/teacher-view-pending-student')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def reject_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/teacher-view-pending-student')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_company_view(request):
    company = CMODEL.Company.objects.all().filter(status=True)
    return render(request,'teacher/teacher_view_company.html',{'company':company })



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_company_data_view(request,pk):
    company=CMODEL.Company.objects.get(id=pk)
    return render(request,'teacher/teacher_view_company_data.html',{'company':company })


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_change_password(request):
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
    return render(request, "teacher/teacher_change_password.html", context)
