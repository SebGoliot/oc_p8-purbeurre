from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import signup, account, login_view, logout_view


class TestUrls(SimpleTestCase):
    """Those tests checks the behaviour of the accounts.urls"""

    def test_signup_url_resolves(self):
        """Checks if the signup url resolves"""
        url = reverse("signup")

        self.assertEquals(resolve(url).func, signup)

    def test_account_url_resolves(self):
        """Checks if the account url resolves"""
        url = reverse("account")

        self.assertEquals(resolve(url).func, account)

    def test_login_url_resolves(self):
        """Checks if the login url resolves"""
        url = reverse("login")

        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        """Checks if the logout url resolves"""
        url = reverse("logout")

        self.assertEquals(resolve(url).func, logout_view)
