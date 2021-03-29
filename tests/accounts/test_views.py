from django.test import TestCase
from django.urls import reverse
from nutella.views import *
from accounts.models import CustomUser as User

class TestViews(TestCase):


    def setUp(self):
        self.username = 'test@user.com'
        self.password = 'veab0toox*KASS.wrik'
        self.user = User.objects.create(email=self.username)
        self.user.set_password(self.password)
        self.user.save()


    def test_signup(self):
        response = self.client.get(reverse('signup'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_form.html')


    def test_signup_authenticated_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('signup'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))


    def test_signup_post(self):
        form_data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'form@test.com',
            'password1': '123',
            'password2': '123',
        }
        response = self.client.post(reverse('signup'), form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertIsInstance(User.objects.get(email='form@test.com'), User)


    def test_login_view(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_form.html')


    def test_login_view_post(self):
        form_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(reverse('login'), form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


    def test_login_authenticated_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))


    def test_account(self):
        response = self.client.get(reverse('account'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


    def test_account_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')


    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

