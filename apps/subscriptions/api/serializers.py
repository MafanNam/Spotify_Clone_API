from rest_framework import serializers

from apps.subscriptions.models import Feature, SubscriptionPlan


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "permission"]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "price", "description", "days_exp", "feature"]
