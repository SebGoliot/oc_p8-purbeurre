from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """ The Form used in user registration
    """
    required_css_class = "required"
    error_css_class = "error"

    first_name = forms.CharField(
        label='Prénom',
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        }))
    last_name = forms.CharField(
        label='Nom',
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        }))
    email = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'E-mail'
        }))
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }))
    password2 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        }))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            UserCreationForm.add_error(self, 'password1',
                forms.ValidationError(
                    "Les mots de passe ne correspondent pas."))



class LoginForm(AuthenticationForm):
    """ The form used in user login
    """
    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'E-mail'
        }))
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }))
