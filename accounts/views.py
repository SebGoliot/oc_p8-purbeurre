from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import UserCreationForm, LoginForm

from django.urls import reverse


def signup(request):
    """View handling the registration form rendering"""

    if request.user.is_authenticated:
        return redirect("account")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    ctx = {
        "form": form,
        "form_title": "Créez votre compte",
        "form_button": "S'inscrire",
        "form_option_title": "Vous avez déjà un compte ?",
        "form_option_target": reverse("login"),
        "form_option_button": "Se connecter",
    }
    return render(request, "auth_form.html", ctx)


def login_view(request):
    """View handling the login form rendering and the user authentication"""

    if request.user.is_authenticated:
        return redirect("account")

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("account")
    else:
        form = LoginForm()

    ctx = {
        "form": form,
        "form_title": "Connexion",
        "form_button": "Connexion",
        "form_option_title": "Pas encore de compte ?",
        "form_option_target": reverse("signup"),
        "form_option_button": "S'inscrire",
    }
    return render(request, "auth_form.html", ctx)


def account(request):
    """View rendering the user account"""
    if request.user.is_authenticated:
        ctx = {
            "username": request.user.first_name,
            "user_mail": request.user.email,
        }
        return render(request, "account.html", ctx)
    else:
        return redirect("login")


def logout_view(request):
    """View handling the user logout"""
    logout(request)
    return redirect("index")
