from django.urls import path

from api.views.petView import PetView, PetDetailView, PetHeuristicaView

app_name = "api"
urlpatterns = [
    path("pet/", PetView.as_view(), name="pet-list"),
    path("pet/<int:pk>/", PetDetailView.as_view(), name="pet-detail"),
    path("pet/<int:id>/heuristica/", PetHeuristicaView.as_view(), name="pet-heuristica"),
]
