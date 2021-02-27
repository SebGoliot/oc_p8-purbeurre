from django.db import models


class Category(models.Model):
    """Category model used to group products"""

    name = models.TextField()


class Product(models.Model):
    """Product model for the products scrapped from the OpenFoodFacts API"""

    code = models.PositiveBigIntegerField()
    name = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    nutriscore = models.TextField()
    product_url = models.TextField()
    image_url = models.TextField()
