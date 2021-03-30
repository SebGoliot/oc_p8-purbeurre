from django.test.testcases import LiveServerTestCase
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from accounts.models import CustomUser

from nutella.management.commands import add_category, update_db


class TestForms(LiveServerTestCase):
    """ Those tests checks the behaviour of the website from a user's perspective
    This file is dedicated to the search feature
    """

    def setUp(self) -> None:
        """ Tests setup
        """
        self.firstname = 'John'
        self.lastname = 'Doe'
        self.email = 'jdoe@gmail.com'
        self.password = 'veab0toox*KASS.wrik'

        self.user = CustomUser.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(30)
        self.selenium.set_page_load_timeout(30)
        self.selenium.set_window_size(1280, 720)

        add_category.Command().handle(**{
            'category_name': ['pate', 'a', 'tartiner']})
        update_db.Command().handle(**{'limit': 10})
        

    def test_search(self):
        """ This test checks the behaviour of the search feature
        """

        self.selenium.get(f"{self.live_server_url}/")
        query = 'nutella'

        search_field = self.selenium.find_element_by_id('nav_search_field')
        
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        self.assertInHTML(query, self.selenium.page_source)


    def test_search_narrow(self):
        """ This test checks the behaviour of the search feature when the window
        is narrow, this ensures the navigation is right on smaller screens
        """

        self.selenium.set_window_size(640, 720)
        self.selenium.get(f"{self.live_server_url}/")
        query = 'nutella'

        nav_button = self.selenium.find_element_by_css_selector(
            ".navbar > div > button[aria-expanded='false']")
        search_field = self.selenium.find_element_by_id('nav_search_field')

        nav_button.click()
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        self.assertInHTML(query, self.selenium.page_source)


    def test_bookmark(self):
        """ This test checks the behaviour of the bookmarks feature
        """
        self.client.force_login(self.user)

        self.selenium.get(f"{self.live_server_url}/")
        query = 'nutella'

        search_field = self.selenium.find_element_by_id('nav_search_field')

        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        bookmark = self.selenium.find_element_by_class_name('bookmark-link')
        bookmark.click()

        self.selenium.get(f"{self.live_server_url}/bookmarks")

