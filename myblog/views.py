from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def signUp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is automatically created via post_save signal
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def blogs(request):
    pass

def Categories(requeust):
    pass

def Profile(request):
    pass

def BlogWrite(request):
    pass

def Notifications(request):
    pass

def PendingBlogs(request):
    pass

def logout(request):
    pass