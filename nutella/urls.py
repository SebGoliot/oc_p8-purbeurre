from django.urls import path
from .views import index, search, product

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product', product, name='product'),
    path('', index, name='legal'),
]