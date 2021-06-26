from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """The Form used in user registration"""

    required_css_class = "required"
    error_css_class = "error"

    first_name = forms.CharField(
        label="Prénom",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Prénom"}
        ),
    )
    last_name = forms.CharField(
        label="Nom",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom"}
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "E-mail"}
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )
    password2 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmez votre mot de passe",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            UserCreationForm.add_error(
                self,
                "password1",
                forms.ValidationError(
                    "Les mots de passe ne correspondent pas."
                ),
            )


class LoginForm(AuthenticationForm):
    """The form used in user login"""

    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "E-mail"}
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )


class EditPasswordForm(forms.Form):
    """The Form used to edit an user's password"""

    required_css_class = "required"
    error_css_class = "error"

    old_password = forms.CharField(
        label="Nouvelle adresse mail",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nouvelle adresse mail",
            }
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )
    password2 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmez votre mot de passe",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            EditPasswordForm.add_error(
                self,
                "password1",
                forms.ValidationError(
                    "Les mots de passe ne correspondent pas."
                ),
            )


class EditMailForm(forms.Form):
    """The Form used to edit an user's password"""

    required_css_class = "required"
    error_css_class = "error"

    new_mail1 = forms.EmailField(
        label="Nouvelle adresse E-mail",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nouvelle adresse E-mail",
            }
        ),
    )
    new_mail2 = forms.EmailField(
        label="Nouvelle adresse E-mail",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nouvelle adresse E-mail",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Mot de passe",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_mail1 = cleaned_data.get("new_mail1")
        new_mail2 = cleaned_data.get("new_mail2")

        if new_mail1 != new_mail2:
            EditMailForm.add_error(
                self,
                "new_mail1",
                forms.ValidationError(
                    "Les adresses mail ne correspondent pas."
                ),
            )
