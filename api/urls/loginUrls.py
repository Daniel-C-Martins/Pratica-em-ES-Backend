from django.urls import path

from api.views.loginView import SignupView, LogoutView
from api.views.loginView import EmailLoginView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("token/", EmailLoginView.as_view(), name="token_obtain_pair_email"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
