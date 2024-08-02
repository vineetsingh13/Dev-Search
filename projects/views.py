from django.shortcuts import render

from django.http import HttpResponse

def projects(request):
    return HttpResponse("Here are our products") 

#whatever paramter we name in the url path
#the same name should be used as parameter in function
def project(request,pk):
    return HttpResponse("Single project"+' '+str(pk)) 
