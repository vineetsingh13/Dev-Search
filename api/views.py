from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


#some what a documentation for api
@api_view(['GET'])
def getRoutes(request):

    routes=[
        {'GET':'api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]

    #safe here means we can send some other data besides json response which we dont want
    #return JsonResponse(routes,safe=False)

    return Response(routes)


@api_view(['GET'])
def getProjects(request):

    projects=Project.objects.all()

    #many to define do we want to serialize all data
    serializer=ProjectSerializer(projects,many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):

    projects=Project.objects.get(id=pk)

    #many to define do we want to serialize all data
    serializer=ProjectSerializer(projects,many=False)

    return Response(serializer.data)