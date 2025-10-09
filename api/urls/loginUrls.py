from django.urls import path

from api.views.loginView import SignupView, LogoutView

app_name = "api"
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
