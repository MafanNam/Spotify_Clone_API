from django.urls import path

from . import views

app_name = "audio"

urlpatterns = [
    path("my/", views.TrackMyListCreateAPIView.as_view(), name="audio-list-create-my"),
    path("my/<slug:slug>/", views.TrackMyDetailAPIView.as_view(), name="audio-detail-my"),
    path("my/<slug:slug>/listen/", views.StreamingMyTrackAPIView.as_view(), name="audio-listen-my"),
    path("", views.TrackListAPIView.as_view(), name="audio-list"),
    path("<slug:slug>/", views.TrackDetailAPIView.as_view(), name="audio-detail"),
    path("<slug:slug>/listen/", views.StreamingTrackAPIView.as_view(), name="audio-listen"),
]
