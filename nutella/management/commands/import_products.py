from django.core.management.base import BaseCommand
from nutella.models import Product, Category
import requests, json

class Command(BaseCommand):

    _OFF_API_ENDPOINT = "https://fr.openfoodfacts.org/cgi/search.pl"

    def add_arguments(self, parser):

        parser.add_argument('limit', type=int, nargs='?', default=500)


    def handle(self, *args, **options):

        limit = options['limit']
        default_page_size = 100
        page = 0

        self.stdout.write(
            f"Importing {limit} products \nThis operation may take a while...")

        products = []
        categories = {}

        # get products by pages of max 250 items
        while limit > 0:
            if limit >= default_page_size:
                item_number = default_page_size
            else:
                item_number = limit
            page += 1
            limit -= default_page_size

            # gather items
            items, item_categories = self._get_items(page, item_number)
            products += items
            categories |= item_categories

        # store
        self._store_products(products, categories)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully added the products"))


    def _get_items(self, page_number, page_size) -> "tuple[list, dict]":
        """Gets data from the API

        Args:
            page_number (int): The page number to get items from
            page_size (int): The page size 

        Returns:
            list: A list of products
        """
        search_args = {
            "sort_by": "popularity",
            "action": "process",
            "page_size": page_size,
            "page": page_number,
            "json": 1,
        }

        data = requests.get( url=self._OFF_API_ENDPOINT, params=search_args)
        return self._sanitize_data(data.content)


    def _sanitize_data(self, data:bytes) -> "tuple[list[dict], dict[int,list]]":
        """Sanitizes data from the API

        Args:
            data (bytes): JSON as retrieved from the OFF API

        Returns:
            list: A clean list of dict representing products
        """

        json_data = json.loads(data.decode("utf-8"))
        products = []
        categories = {}

        for each in json_data["products"]:
            product = {}
            product['code'] = each.get("code")
            product['name'] = each.get("product_name")
            product['nutriscore'] = each.get("nutriscore_grade")
            product['product_url'] = each.get("url")
            product['image_url'] = each.get("image_front_url")
            if nutriments := each.get('nutriments'):
                product['saturated_fat'] = nutriments.get('saturated-fat_100g')
                product['fat'] = nutriments.get('fat_100g')
                product['sugar'] = nutriments.get('sugars_100g')
                product['salt'] = nutriments.get('salt_100g')
            categories[product['code']] = each.get("categories_tags")
            
            if all(product.values()):
                products.append(product)
                product['nutriscore'] = product['nutriscore'].lower()

        return products, categories

    
    def _store_products(self, data:"list[dict]", categories:"dict"):
        """Saves a product to the db and its categories
        Updates the product if it already exists

        Args:
            data (list): A list containing all the products to store
            data (dict): A dictionnary containing the products categories
        """
        for each in data:
            product = Product.objects.update_or_create(
                            code=each['code'], defaults=each)[0]

            if _categories := categories.get(each['code']):
                for category_name in _categories:
                    category, created = Category.objects.get_or_create(
                        name=category_name)
                    if created:
                        category.save()
                    product.category.add(category)
                product.save()
