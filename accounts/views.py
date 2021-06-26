from accounts.models import CustomUser
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import (
    UserCreationForm, LoginForm, EditPasswordForm, EditMailForm)

from django.urls import reverse_lazy
from django.views import View


class SignupView(View):
    """Class handling the registration form"""
    ctx = {
        "form": UserCreationForm(),
        "form_title": "Créez votre compte",
        "form_button": "S'inscrire",
        "form_option_title": "Vous avez déjà un compte ?",
        "form_option_target": reverse_lazy("login"),
        "form_option_button": "Se connecter",
    }

    def get(self, request, *args, **kwargs):
        """Renders the registration form, or redirect to 'account' if the user
        is already authenticated
        """
        if request.user.is_authenticated:
            return redirect("account")
        return render(request, "auth_form.html", self.ctx)

    def post(self, request, *args, **kwargs):
        """Handles the form validation and user registration 
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("index")
        return render(request, "auth_form.html", self.ctx)



class LoginView(View):
    """Class handling the login form"""
    ctx = {
        "form": LoginForm,
        "form_title": "Connexion",
        "form_button": "Connexion",
        "form_option_title": "Pas encore de compte ?",
        "form_option_target": reverse_lazy("signup"),
        "form_option_button": "S'inscrire",
    }

    def get(self, request, *args, **kwargs):
        """Renders the signup form, or redirect to 'account' if the user is
        already authenticated
        """
        if request.user.is_authenticated:
            return redirect("account")
        return render(request, "auth_form.html", self.ctx)

    def post(self, request, *args, **kwargs):
        """Handles the form validation and user authentication 
        """
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("account")
        return render(request, "auth_form.html", self.ctx)


class AccountView(View):
    """Class handling the account view"""
    def get(self, request, *args, **kwargs):
        """Renders the user account, or redirect to 'login' if the user is not
        authenticated
        """
        if request.user.is_authenticated:
            ctx = {
                "username": request.user.first_name,
                "user_mail": request.user.email,
            }
            return render(request, "account.html", ctx)
        else:
            return redirect("login")


class LogoutView(View):
    """Class handling the logout view"""
    def get(self, request, *args, **kwargs):
        """Handles the user logout"""
        logout(request)
        return redirect("index")


class ChangePassword(View):

    ctx = {
        "form": EditPasswordForm(),
        "form_title": "Changez votre mot de passe",
        "form_button": "Valider",
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")
        return render(request, "auth_form.html", self.ctx)

    def post(self, request, *args, **kwargs):
        form = EditPasswordForm(data=request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=request.user, password=old_password)
            if user is not None and user.is_active:
                user.set_password(raw_password)
                user.save()
                login(request, user)
                return redirect("account")
            else:
                form.add_error(
                    "old_password",
                    forms.ValidationError("Le mot de passe actuel est invalide."),
                )
        return render(request, "auth_form.html", self.ctx)


class ChangeMail(View):

    ctx = {
        "form": EditMailForm(),
        "form_title": "Changez votre mot de passe",
        "form_button": "Valider",
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")
        return render(request, "auth_form.html", self.ctx)

    def post(self, request, *args, **kwargs):
        form = EditMailForm(data=request.POST)
        if form.is_valid():
            new_mail = form.cleaned_data.get("new_mail1")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(email=request.user, password=raw_password)
            if user is not None and user.is_active:
                user.email = new_mail   #type: ignore
                user.save()
                login(request, user)
                return redirect("account")
            else:
                form.add_error(
                    "password",
                    forms.ValidationError("Mot de passe invalide."),
                )
        return render(request, "auth_form.html", self.ctx)
