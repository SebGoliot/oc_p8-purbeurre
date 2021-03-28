from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import signup, account, login_view, logout_view


class TestUrls(SimpleTestCase):
    
    def test_signup_resolves(self):
        url = reverse('signup')

        self.assertEquals(resolve(url).func, signup)
    
    def test_account_resolves(self):
        url = reverse('account')

        self.assertEquals(resolve(url).func, account)
    
    def test_login_resolves(self):
        url = reverse('login')

        self.assertEquals(resolve(url).func, login_view)
    
    def test_logout_resolves(self):
        url = reverse('logout')

        self.assertEquals(resolve(url).func, logout_view)
