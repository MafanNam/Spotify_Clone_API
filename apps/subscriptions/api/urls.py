from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.SubscriptionsAPIView.as_view(), name="subscriptions"),
    path("<int:pk>/", views.SubscriptionPlanDetailAPIView.as_view(), name="subscriptions-detail"),
]
