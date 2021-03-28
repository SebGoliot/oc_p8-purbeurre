from django.test import TestCase
from accounts.models import CustomUser, CustomUserManager

class TestModels(TestCase):

    def setUp(self):
        self.email = 'test@user.com'
        self.password = 'veab0toox*KASS.wrik'


    def test_user_str(self):
        user = CustomUser.objects.create(email = self.email)

        self.assertEqual(str(user), 'test@user.com')


    def test_manager_create_user_no_email(self):
        
        self.assertRaises(ValueError,
            CustomUserManager().create_user,
            **{'email': None, 'password': self.password}
            )


    def test_manager_create_user(self):
        user = CustomUser.objects.create_user(                                  # type: ignore
            email=self.email, password=self.password)

        self.assertIsInstance(user, CustomUser)


    def test_manager_create_superuser(self):
        user = CustomUser.objects.create_superuser(                             # type: ignore
            email=self.email, password=self.password)

        self.assertIsInstance(user, CustomUser)

    def test_manager_create_superuser_not_staff(self):
        data = {
            'email': self.email,
            'password': self.password,
            'is_staff': False
        }

        self.assertRaises(
            ValueError, CustomUser.objects.create_superuser, **data)            # type: ignore

    def test_manager_create_superuser_not_superuser(self):
        data = {
            'email': self.email,
            'password': self.password,
            'is_superuser': False
        }

        self.assertRaises(
            ValueError, CustomUser.objects.create_superuser, **data)            # type: ignore

