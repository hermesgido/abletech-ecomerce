from django.shortcuts import redirect, render
from .form import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.

<<<<<<< HEAD

=======
>>>>>>> 763ca3165f5393820508f81b1e419a6a84c1d271
def home(request):
    
   
    return render(request, "index.html")

def signup(request):
<<<<<<< HEAD
    form = UserRegForm()
    myUser = User.objects.all()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]

        if password != password1:
            messages.error(request, "Password dont Match")
            return redirect(signup)
        if len(password) < 4:
            messages.error(request, "Password too short")
            return redirect(signup)
        if User.objects.filter(username=username):
            messages.error(request, "user name already exist!")
            return redirect(signup)
        if User.objects.filter(email=email):
            messages.error(request, "email  already exist!")
            return redirect(signup)
        else:
            myUser = User.objects.create_user(
                username=username,
                email=email, 
                password=password,
                type_Of_User  = "B",
                )
            buyer = Buyer.objects.create(user_id=myUser)
            myUser.save()
            buyer.save()
            messages.success(request, "successfull registered")
            return redirect(signin)

=======
    
>>>>>>> 763ca3165f5393820508f81b1e419a6a84c1d271
    return render(request, "register.html")


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "logged in...")
            return redirect(home)
        else:
            messages.error(request, "wrong details")
            return redirect(signin)

    return render(request, "login.html")


def dashboard(request):
    return render(request, "dashboard.html")


def admins(request):
    return render(request, "admins.html")
