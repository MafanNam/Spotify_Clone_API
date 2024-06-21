from django.urls import path

from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.PlaylistListAPIView.as_view(), name="playlist-list"),
    path("recently/", views.PlaylistRecentlyPlayedAPIView.as_view(), name="playlist-recently-played"),
    path("my/", views.MyPlaylistListCreateAPIView.as_view(), name="playlist-list-my"),
    path("my/<slug:slug>/", views.MyPlaylistDetailAPIView.as_view(), name="playlist-detail-my"),
    path("<slug:slug>/", views.PlaylistDetailAPIView.as_view(), name="playlist-detail"),
]
