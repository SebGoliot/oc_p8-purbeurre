from django.urls import path
from .views import index, search, product, legal, bookmark, user_products

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product/<int:product_id>', product, name='product'),
    path('my-products/', user_products, name='user_products'),
    path('legal', legal, name='legal'),
    path('bookmark/<int:product_id>', bookmark, name='bookmark'),
]
