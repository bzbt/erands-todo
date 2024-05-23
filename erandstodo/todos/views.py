from django.http import HttpResponse


# Index page of the app
def index(request):
    return HttpResponse('Hello, world!')
