from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("account/", AccountView.as_view(), name="account"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
