from django.shortcuts import render ,HttpResponse

# Create your views here.
def load_user_app(request):
    return HttpResponse("User App Loaded")
