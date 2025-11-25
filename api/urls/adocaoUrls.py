from django.urls import path

from api.views.adocaoView import (
    AdocaoView,
    AdocaoDetailView,
    AdocaoPorUsuarioView,
    PetAdotadoView,
)

app_name = "api"
urlpatterns = [
    path("adocao/", AdocaoView.as_view(), name="adocao-list"),
    path("adocao/<int:pk>/", AdocaoDetailView.as_view(), name="adocao-detail"),
    path(
        "adocao/usuario/<int:user_id>/",
        AdocaoPorUsuarioView.as_view(),
        name="adocao-por-usuario",
    ),
    path(
        "adocao/pet/<int:pet_id>/adotado/",
        PetAdotadoView.as_view(),
        name="pet-adotado",
    ),
]
