from django.urls import path
from .views import signup, account

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
]
