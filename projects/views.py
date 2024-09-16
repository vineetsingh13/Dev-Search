from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.db.models import Q
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
    #tags=projectObj.tags.all()
    return render(request, 'projects/single-project.html',{'project':projectObj})  


@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form=ProjectForm()
    context={'form':form}

    if request.method=='POST':
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():

            #save() to save in db
            #form.save()
            project=form.save(commit=False)

            #first save the project and then assign the project to the respective profile and then save
            project.owner=profile
            project.save()
            return redirect('account')

    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def updateProject(request,pk):
    #project=Project.objects.get(id=pk)

    profile=request.user.profile

    #below we make sure only the respective user can edit the project
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)
    context={'form':form}

    if request.method=='POST':
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            #save() to save in db
            form.save()
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
