from django.urls import path

from . import views

app_name = "albums"

urlpatterns = [
    path("", views.AlbumListCreateAPIView.as_view(), name="album-list-create"),
    path("my/", views.MyAlbumListCreateAPIView.as_view(), name="my-album-list-create"),
    path("my/<slug:slug>/", views.MyAlbumDetailAPIView.as_view(), name="my-album-detail"),
    path("<slug:slug>/", views.AlbumDetailAPIView.as_view(), name="album-detail"),
]
