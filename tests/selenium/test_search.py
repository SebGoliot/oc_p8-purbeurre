from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from accounts.models import CustomUser

from nutella.management.commands import import_products


class TestSearch(StaticLiveServerTestCase):
    """ Those tests checks the behaviour of the website from a user's
    perspective
    This file is dedicated to the search feature
    """

    @classmethod
    def setUpClass(cls) -> None:
        """ Tests setup
        """
        super(TestSearch, cls).setUpClass()
        cls.firstname = 'John'
        cls.lastname = 'Doe'
        cls.email = 'jdoe@gmail.com'
        cls.password = 'veab0toox*KASS.wrik'

        cls.user = CustomUser.objects.create(email=cls.email)
        cls.user.set_password(cls.password)
        cls.user.save()

        chrome_options = Options()  
        chrome_options.add_argument("--headless")

        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(60)
        cls.selenium.set_page_load_timeout(60)
        cls.selenium.set_window_size(1280, 720)
        cls.wait = WebDriverWait(cls.selenium, 10)

        import_products.Command().handle(**{'limit': 123})


    def test_search(self):
        """ This test checks the behaviour of the search feature
        """

        self.selenium.get(self.live_server_url)
        query = 'nutella'

        search_field = self.selenium.find_element_by_id('nav_search_field')
        
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        self.assertInHTML(query, self.selenium.page_source)

    def test_search_failure(self):
        """ This test checks the behaviour of the search feature
        """

        self.selenium.get(self.live_server_url)
        query = 'azertyuiop'

        search_field = self.selenium.find_element_by_id('nav_search_field')
        
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        self.assertInHTML(
            "<h2>Oups, aucun substitut n'a été trouvé 😕</h2>",
            self.selenium.page_source)


    def test_search_narrow(self):
        """ This test checks the behaviour of the search feature when the window
        is narrow, this ensures the navigation is right on smaller screens
        """

        self.selenium.set_window_size(640, 720)
        self.selenium.get(self.live_server_url)
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
        
        # login the user
        self.selenium.get(f"{self.live_server_url}/login/")

        email = self.selenium.find_element_by_id('id_username')
        password1 = self.selenium.find_element_by_id('id_password')
        submit = self.selenium.find_element_by_id('submit_button')

        email.send_keys(self.email)
        password1.send_keys(self.password)
        submit.send_keys(Keys.RETURN)
        # The user should now be logged-in

        # Go back to the index

        # Search a product
        search_field = self.selenium.find_element_by_id('nav_search_field')
        query = 'nutella'
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        # Save the bookmark
        bookmark = self.selenium.find_element_by_class_name('bookmark-link')
        bookmark.click()
        # wait for AJAX to finish
        self.wait.until( lambda driver: 
            driver.execute_script('return jQuery.active') == 0)

        # Check the bookmark is visible in the bookmarks page
        self.selenium.get(f"{self.live_server_url}/my-products/")
        product_tile = self.selenium.find_element_by_class_name('product-tile')
        self.assertIsInstance(product_tile, WebElement)

        # Remove the bookmark
        bookmark = self.selenium.find_element_by_class_name('bookmark-link')
        bookmark.click()
        # wait for AJAX to finish
        self.wait.until( lambda driver: 
            driver.execute_script('return jQuery.active') == 0)


        # Refresh and assert the bookmark is no more in the bookmarks page
        self.selenium.refresh()
        self.assertInHTML(
            "<h2>Vous n'avez trouvé aucun substituts ? 😲</h2>",
            self.selenium.page_source)
