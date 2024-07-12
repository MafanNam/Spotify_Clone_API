from django.urls import path

from . import views

app_name = "audio"

urlpatterns = [
    path("my/", views.TrackMyListCreateAPIView.as_view(), name="audio-list-create-my"),
    path("my/<slug:slug>/", views.TrackMyDetailAPIView.as_view(), name="audio-detail-my"),
    path("my/<slug:slug>/listen/", views.StreamingMyTrackAPIView.as_view(), name="audio-listen-my"),
    path("", views.TrackListAPIView.as_view(), name="audio-list"),
    path("liked/", views.TrackLikedListAPIView.as_view(), name="audio-liked-list"),
    path("recently/", views.TrackRecentlyPlayedAPIView.as_view(), name="audio-recently-played"),
    path(
        "recently/user/<int:id>/",
        views.TrackRecentlyPlayedByUserAPIView.as_view(),
        name="audio-recently-played-by-user",
    ),
    path("<slug:slug>/", views.TrackDetailAPIView.as_view(), name="audio-detail"),
    path("<slug:slug>/listen/", views.StreamingTrackAPIView.as_view(), name="audio-listen"),
    path("<slug:slug>/download/", views.DownloadTrackAPIView.as_view(), name="audio-download"),
    path("<slug:slug>/like/", views.TrackLikeAPIView.as_view(), name="audio-like"),
    path("<slug:slug>/unlike/", views.TrackUnlikeAPIView.as_view(), name="audio-unlike"),
]
