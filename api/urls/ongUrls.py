from django.urls import path

from api.views.ongView import OngView, OngDetailView

app_name = "api"
urlpatterns = [
    path("ong/", OngView.as_view(), name="ong-list"),
    path("ong/<int:pk>/", OngDetailView.as_view(), name="ong-detail"),
]
