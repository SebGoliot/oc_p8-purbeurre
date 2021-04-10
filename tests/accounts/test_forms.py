from django.test import TestCase
from accounts.forms import UserCreationForm, LoginForm
from accounts.models import CustomUser


class TestUserCreationForm(TestCase):
    """Those tests checks the behaviour of the accounts.forms UserCreationForm"""

    def test_user_creation_valid_data(self):
        """This test checks if the form can be validated"""
        form = UserCreationForm(
            data={
                "first_name": "test",
                "last_name": "user",
                "email": "test@user.com",
                "password1": "test123",
                "password2": "test123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_creation_invalid_mail(self):
        """This test checks if the form can detect invalid mail"""
        form = UserCreationForm(
            data={
                "first_name": "test",
                "last_name": "user",
                "email": "testuser.com",
                "password1": "test123",
                "password2": "test123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_creation_invalid_passwords(self):
        """This test checks if the form can detect non-matching passwords"""
        form = UserCreationForm(
            data={
                "first_name": "test",
                "last_name": "user",
                "email": "test@user.com",
                "password1": "test123",
                "password2": "testabc",
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_creation_missing_data(self):
        """This test checks if the form can detect incomplete data"""
        form = UserCreationForm(
            data={
                "first_name": "test",
                "last_name": "user",
                "password1": "test123",
                "password2": "test123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_creation_no_data(self):
        """This test checks if the form can detect empty data"""
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())


class TestLoginForm(TestCase):
    """Those tests checks the behaviour of the accounts.forms LoginForm"""

    def setUp(self):
        """Tests setup"""
        self.username = "test@user.com"
        self.password = "veab0toox*KASS.wrik"
        self.user = CustomUser.objects.create(email=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_login_valid_data(self):
        """This test checks if the form can be validated"""
        form = LoginForm(
            data={
                "username": self.username,
                "password": self.password,
            }
        )
        self.assertTrue(form.is_valid())

    def test_login_invalid_mail(self):
        """This test checks if the form can detect invalid mail"""
        form = LoginForm(
            data={
                "username": "usertest.com",
                "password": self.password,
            }
        )
        self.assertFalse(form.is_valid())

    def test_login_missing_data(self):
        """This test checks if the form can detect incomplete data"""
        form = LoginForm(
            data={
                "username": self.username,
            }
        )
        self.assertFalse(form.is_valid())

    def test_login_no_data(self):
        """This test checks if the form can detect empty data"""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
