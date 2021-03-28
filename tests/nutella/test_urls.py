from django.test import SimpleTestCase
from django.urls import reverse, resolve
from nutella.views import index, search, product, legal, bookmark, user_products


class TestUrls(SimpleTestCase):
    

    def test_index_resolves(self):
        url = reverse('index')

        self.assertEquals(resolve(url).func, index)
    

    def test_search_resolves(self):
        url = reverse('search')

        self.assertEquals(resolve(url).func, search)


    def test_product_resolves(self):
        url = reverse('product', args=[42])

        self.assertEquals(resolve(url).func, product)


    def test_my_products_resolves(self):
        url = reverse('user_products')

        self.assertEquals(resolve(url).func, user_products)


    def test_legal_resolves(self):
        url = reverse('legal')

        self.assertEquals(resolve(url).func, legal)


    def test_bookmark_resolves(self):
        url = reverse('bookmark', args=[42])

        self.assertEquals(resolve(url).func, bookmark)
