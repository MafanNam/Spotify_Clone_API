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
    path("users/me/spam-email-every-week/", views.SpamEmailEveryWeek.as_view(), name="spam-email-every-week"),
    path("users/<int:user_id>/follow/", views.UserFollowAPIView.as_view(), name="user-follow"),
    path("users/<int:user_id>/unfollow/", views.UserUnfollowAPIView.as_view(), name="user-unfollow"),
    path("users/<int:user_id>/followers/", views.ListUserFollowersAPIView.as_view(), name="list-user-followers"),
    path("users/<int:user_id>/following/", views.ListUserFollowingAPIView.as_view(), name="list-user-following"),
    path("users/profiles/", views.ListUsersProfileAPIView.as_view(), name="list-users-profile"),
    path("users/profiles/my/", views.DetailMyUserProfileAPIView.as_view(), name="detail-my-user-profile"),
    path("users/profiles/my/image/", views.MyUserProfileImageAPIView.as_view(), name="update-my-user-profile-image"),
]
