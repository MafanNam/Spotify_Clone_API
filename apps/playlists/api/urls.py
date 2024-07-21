from django.urls import path

from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.PlaylistListAPIView.as_view(), name="playlist-list"),
    path("recently/", views.PlaylistRecentlyPlayedAPIView.as_view(), name="playlist-recently-played"),
    path("favorite/", views.PlaylistFavoriteListAPIView.as_view(), name="playlist-favorite"),
    path("my/", views.MyPlaylistListCreateAPIView.as_view(), name="playlist-list-my"),
    path("my/<slug:slug>/", views.MyPlaylistDetailAPIView.as_view(), name="playlist-detail-my"),
    path("<slug:slug>/", views.PlaylistDetailAPIView.as_view(), name="playlist-detail"),
    path(
        "<slug:slug>/favorite/", views.PlaylistFavoriteCreateAPIView.as_view(), name="playlist-favorite-create-delete"
    ),
    path(
        "<slug:slug>/add/tracks/<slug:track_slug>/",
        views.AddRemoveTrackPlaylistAPIView.as_view(),
        name="playlist-track-add-delete",
    ),
]
