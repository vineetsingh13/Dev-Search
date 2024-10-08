from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Message
from django.db.models import Q
from django.contrib import messages
from .utils import searchProfiles, paginationProfiles
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
# Create your views here.

@login_required(login_url="login")
def profiles(request):

    profiles, search_query=searchProfiles(request)

    custom_range,profiles=paginationProfiles(request,profiles,results=3)

    context={'profiles': profiles,'search_query':search_query,'custom_range':custom_range}
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

            #below if the user is not logged in and trying to review a project
            #the user will be taken to the login page and after logging in again back to the project page
            #if next is empty take user to account page
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'username or password is incorrect')


    return render(request,'users/login_register.html')


def logoutUser(request):
    #here we just delete the current session and the user without any session id will be logged out
    logout(request)
    messages.info(request,'user was logged out!')
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
            return redirect('edit-account')
        else:
            messages.error(request,'An error has occurred')

    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)


@login_required(login_url="login")
def userAccount(request):

    #to get the info of the logged in user
    profile=request.user.profile

    skills=profile.skill_set.all()
    project=profile.project_set.all()

    context={'profile':profile,'skills':skills,'projects':project}
    return render(request,'users/account.html',context)


@login_required(login_url="login")
def editAccount(request):
    profile=request.user.profile

    #to make the form be already filled with data
    form=ProfileForm(instance=profile)

    if request.method=='POST':
        #we are adding image also thats why FILES
        form=ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()

            return redirect('account')

    context={'form':form}
    return render(request, 'users/profile_form.html',context)


@login_required(login_url="login")
def createSkill(request):

    form=SkillForm()
    profile=request.user.profile
    if request.method == 'POST':
        form=SkillForm(request.POST)

        if form.is_valid():
            #below will make sure the tag is added for the respective user only
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('account')
        

    context={'form':form}
    return render(request, 'users/skill_form.html',context)


@login_required(login_url="login")
def updateSkill(request,pk):

    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)

    if request.method == 'POST':
        form=SkillForm(request.POST,instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request,'Skill was updated successfully!')
            return redirect('account')
        

    context={'form':form}
    return render(request, 'users/skill_form.html',context)



def deleteSkill(request,pk):

    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)

    if request.method=='POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')
    
    context={'object':skill}
    return render(request,'delete_template.html',context)


@login_required(login_url="login")
def inbox(request):

    profile=request.user.profile
    messageRequests=profile.messages.all()
    unreadCount=messageRequests.filter(is_read=False).count()


    context={'messageRequest':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)


@login_required(login_url="login")
def viewMessage(request,pk):
    profile=request.user.profile
    message=profile.messages.get(id=pk)

    if message.is_read==False:
        message.is_read=True
        message.save()

    context={'message':message}
    return render(request,'users/message.html',context)


@login_required(login_url="login")
def createMessage(request,pk):
    recipient=Profile.objects.get(id=pk)
    form=MessageForm()

    sender=request.user.profile
    print(sender)
    if request.method=='POST':
        form=MessageForm(request.POST)

        if form.is_valid():
            message=form.save(commit=False)
            message.sender=sender
            message.recipient=recipient
            
            if sender:
                message.name=sender.name
                message.email=sender.email
            message.save()

            messages.success(request,'Your message was successfully sent!')
            return redirect('user-profile',pk=recipient.id)



    context={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)
