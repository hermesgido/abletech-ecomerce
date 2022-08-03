from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")

def signup(request):
    
    return render(request, "register.html")


def signin(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

def admins(request):
    return render(request, "admins.html")