from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.authView import LoginView
from api.views.adotanteView import RegisterAdotanteView
from api.views.tutorView import RegisterTutorView

app_name = "api"
urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("auth/register/adotante/", RegisterAdotanteView.as_view(), name="register-adotante"),
    path("auth/register/tutor/", RegisterTutorView.as_view(), name="register-tutor"),
]
