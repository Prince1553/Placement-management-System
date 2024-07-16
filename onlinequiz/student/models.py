from django.db import models
from django.contrib.auth.models import User
from company.models import Company


campus_chioce= (
   ('Amritsar','Amritsar'),
   ('Mohali Campus 1 ','Mohali Campus 1 '),
   ('Hoshiarpur','Hoshiarpur'),
   ('Mohali Campus 2 ','Mohali Campus 2 '),

)

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to="students", null=True, blank=True)
    address = models.CharField(max_length=40)
    campus = models.CharField(choices=campus_chioce,max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


STATE_CHOICE = (
 ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
 ('Andhra Pradesh','Andhra Pradesh'),
 ('Arunachal Pradesh','Arunachal Pradesh'),
 ('Assam','Assam'),
 ('Bihar','Bihar'),
 ('Chandigarh','Chandigarh'),
 ('Chhattisgarh','Chhattisgarh'),
 ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
 ('Daman and Diu','Daman and Diu'),
 ('Delhi','Delhi'),
 ('Goa','Goa'),
 ('Gujarat','Gujarat'),
 ('Haryana','Haryana'),
 ('Himachal Pradesh','Himachal Pradesh'),
 ('Jammu & Kashmir','Jammu & Kashmir'),
 ('Jharkhand','Jharkhand'),
 ('Karnataka','Karnataka'),
 ('Kerala','Kerala'),
 ('Lakshadweep','Lakshadweep'),
 ('Madhya Pradesh','Madhya Pradesh'),
 ('Maharashtra','Maharashtra'),
 ('Manipur','Manipur'),
 ('Meghalaya','Meghalaya'),
 ('Mizoram','Mizoram'),
 ('Nagaland','Nagaland'),
 ('Odisha','Odisha'),
 ('Puducherry','Puducherry'),
 ('Punjab','Punjab'),
 ('Rajasthan','Rajasthan'),
 ('Sikkim','Sikkim'),
 ('Tamil Nadu','Tamil Nadu'),
 ('Telangana','Telangana'),
 ('Tripura','Tripura'),
 ('Uttarakhand','Uttarakhand'),
 ('Uttar Pradesh','Uttar Pradesh'),
 ('West Bengal','West Bengal'),
)

class Resume(models.Model):
 student= models.ForeignKey(Student,on_delete=models.CASCADE)
 company = models.ForeignKey(Company, on_delete=models.CASCADE)
 name = models.CharField(max_length=100)
 dob = models.DateField(auto_now=False, auto_now_add=False)
 gender = models.CharField(max_length=100)
 locality = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 pin = models.PositiveIntegerField()
 state = models.CharField(choices=STATE_CHOICE, max_length=50)
 mobile = models.PositiveIntegerField()
 email = models.EmailField()
 my_file = models.FileField(upload_to='doc', blank=True)
