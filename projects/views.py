from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.contrib import messages
from .utils import searchProjects, paginationProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required


#so to pass data to the html pages we pass them as dictionary in the render method
#and we access them with {{page}} in the html pages
@login_required(login_url="login")
def projects(request):

    projects, search_query=searchProjects(request)
    custom_range,projects=paginationProjects(request,projects,results=6)

    # print(search_query , custom_range);

    context ={'projects': projects,'search_query':search_query,'custom_range':custom_range}
    print(context);
    return render(request, 'projects/projects.html',context) 


#whatever paramter we name in the url path
#the same name should be used as parameter in function
def project(request,pk):
    
    projectObj= Project.objects.get(id=pk)

    form=ReviewForm()

    if request.method=='POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)

        #to set the owner and the project for which review is written
        review.project=projectObj
        review.owner=request.user.profile
        review.save()

        #update vote count and ratio
        #we can run it directly like an attribute and not method
        projectObj.getVoteCount

        messages.success(request,"Your review was recorded successfully!")

        return redirect('project',pk=projectObj.id)

    #tags=projectObj.tags.all()
    return render(request, 'projects/single-project.html',{'project':projectObj,'form':form})  


@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form=ProjectForm()
    context={'form':form}

    if request.method=='POST':

        newtags=request.POST.get('newtags').replace(','," ").split()
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():

            #save() to save in db
            #form.save()
            project=form.save(commit=False)

            #first save the project and then assign the project to the respective profile and then save
            project.owner=profile
            project.save()

            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def updateProject(request,pk):
    #project=Project.objects.get(id=pk)

    profile=request.user.profile

    #below we make sure only the respective user can edit the project
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)
    context={'form':form,'project':project}

    if request.method=='POST':
        #print(request.POST)
        #print("data", request.POST)

        tag_remove=request.POST.getlist('tags_to_remove')
        
        newtags=request.POST.get('newtags').replace(','," ").split()
        
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            #save() to save in db
            form.save()

            for tag_id in tag_remove:
                tag = Tag.objects.get(id=tag_id)
                project.tags.remove(tag)

            #below we are checking if the new tag already exists or not if not we add to the database
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def delete_project(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)

    if request.method=='POST':
        project.delete()
        return redirect('projects')
    
    context={'object':project}
    return render(request,'delete_template.html',context)
