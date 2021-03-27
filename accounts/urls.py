from django.urls import path
from .views import *
from nutella.views import user_products

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
    path('my-products/', user_products, name='products'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
