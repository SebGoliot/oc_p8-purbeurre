from django.test import TestCase
from accounts.models import CustomUser, CustomUserManager


class TestModels(TestCase):
    """Those tests checks the behaviour of the accounts.models"""

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestModels, cls).setUpClass()
        cls.email = "test@user.com"
        cls.password = "veab0toox*KASS.wrik"

    def test_user_str(self):
        """This test checks if the CustomUser object returns the user email
        when __str__ is called
        """
        user = CustomUser.objects.create(email=self.email)

        self.assertEqual(str(user), self.email)

    def test_manager_create_user_no_email(self):
        """This test checks if the CustomUserManager raises an exception when
        the user is created without email
        """
        self.assertRaises(
            ValueError,
            CustomUserManager().create_user,
            **{"email": None, "password": self.password}
        )

    def test_manager_create_user(self):
        """This test checks if the create_user behaviour is as expected"""
        user = CustomUser.objects.create_user(  # type: ignore
            email=self.email, password=self.password
        )

        self.assertIsInstance(user, CustomUser)

    def test_manager_create_superuser(self):
        """This test checks if the create_superuser behaviour is as expected"""
        user = CustomUser.objects.create_superuser(  # type: ignore
            email=self.email, password=self.password
        )

        self.assertIsInstance(user, CustomUser)

    def test_manager_create_superuser_not_staff(self):
        """This test checks if the create_superuser raises an error when the
        created user is_staff property is set to False
        """
        data = {
            "email": self.email,
            "password": self.password,
            "is_staff": False,
        }

        self.assertRaises(
            ValueError,
            CustomUser.objects.create_superuser,  # type: ignore
            **data
        )

    def test_manager_create_superuser_not_superuser(self):
        """This test checks if the create_superuser raises an error when the
        created user is_superuser property is set to False
        """
        data = {
            "email": self.email,
            "password": self.password,
            "is_superuser": False,
        }

        self.assertRaises(
            ValueError,
            CustomUser.objects.create_superuser,  # type: ignore
            **data
        )
