from django.db import models
from accounts.models import CustomUser


class Category(models.Model):
    """Category model used to group products"""

    name = models.TextField()

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    """Product model for the products scrapped from the OpenFoodFacts API"""

    code = models.PositiveBigIntegerField()
    name = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    nutriscore = models.TextField()
    product_url = models.TextField()
    image_url = models.TextField()

    fat = models.DecimalField(decimal_places=2, max_digits=6)
    saturated_fat = models.DecimalField(decimal_places=2, max_digits=6)
    sugar = models.DecimalField(decimal_places=2, max_digits=6)
    salt = models.DecimalField(decimal_places=2, max_digits=6)


class Substitute(models.Model):
    """Substritute associative table"""

    user = models.ForeignKey(
            CustomUser, on_delete=models.CASCADE, related_name='user')
    old_product = models.ForeignKey(
            Product, on_delete=models.CASCADE, related_name='old_product')
    new_product = models.ForeignKey(
            Product, on_delete=models.CASCADE, related_name='new_product')
