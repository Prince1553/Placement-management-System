from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Image
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class ImageForm(forms.ModelForm):
 class Meta:
  model = Image
  fields = '__all__'
  labels = {'photo':''}
