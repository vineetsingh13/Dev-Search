from django.shortcuts import render

from django.http import HttpResponse

def projects(request):
    return render(request, 'projects/projects.html') 

#whatever paramter we name in the url path
#the same name should be used as parameter in function
def project(request,pk):
    return render(request, 'projects/single-project.html')  
