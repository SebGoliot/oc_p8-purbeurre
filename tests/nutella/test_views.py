from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from nutella.views import *
from nutella.models import Category, Product
from accounts.models import CustomUser as User

class TestViews(TestCase):


    def setUp(self):
        
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

        self.username = 'test@user.com'
        self.password = 'veab0toox*KASS.wrik'

        self.user = User.objects.create(email=self.username)
        self.user.set_password(self.password)
        self.user.save()


    def test_index(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_legal(self):
        response = self.client.get(reverse('legal'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal.html')


    def test_product(self):
        response = self.client.get(reverse('product', args=[42]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')


    def test_search(self):
        response = self.client.get(reverse('search'), {'query': 'test_name'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')


    def test_search_fail(self):
        response = self.client.get(reverse('search'), {'query': 'fail'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')


    def test_search_logged_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('search'), {'query': 'test_name'})
        self.client.logout()

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')


    def test_user_products(self):
        response = self.client.get(reverse('user_products'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_bookmark_403(self):
        response = self.client.post(reverse('bookmark', args=[42]))

        self.assertEquals(response.status_code, 403)


    def test_bookmark_404(self):
        response = self.client.get(reverse('bookmark', args=[42]))

        self.assertEquals(response.status_code, 404)


    def test_bookmark_save(self):
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        response = self.client.post(reverse('bookmark', args=[42]))
        self.client.logout()
        self.assertEquals(response.status_code, 200)

        bookmark = Bookmark.objects.get(
            user = self.user,
            product = Product.objects.get(code=42)
            )
        self.assertIsInstance(bookmark, Bookmark)


    def test_bookmark_delete(self):
        self.client.login(**{
            'email': self.username,
            'password': self.password
        })
        bookmark = {
            'user': self.user,
            'product': Product.objects.get(code=42)
        }
        Bookmark.objects.create(**bookmark)
        response = self.client.post(reverse('bookmark', args=[42]))
        self.client.logout()

        self.assertEquals(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, Bookmark.objects.get, **bookmark)
