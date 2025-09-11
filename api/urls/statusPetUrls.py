from django.urls import path

from api.views.statusPetView import StatusPetView, StatusPetDetailView

app_name = "api"
urlpatterns = [
    path("statusPet/", StatusPetView.as_view(), name="statusPet-list"),
    path("statusPet/<int:pk>/", StatusPetDetailView.as_view(), name="statusPet-detail"),
]
