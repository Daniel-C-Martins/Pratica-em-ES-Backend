from django.urls import path

from api.views.rastreioView import RastreioView, RastreioDetailView, RastreioPorPet

app_name = "api"
urlpatterns = [
    path("rastreio/", RastreioView.as_view(), name="rastreio-list"),
    path("rastreio/<int:pk>/", RastreioDetailView.as_view(), name="rastreio-detail"),
    path(
        "rastreio/pet/<int:pet_id>/", RastreioPorPet.as_view(), name="rastreio-por-pet"
    ),
]
