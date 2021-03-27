from django.urls import path
from .views import index, search, product, legal, bookmark_product

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product/<int:product_id>', product, name='product'),
    path('legal', legal, name='legal'),
    path('bookmark-product/<int:product_id>',
        bookmark_product, name='bookmark_product'),
]
