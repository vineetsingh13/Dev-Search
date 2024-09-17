from django.http import JsonResponse


#some what a documentation for api
def getRoutes(request):

    routes=[
        {'GET':'api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]

    #safe here means we can send some other data besides json response which we dont want
    return JsonResponse(routes,safe=False)