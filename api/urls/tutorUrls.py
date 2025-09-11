from django.urls import path

from api.views.tutorView import TutorView, TutorDetailView

app_name = "api"
urlpatterns = [
    path("tutor/", TutorView.as_view(), name="tutor-list"),
    path("tutor/<int:pk>/", TutorDetailView.as_view(), name="tutor-detail"),
]
