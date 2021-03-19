from django import forms
from django.forms.utils import ErrorList
from .models import CustomUser


class UserCreationForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'E-mail'
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        }))

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
