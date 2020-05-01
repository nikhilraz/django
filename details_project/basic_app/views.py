from django.shortcuts import render
from basic_app.forms import UserForm,UserInfoForm
from basic_app.models import audit,UserInfo
# for login

from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'index.html')

# to make sure person who logged in ,only be logged out
@login_required
def special(request):
    return HttpResponse('u are logged in,nice!')


@login_required
def user_logout(request):
    curr_username=request.user
    audit.objects.filter(name=curr_username).update(logout_time=str(datetime.now()))
    logout(request)
    return render(request,'login.html',{})



def register(request):
    registered=False;
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #user_form ko sedha save kar
            user=user_form.save()
            pas=user.password
            user.set_password(user.password)
            user.save()
            #we grabed  ser information password set kiye fir save kiye database me
            profile=profile_form.save(commit=False)
            profile.user=user
            #one to one in models
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()

            registered=True;
        else:
            #invalid
            print(user_form.errors,profile_form.errors)

    else:
            user_form=UserForm()
            profile_form=UserInfoForm()
    if registered==False:
        return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        check=authenticate(username=user.username,password=pas)
        if check:
            if check.is_active:
                login(request,check)
                # save in audit table
                a=audit(name=user.username,login_time=str(datetime.now()),logout_time='')
                a.save()
                dict=audit.objects.all()
                # //u can send dict to any html page to display db contents
                return render(request,'other.html',{'username':user.username,'password':pas})
            else:
                return HttpResponse('account not active')
        else:
                return HttpResponse('invalid login supplied username {} password {}!'.format(user.username,pas))


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        # name in login in html is username,see
        password=request.POST.get('password')
        # use builtin authenticate method
        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                # for access data when looged in
                # save in audit table
                a=audit(name=username,login_time=str(datetime.now()),logout_time='')
                a.save()
                dict=audit.objects.all()
                return render(request,'other.html',{'username':username,'password':password})
            else:
                return HttpResponse('account not active')
        else:
            print('bad credentials!')
            print('username {} and password {}'.format(username,password))
            return HttpResponse('invalid login supplied!')
    else:
        return render(request,'login.html',{})
