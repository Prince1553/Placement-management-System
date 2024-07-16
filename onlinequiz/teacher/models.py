from django.db import models
from django.contrib.auth.models import User

campus_chioce= (
   ('Amritsar','Amritsar'),
   ('Mohali Campus 1 ','Mohali Campus 1 '),
   ('Hoshiarpur','Hoshiarpur'),
   ('Mohali Campus 2 ','Mohali Campus 2 '),

)

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to="teachers",null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    campus = models.CharField(choices=campus_chioce,max_length=40)
    status= models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name