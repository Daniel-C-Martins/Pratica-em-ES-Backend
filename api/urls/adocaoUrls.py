from django.urls import path

from api.views.adocaoView import AdocaoView, AdocaoDetailView

app_name = "api"
urlpatterns = [
    path("adocao/", AdocaoView.as_view(), name="adocao-list"),
    path("adocao/<int:pk>/", AdocaoDetailView.as_view(), name="adocao-detail"),
]
