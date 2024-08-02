from django.shortcuts import render

from django.http import HttpResponse

projectslist=[
    {
        'id': '1',
        'title': "Ecommerce Website",
        'description': "Fully functional ecommerce website"
    },
    {
        'id': '2',
        'title': "Portfolio Website",
        'description': "Project where i built my portfolio website"
    },
    {
        'id': '3',
        'title': "Social Website",
        'description': "A fully functional ecommerce website"
    }
]
#so to pass data to the html pages we pass them as dictionary in the render method
#and we access them with {{page}} in the html pages
def projects(request):
    page="projects"
    number=10
    context ={'page':page,'number':number,'projects': projectslist}
    return render(request, 'projects/projects.html',context) 


#whatever paramter we name in the url path
#the same name should be used as parameter in function
def project(request,pk):
    projectObj=None

    for i in projectslist:
        if i['id']==pk:
            projectObj=i

    
    return render(request, 'projects/single-project.html',{'project':projectObj})  
