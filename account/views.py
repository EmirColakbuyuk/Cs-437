from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash

def loginView(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            nextUrl = request.GET.get('next', None)
            if nextUrl is None:
                #messages.success(request, "Login Succesful!")
                return redirect("index")
            else:
                return redirect(nextUrl)
        else:
            #messages.error(request, "Username or Password is not valid.")
            return render(request, "account/login.html")

    else:
        return render(request, "account/login.html")

def registerView(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        password = request.POST.get("password", None)
        re_password = request.POST.get("repassword", None)


        # if username and email and first_name and last_name is not None:
        # pass
        # else:
        # return render(request, "account/register.html", {"error": "Please annın nikahı"})

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error": "Username has already exists."})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {"error": "Email has already exists."})
                else:
                    user = User(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    try:
                        user.full_clean()
                    except Exception as e:
                        return render(request, "account/register.html", {"error": e.messages})#"there cannot be" koyulabılır 2z yerıne
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    user.is_active = True
                    user.save()
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('index')
                    else:
                        return render(request, "account/register.html", {"error": "Authentication error"})

        else:
            return render(request, "account/register.html", {"error": "Passwords are not the same."})
    else:
        return render(request, "account/register.html")

def logoutView(request):
    logout(request)
    #messages.success(request, "You have been logging out.")
    return redirect("index")





@login_required
def profileView(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "account/profile.html", {'form': form})


def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("changePassword")
        else:
            return render(request, 'account/changePassword.html', {"form": form})

    form = PasswordChangeForm(request.user)
    return render(request, 'account/changePassword.html', {"form": form}) 
