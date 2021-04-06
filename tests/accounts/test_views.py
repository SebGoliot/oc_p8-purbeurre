from django.test import TestCase
from django.urls import reverse
from nutella.views import *
from accounts.models import CustomUser

class TestViews(TestCase):
    """ Those tests checks the behaviour of the accounts.views methods
    """


    @classmethod
    def setUpClass(cls) -> None:
        """ Tests setup
        """
        super(TestViews, cls).setUpClass()
        
        cls.username = 'test@user.com'
        cls.password = 'veab0toox*KASS.wrik'
        cls.user = CustomUser.objects.create(email=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()


    def test_signup(self):
        """ This test checks if the signup view behaves as expected
        """
        response = self.client.get(reverse('signup'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_form.html')


    def test_signup_authenticated_redirect(self):
        """ This test checks if the signup view behaves as expected if the user
        is already authenticated
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('signup'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))


    def test_signup_post(self):
        """ This test checks if the signup view's POST creates a user if proper
        form data is sent though it
        """
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
        self.assertIsInstance(
            CustomUser.objects.get(email='form@test.com'), CustomUser)


    def test_login_view(self):
        """ This test checks if the login view behaves as expected
        """
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_form.html')


    def test_login_view_post(self):
        """ This test checks if the login view's POST behaves as expected and
        provides a good authenticated user
        """
        form_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(reverse('login'), form_data)

        self.assertEquals(response.status_code, 302)
        self.assertIsInstance(response.wsgi_request.user, CustomUser)
        self.assertEquals(str(response.wsgi_request.user), self.username)
        self.assertRedirects(response, reverse('account'))


    def test_login_authenticated(self):
        """ This test checks if the login view behaves as expected if the user
        is already authenticated
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))


    def test_account_not_authenticated(self):
        """ This test checks if the account view behaves as expected if the user
        is not authenticated
        """
        response = self.client.get(reverse('account'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


    def test_account(self):
        """ This test checks if the account view behaves as expected
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')


    def test_logout_view(self):
        """ This test checks if the logout behaves as expected
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


    def test_logout_view_not_authenticated(self):
        """ This test checks if the logout behaves as expected if the user is
        not authenticated
        """
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

