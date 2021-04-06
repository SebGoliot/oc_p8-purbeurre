from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from nutella.views import *
from nutella.models import Category, Product
from accounts.models import CustomUser as CustomUser
import json

class TestViews(TestCase):
    """ Those tests checks the behaviour of the nutella.views methods
    """


    @classmethod
    def setUpClass(cls) -> None:
        """ Tests setup
        """
        super(TestViews, cls).setUpClass()
        
        category = Category.objects.create(
            name = 'test_category'
        )
        product = Product.objects.create(
            code = 42,
            name = 'test_name',
            nutriscore = 'a',
            product_url = 'http://www.google.com',
            image_url = 'http://www.google.com',
            saturated_fat = 42,
            fat = 42,
            sugar = 42,
            salt = 42,
        )
        product.category.add(category)
        product.save()

        cls.username = 'test@user.com'
        cls.password = 'veab0toox*KASS.wrik'

        cls.user = CustomUser.objects.create(email=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()


    def test_index(self):
        """ This test checks if the index view behaves as expected
        """
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_legal(self):
        """ This test checks if the legal view behaves as expected
        """
        response = self.client.get(reverse('legal'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal.html')


    def test_product(self):
        """ This test checks if the product view behaves as expected
        """
        response = self.client.get(reverse('product', args=[42]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')


    def test_search(self):
        """ This test checks if the search view behaves as expected when a
        product is found
        """
        response = self.client.get(reverse('search'), {'query': 'test'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertInHTML(
            "<h2>Vous pouvez remplacer cet aliment par :</h2>",
            response.content.decode())


    def test_search_no_query(self):
        """ This test checks if the search view behaves as expected when no
        products are found
        """
        response = self.client.get(reverse('search'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


    def test_search_fail(self):
        """ This test checks if the search view behaves as expected when no
        products are found
        """
        response = self.client.get(reverse('search'), {'query': 'fail'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertInHTML(
            "<h2>Oups, aucun substitut n'a été trouvé 😕</h2>",
            response.content.decode()
            )


    def test_search_logged_user(self):
        """ This test checks if the search view behaves as expected with an
        authenticated user
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
            })
        response = self.client.get(reverse('search'), {'query': 'test_name'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')


    def test_user_products(self):
        """ This test checks if the products view behaves as expected with an
        authenticated user
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        response = self.client.get(reverse('user_products'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks.html')


    def test_user_products_non_authenticated(self):
        """ This test checks if the products view behaves as expected when the
        user is not authenticated
        """
        response = self.client.get(reverse('user_products'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login')+'?next=/my-products/')


    def test_bookmark_403(self):
        """ This test checks if the bookmark view POST method returns a 403 when
        no users are authenticated
        """
        response = self.client.post(reverse('bookmark'))

        self.assertEquals(response.status_code, 403)


    def test_bookmark_404(self):
        """ This test checks if the product view GET method returns a 404 when
        no users are authenticated
        """
        response = self.client.get(reverse('bookmark'))

        self.assertEquals(response.status_code, 404)


    def test_bookmark_malformed(self):
        """ This test checks if the product view POST method returns a
        HTTPResponseBAdRequest when the JSON payload is malformed
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        response = self.client.post(
            reverse('bookmark'),
            data="malformed request",
            content_type='application/json'
            )

        self.assertEquals(response.status_code, 400)
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertIn('malformed', response.content.decode())


    def test_bookmark_missing_values(self):
        """ This test checks if the product view POST method returns a
        HTTPResponseBAdRequest when the JSON payload is missing some values
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        response = self.client.post(
            reverse('bookmark'),
            data={'product_id': 42},
            content_type='application/json'
            )

        self.assertEquals(response.status_code, 400)
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertIn('missing', response.content.decode())


    def test_bookmark_save(self):
        """ This test checks if the product view POST method saves the bookmark
        if a user is authenticated and the bookmark doesn't exist yet
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        response = self.client.post(
            reverse('bookmark'),
            data={'product_id': 42, 'old_product_id': 42},
            content_type='application/json'
            )
        bookmark = Bookmark.objects.get(
            user = self.user,
            product = Product.objects.get(code=42)
            )

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(bookmark, Bookmark)


    def test_bookmark_delete(self):
        """ This test checks if the product view POST method deletes the
        bookmark if a user is authenticated and the bookmark already exist
        """
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        bookmark = {
            'user': self.user,
            'product': Product.objects.get(code=42),
            'old_product': Product.objects.get(code=42)
        }
        Bookmark.objects.create(**bookmark)

        response = self.client.post(
            reverse('bookmark'),
            data={'product_id': 42, 'old_product_id': 42},
            content_type='application/json'
            )

        self.assertEquals(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, Bookmark.objects.get, **bookmark)
