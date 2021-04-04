from django.test import SimpleTestCase
from django.urls import reverse, resolve
from nutella.views import index, search, product, legal, bookmark, user_products


class TestUrls(SimpleTestCase):
    """ Those tests checks the behaviour of the nutella.urls
    """

    def test_index_url_resolves(self):
        """ Checks if the index url resolves
        """
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)
    

    def test_search_url_resolves(self):
        """ Checks if the search url resolves
        """
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)


    def test_product_url_resolves(self):
        """ Checks if the product url resolves
        """
        url = reverse('product', args=[42])
        self.assertEquals(resolve(url).func, product)


    def test_my_products_url_resolves(self):
        """ Checks if the user_products url resolves
        """
        url = reverse('user_products')
        self.assertEquals(resolve(url).func, user_products)


    def test_legal_url_resolves(self):
        """ Checks if the legal url resolves
        """
        url = reverse('legal')
        self.assertEquals(resolve(url).func, legal)


    def test_bookmark_url_resolves(self):
        """ Checks if the bookmark url resolves
        """
        url = reverse('bookmark')
        self.assertEquals(resolve(url).func, bookmark)
