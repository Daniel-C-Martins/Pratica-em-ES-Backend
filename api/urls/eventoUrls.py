from django.urls import path

from api.views.eventoView import EventoView, EventoDetailView

app_name = "api"
urlpatterns = [
    path("evento/", EventoView.as_view(), name="evento-list"),
    path("evento/<int:pk>/", EventoDetailView.as_view(), name="evento-detail"),
]
