from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Resume
from .models import Student
from student import models as SMODEL
from quiz import models as QMODEL
from company import models as CMODEL

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['address','campus','mobile','profile_pic']




GENDER_CHOICES = [
 ('Male', 'Male'),
 ('Female', 'Female')
]

# JOB_CITY_CHOICE = [
#  ('Delhi', 'Delhi'),
#  ('Pune', 'Pune'),
#  ('Ranchi', 'Ranchi'),
#  ('Mumbai', 'Mumbai'),
#  ('Dhanbad', 'Dhanbad'),
#  ('Banglore', 'Banglore')
# ]


class ResumeForm(forms.ModelForm):
 gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
 # companyname = forms.ModelChoiceField(queryset=CMODEL.Company.objects.all().filter(status=True), empty_label="Company Name", to_field_name="name")
 # job_city = forms.MultipleChoiceField(label='Preferred Job Locations', choices=JOB_CITY_CHOICE, widget=forms.CheckboxSelectMultiple)
 class Meta:
  model = Resume
  fields = ['name', 'dob', 'gender', 'locality', 'city', 'pin', 'state', 'mobile', 'email'  , 'my_file',]
  labels = { 'name':'Full Name', 'dob': 'Date of Birth', 'pin':'Pin Code', 'mobile':'Mobile No.', 'email':'Email ID' , 'my_file':'Document'}
  widgets = {
   'name':forms.TextInput(attrs={'class':'form-control'}),
   'dob':forms.DateInput(attrs={'class':'form-control', 'id':'datepicker'}),
   'locality':forms.TextInput(attrs={'class':'form-control'}),
   'city':forms.TextInput(attrs={'class':'form-control'}),
   'pin':forms.NumberInput(attrs={'class':'form-control'}),
   'state':forms.Select(attrs={'class':'form-select'}),
   'mobile':forms.NumberInput(attrs={'class':'form-control'}),
   'email':forms.EmailInput(attrs={'class':'form-control'}),
  }

