from django.db import models

from student.models import Student

class Image(models.Model):
 photo = models.ImageField(upload_to="myimage")
 date = models.DateTimeField(auto_now_add=True)



