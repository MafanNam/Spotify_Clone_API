from django.urls import path

from . import views

app_name = "artists"

urlpatterns = [
    path("me/", views.ArtistDetailMeAPIView.as_view(), name="artist-me"),
    path("me/image/", views.MyArtistImageAPIView.as_view(), name="update-my-artist-profile-image"),
    path("me/verify/", views.ArtistVerifyMeAPIView.as_view(), name="artist-verify-me"),
    path("me/license/", views.LicenseListCreateAPIView.as_view(), name="license-list-create"),
    path("me/license/<int:pk>/", views.LicenseRetrieveUpdateDestroyAPIView.as_view(), name="license-detail"),
    path("", views.ArtistListCreateAPIView.as_view(), name="artist-list-create"),
    path("favorite/", views.ArtistFavoriteListAPIView.as_view(), name="artist-favorite"),
    path("<slug:slug>/", views.ArtistDetailAPIView.as_view(), name="artist-detail"),
    path("<slug:slug>/favorite/", views.ArtistFavoriteCreateAPIView.as_view(), name="artist-favorite-create-delete"),
]
