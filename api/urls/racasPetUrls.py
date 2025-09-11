from django.urls import path

from api.views.racasPetView import RacasPetView, RacasPetDetailView

app_name = "api"
urlpatterns = [
    path("racasPet/", RacasPetView.as_view(), name="racasPet-list"),
    path("racasPet/<int:pk>/", RacasPetDetailView.as_view(), name="racasPet-detail"),
]
