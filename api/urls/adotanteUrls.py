from django.urls import path

from api.views.adotanteView import (
    AdotanteView,
    AdotanteDetailView,
    AdotantePorUsuarioView,
)

app_name = "api"
urlpatterns = [
    path("adotante/", AdotanteView.as_view(), name="adotante-list"),
    path("adotante/<int:pk>/", AdotanteDetailView.as_view(), name="adotante-detail"),
    path(
        "adotante/usuario/<int:user_id>/",
        AdotantePorUsuarioView.as_view(),
        name="adotante-por-usuario",
    ),
]
