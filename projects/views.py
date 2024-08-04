from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


#so to pass data to the html pages we pass them as dictionary in the render method
#and we access them with {{page}} in the html pages
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


def createProject(request):
    form=ProjectForm()
    context={'form':form}
    return render(request,"projects/project_form.html",context)