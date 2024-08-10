from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


#so to pass data to the html pages we pass them as dictionary in the render method
#and we access them with {{page}} in the html pages
@login_required(login_url="login")
def projects(request):
    projects=Project.objects.all()
    context ={'projects': projects}
    return render(request, 'projects/projects.html',context) 


#whatever paramter we name in the url path
#the same name should be used as parameter in function
def project(request,pk):
    
    projectObj= Project.objects.get(id=pk)
    #tags=projectObj.tags.all()
    return render(request, 'projects/single-project.html',{'project':projectObj})  


@login_required(login_url="login")
def createProject(request):
    form=ProjectForm()
    context={'form':form}

    if request.method=='POST':
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            #save() to save in db
            form.save()
            return redirect('projects')

    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def updateProject(request,pk):
    project=Project.objects.get(id=pk)
    form=ProjectForm(instance=project)
    context={'form':form}

    if request.method=='POST':
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            #save() to save in db
            form.save()
            return redirect('projects')

    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def delete_project(request,pk):

    project=Project.objects.get(id=pk)

    if request.method=='POST':
        project.delete()
        return redirect('projects')
    
    context={'object':project}
    return render(request,'projects/delete_template.html',context)
