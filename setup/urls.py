from django.contrib import admin
from django.urls import path, include
from django_scalar import views as scalar_views
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", scalar_views.scalar_viewer, name="docs"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls.racasPetUrls", namespace="racasPet")),
    path("api/", include("api.urls.statusPetUrls", namespace="statusPet")),
    path("api/", include("api.urls.tutorUrls", namespace="tutor")),
    path("api/", include("api.urls.petUrls", namespace="pet")),
    path("api/", include("api.urls.ongUrls", namespace="ong")),
    path("api/", include("api.urls.adotanteUrls", namespace="adotante")),
    path("api/", include("api.urls.adocaoUrls", namespace="adocao")),
    path("api/", include("api.urls.eventoUrls", namespace="evento")),
    path("api/", include("api.urls.especiePetUrls", namespace="especiePet")),
    path(
        "api/",
        include("api.urls.preferenciaAdotanteUrls", namespace="preferenciaAdotante"),
    ),
    path("api/", include("api.urls.rastreioUrls", namespace="rastreio")),
    path("api/", include("api.urls.authUrls", namespace="auth")),
]
