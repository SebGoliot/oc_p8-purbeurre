from django.urls import path
from .views import index, search, product

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product/<int:product_id>', product, name='product'),
    path('legal', index, name='legal'), #TODO : route to a proper 'legal' view
]
