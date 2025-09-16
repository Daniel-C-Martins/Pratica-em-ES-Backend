from django.urls import path

from api.views.preferenciaAdotante import (
    PreferenciaAdotanteView,
    PreferenciaAdotanteDetailView,
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
]
