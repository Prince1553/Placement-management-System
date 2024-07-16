from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=70)
    address = models.CharField(max_length=70)
    designation = models.CharField(max_length=40)
    description= models.CharField(max_length=40)
    seats= models.IntegerField()
    salary = models.IntegerField()
    mobile = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)

