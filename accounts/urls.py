from django.urls import path
from .views import signup, account, login_view, logout_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
