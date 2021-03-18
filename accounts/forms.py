from django import forms
from django.forms.utils import ErrorList
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ()

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
