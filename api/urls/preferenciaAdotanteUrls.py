from django.urls import path

from api.views.preferenciaAdotante import (
    PreferenciaAdotanteView,
    PreferenciaAdotanteDetailView,
    PreferenciaPorUsuarioView,
)

app_name = "api"
urlpatterns = [
    path(
        "preferencia-adotante/",
        PreferenciaAdotanteView.as_view(),
        name="preferencia-adotante-list",
    ),
    path(
        "preferencia-adotante/<int:pk>/",
        PreferenciaAdotanteDetailView.as_view(),
        name="preferencia-adotante-detail",
    ),
    path(
        "preferencia-adotante/usuario/<int:user_id>/",
        PreferenciaPorUsuarioView.as_view(),
        name="preferencia-por-usuario",
    ),
]
