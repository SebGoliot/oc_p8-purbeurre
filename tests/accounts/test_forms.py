from django.test import TestCase
from accounts.forms import UserCreationForm, LoginForm

class TestForms(TestCase):

    def test_user_creation_valid_data(self):
        form = UserCreationForm(data={
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@user.com',
            'password1': 'test123',
            'password2': 'test123',
        })
        self.assertTrue(form.is_valid())

    def test_user_creation_invalid_mail(self):
        form = UserCreationForm(data={
            'first_name': 'test',
            'last_name': 'user',
            'email': 'testuser.com',
            'password1': 'test123',
            'password2': 'test123',
        })
        self.assertFalse(form.is_valid())

    def test_user_creation_invalid_passwords(self):
        form = UserCreationForm(data={
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@user.com',
            'password1': 'test123',
            'password2': 'testabc',
        })
        self.assertFalse(form.is_valid())

    def test_user_creation_missing_data(self):
        form = UserCreationForm(data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'test123',
            'password2': 'test123',
        })
        self.assertFalse(form.is_valid())

    def test_user_creation_no_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())



    # def test_login_valid_data(self):
    #     form = LoginForm(data={
    #         'username': 'user@test.com',
    #         'password': 'test123',
    #     })
    #     self.assertTrue(form.is_valid())

    # def test_login_invalid_mail(self):
    #     form = LoginForm(data={
    #         'username': 'usertest.com',
    #         'password': 'test123',
    #     })
    #     self.assertFalse(form.is_valid())

    # def test_login_missing_data(self):
    #     form = LoginForm(data={
    #         'username': 'user@test.com',
    #     })
    #     self.assertFalse(form.is_valid())

    # def test_login_no_data(self):
    #     form = LoginForm(data={})
    #     self.assertFalse(form.is_valid())





# class UserCreationForm(forms.ModelForm):
#     first_name = forms.CharField(
#     last_name = forms.CharField(
#     email = forms.EmailField(
#     password1 = forms.CharField(
#     password2 = forms.CharField(
#     def save(self, commit=True):
# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(
#     password = forms.CharField(
