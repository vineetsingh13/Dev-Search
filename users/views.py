from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.

@login_required(login_url="login")
def profiles(request):
    profiles=Profile.objects.all()
    context={'profiles': profiles}
    return render(request,'users/profiles.html',context)


def userProfile(request,pk):

    profile=Profile.objects.get(id=pk)

    topSkills=profile.skill_set.exclude(description__exact="")
    otherSkills=profile.skill_set.filter(description="")

    context={'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)


def loginPage(request):
    page='login'
    #this will not allow the user to go to login page if he is logged in
    if request.user.is_authenticated:
        return redirect('profiles')
    

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        try:
            user =User.objects.get(username=username)
        except:
            messages.error(request,'username does not exist')

        #here what authentication is going to do is query the database to find if the user exists
        #if exists return user instance else none
        user=authenticate(request,username=username,password=password)


        #so what this login method here is going to do if the user exists
        #it will set the session in the browsers cookies
        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'username or password is incorrect')


    return render(request,'users/login_register.html')


def logoutUser(request):
    #here we just delete the current session and the user without any session id will be logged out
    logout(request)
    messages.error(request,'user was logged out!')
    return redirect('login')


def registerUser(request):
    page='register'
    form =CustomUserCreationForm()

    if request.method=='POST':
        #usercreationform is a django form that is used to create a user and we can use it directly
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            #form.save()
            #first making sure that the name is lowercase and then saving
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            messages.success(request,'User account was created!')
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'An error has occurred')

    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)