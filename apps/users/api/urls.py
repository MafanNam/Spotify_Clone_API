from django.urls import include, path, re_path

from . import views

app_name = "users"

urlpatterns = [
    re_path(
        r"^auth/o/(?P<provider>\S+)/$",
        views.CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("auth/", include("djoser.urls")),
    path("auth/jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", views.CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/jwt/verify/", views.CustomTokenVerifyView.as_view(), name="jwt-verify"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/users/me/spam-email-every-week/", views.SpamEmailEveryWeek.as_view(), name="spam-email-every-week"),
    path("auth/users/<int:user_id>/follow/", views.UserFollowAPIView.as_view(), name="user-follow"),
    path("auth/users/<int:user_id>/unfollow/", views.UserUnfollowAPIView.as_view(), name="user-unfollow"),
]
