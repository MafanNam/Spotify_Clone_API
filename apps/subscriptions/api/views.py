from rest_framework import generics, permissions

from apps.subscriptions.api.serializers import SubscriptionPlanSerializer
from apps.subscriptions.models import SubscriptionPlan


class SubscriptionsAPIView(generics.ListAPIView):
    """
    List all subscriptions.
    """

    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class SubscriptionPlanDetailAPIView(generics.RetrieveAPIView):
    """
    Get subscription detail by id.
    """

    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]
