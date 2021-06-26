from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import (
    ChangeMail, SignupView, AccountView, LoginView, LogoutView, ChangePassword)


class TestUrls(SimpleTestCase):
    """Those tests checks the behaviour of the accounts.urls"""

    def test_signup_url_resolves(self):
        """Checks if the signup url resolves"""
        url = reverse("signup")

        self.assertEquals(
            resolve(url).func.__name__, SignupView.as_view().__name__)

    def test_account_url_resolves(self):
        """Checks if the account url resolves"""
        url = reverse("account")

        self.assertEquals(
            resolve(url).func.__name__, AccountView.as_view().__name__)

    def test_login_url_resolves(self):
        """Checks if the login url resolves"""
        url = reverse("login")

        self.assertEquals(
            resolve(url).func.__name__, LoginView.as_view().__name__)

    def test_logout_url_resolves(self):
        """Checks if the logout url resolves"""
        url = reverse("logout")

        self.assertEquals(
            resolve(url).func.__name__, LogoutView.as_view().__name__)


    def test_edit_password_url_resolves(self):
        """Checks if the edit_password url resolves"""
        url = reverse("edit-password")

        self.assertEquals(
            resolve(url).func.__name__, ChangePassword.as_view().__name__
        )

    def test_edit_mail_url_resolves(self):
        """Checks if the edit_mail url resolves"""
        url = reverse("edit-mail")

        self.assertEquals(
            resolve(url).func.__name__, ChangeMail.as_view().__name__
        )
