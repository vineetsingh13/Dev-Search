from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review


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
#@permission_classes([IsAuthenticated])
def getProjects(request):

    print(request.user)
    projects=Project.objects.all()

    #many to define do we want to serialize all data
    serializer=ProjectSerializer(projects,many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request,pk):

    projects=Project.objects.get(id=pk)

    #many to define do we want to serialize all data
    serializer=ProjectSerializer(projects,many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):

    project=Project.objects.get(id=pk)
    user=request.user.profile

    #here request.data return the body of the api request
    data = request.data

    #below to make the user able to vote we first check whether the review for the associated project by the associated owner exists or not
    #created will just return true or false and review will return the object and then we change the value of vote
    review, created=Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    #below we take the value of the vote up or down and save it
    review.value=data['value']
    review.save()
    project.getVoteCount


    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)