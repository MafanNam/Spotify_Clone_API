from django.urls import path

from . import views

app_name = "artists"

urlpatterns = [
    path("me/", views.ArtistDetailMeAPIView.as_view(), name="artist-me"),
    # path("me/verify/", views.ArtistVerifyMeAPIView.as_view(), name="artist-verify-me"),
    path("me/license/", views.LicenseListCreateAPIView.as_view(), name="license-list-create"),
    path("me/license/<int:pk>/", views.LicenseRetrieveUpdateDestroyAPIView.as_view(), name="license-detail"),
    path("", views.ArtistListCreateAPIView.as_view(), name="artist-list-create"),
    path("<slug:slug>/", views.ArtistDetailAPIView.as_view(), name="artist-detail"),
]
