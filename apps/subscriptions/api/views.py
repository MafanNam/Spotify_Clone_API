from rest_framework import generics, permissions

from apps.subscriptions.api.serializers import SubscriptionPlanSerializer
from apps.subscriptions.models import SubscriptionPlan


class SubscriptionsAPIView(generics.ListCreateAPIView):
    """
    List all subscriptions.
    Only admin can create subscription.
    """

    queryset = SubscriptionPlan.objects.prefetch_related("feature").all()
    serializer_class = SubscriptionPlanSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class SubscriptionPlanDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get subscription detail by id.
    Only admin can update and delete subscription.
    """

    queryset = SubscriptionPlan.objects.prefetch_related("feature").all()
    serializer_class = SubscriptionPlanSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
