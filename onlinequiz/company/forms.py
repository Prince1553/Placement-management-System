from django import forms
from django.contrib.auth.models import User
from . import models

class CompanyUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[ 'username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model=models.Company
        fields= ['name','email','address','designation','description','seats','salary','mobile']