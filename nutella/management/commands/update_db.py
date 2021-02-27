from django.core.management.base import BaseCommand, CommandError
from nutella.models import Product, Category
from django.db.utils import OperationalError
from django.db.models.query import QuerySet
import requests, json

class Command(BaseCommand):

    _OFF_API_ENDPOINT = "https://fr.openfoodfacts.org/cgi/search.pl"


    def handle(self, *args, **options):

        if categories := self._get_categories():
            n_categories = len(categories)
            self.stdout.write(f"Updating db for {n_categories} categories")

            for i, category in enumerate(categories):
                self.stdout.write(
                    f"Updating category {i+1}/{n_categories}: {category.name}"
                    )
                items = self._get_category_from_api(category.name)
                self._store_products(items, category)


    def _get_categories(self) -> "QuerySet|None":
        """Get the registered categories from the db

        Returns:
            Queryset|None: The Queryset or None
        """
        try:
            categories = Category.objects.all()
        except OperationalError as err:
            self.stdout.write(self.style.ERROR(
                f"Could not retrieve the categories !\n{err}"
            ))
            return None

        if len(categories) == 0:
            self.stdout.write(self.style.WARNING(
                ("Couldn't get the categories to update !\n"
                "Make sure you have registered at least one category with"
                "`manage.py add_category`")
            ))
            return None

        return categories


    def _get_category_from_api(self, category:Category, limit:int=250) -> list:
        """Gets data from the API corresponding to a category

        Args:
            category (Category): The category of products to retrieve
            limit (int, optional): The max number of products to retrieve.

        Returns:
            list: A list of products
        """

        search_args = {
            "sort_by": "unique_scans_n",
            "action": "process",
            "search_terms": category,
            "page_size": limit,
            "json": 1,
        }

        data = requests.get(url=self._OFF_API_ENDPOINT, params=search_args)
        return self._sanitize_data(data.content)


    def _sanitize_data(self, data:bytes) -> "list[dict]":
        """Sanitizes data from the API

        Args:
            data (bytes): JSON as retrieved from the OFF API

        Returns:
            list: A clean list of dict representing products
        """

        json_data = json.loads(data.decode("utf-8"))
        products = []

        for each in json_data["products"]:

            product = {}
            product['code'] = each.get("code")
            product['name'] = each.get("product_name")
            product['nutriscore'] = each.get("nutriscore_grade")
            product['product_url'] = each.get("url")
            product['image_url'] = each.get("image_front_url")

            if all(product.values()):
                products.append(product)
        return products

    
    def _store_products(self, data:"list[dict]", category:Category):
        """Saves a product to the db

        Args:
            data (list): A list containing all the products to store
            category (Category): The Category of the products to store
        """

        for each in data:
            Product.objects.get_or_create(
                code = each['code'],
                name = each['name'],
                category = category,
                nutriscore = str(each['nutriscore']).upper(),
                product_url = each['product_url'],
                image_url = each['image_url'],
            )
