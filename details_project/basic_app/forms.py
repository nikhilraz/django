from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserInfo

#create two classes one for User model inbuilt
#and one for our own userinfo model
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')


class UserInfoForm(forms.ModelForm):
    class Meta():
        model=UserInfo
        fields=('site','profile_pic')

#now register the models to admin
#if we login ,we can see actual models
