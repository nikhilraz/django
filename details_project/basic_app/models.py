from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #additional field other than inbuilt

    site=models.URLField(blank=True)
    #nhi bhi dega chalega blank =True
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
    #now create a form for models .py files
class audit(models.Model):
    name=models.CharField(max_length=264,default='ABCXYZ')
    # created = models.DateTimeField(auto_now_add=True)
    login_time=models.CharField(max_length=264,default=str(datetime.now()))
    logout_time=models.CharField(max_length=264,default=str(datetime.now()))
