from django.urls import path
from .views import index, search, product, legal

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product/<int:product_id>', product, name='product'),
    path('legal', legal, name='legal'),
]
