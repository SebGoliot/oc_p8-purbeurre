from django import forms
from django.forms.utils import ErrorList
from .models import CustomUser


class UserCreationForm(forms.ModelForm):

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
