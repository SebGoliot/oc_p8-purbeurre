from django.urls import path
from .views import index, search, product, account, signup

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('product/<int:product_id>', product, name='product'),
    path('account', account, name='account'),
    path('signup', signup, name='signup'),
    path('', index, name='legal'),
]