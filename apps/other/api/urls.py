from django.urls import path

from . import views

app_name = "other"

urlpatterns = [
    path("genres/", views.GenreListAPIView.as_view(), name="genre-list"),
    path("genres/<int:pk>/", views.GenreDetailAPIView.as_view(), name="genre-detail"),
]
