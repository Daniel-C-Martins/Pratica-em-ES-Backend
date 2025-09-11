from django.urls import path

from api.views.especiePetView import EspeciePetView, EspeciePetDetailView

app_name = "api"
urlpatterns = [
    path("especie-pet/", EspeciePetView.as_view(), name="especie-pet-list"),
    path(
        "especie-pet/<int:pk>/",
        EspeciePetDetailView.as_view(),
        name="especie-pet-detail",
    ),
]
