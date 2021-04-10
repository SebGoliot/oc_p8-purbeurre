from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from accounts.models import CustomUser


class TestForms(StaticLiveServerTestCase):
    """Those tests checks the behaviour of the website from a user's
    perspective
    This file is dedicated to the forms
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Tests setup"""
        super(TestForms, cls).setUpClass()
        cls.firstname = "John"
        cls.lastname = "Doe"
        cls.email = "jdoe@gmail.com"
        cls.password = "veab0toox*KASS.wrik"

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(60)
        cls.selenium.set_page_load_timeout(60)

    def test_signup_form(self):
        """This test checks the signup form behaviour"""

        self.selenium.get(f"{self.live_server_url}/signup/")

        firstname = self.selenium.find_element_by_id("id_first_name")
        lastname = self.selenium.find_element_by_id("id_last_name")
        email = self.selenium.find_element_by_id("id_email")
        password1 = self.selenium.find_element_by_id("id_password1")
        password2 = self.selenium.find_element_by_id("id_password2")
        submit = self.selenium.find_element_by_id("submit_button")

        firstname.send_keys(self.firstname)
        lastname.send_keys(self.lastname)
        email.send_keys(self.email)
        password1.send_keys(self.password)
        password2.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

        self.selenium.get(f"{self.live_server_url}/account/")

        assert self.firstname in self.selenium.page_source
        self.assertInHTML(self.email, self.selenium.page_source)

    def test_login_form(self):
        """This test checks the login form behaviour"""

        self.user = CustomUser.objects.create(
            email=self.email, first_name=self.firstname
        )
        self.user.set_password(self.password)
        self.user.save()

        self.selenium.get(f"{self.live_server_url}/login/")

        email = self.selenium.find_element_by_id("id_username")
        password1 = self.selenium.find_element_by_id("id_password")
        submit = self.selenium.find_element_by_id("submit_button")

        email.send_keys(self.email)
        password1.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

        self.selenium.get(f"{self.live_server_url}/account/")

        assert self.firstname in self.selenium.page_source
        assert self.email in self.selenium.page_source

        CustomUser.objects.get(email=self.email).delete()

        assert self.firstname in self.selenium.page_source
        self.assertInHTML(self.email, self.selenium.page_source)
