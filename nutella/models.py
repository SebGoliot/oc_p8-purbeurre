from django.db import models
from accounts.models import CustomUser


class Category(models.Model):
    """Category model used to group products"""

    name = models.TextField()

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    """Product model for the products scrapped from the OpenFoodFacts API"""

    code = models.PositiveBigIntegerField(primary_key=True)
    name = models.TextField()
    category = models.ManyToManyField(Category)
    nutriscore = models.TextField()
    product_url = models.TextField()
    image_url = models.TextField()

    fat = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="matières grasses"
    )
    saturated_fat = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="acides gras saturés"
    )
    sugar = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="sucres"
    )
    salt = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="sel"
    )


class Bookmark(models.Model):
    """Bookmarks associative table"""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookmarks"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="bookmarks"
    )
    old_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="substitutes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
