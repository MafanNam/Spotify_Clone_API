from rest_framework import serializers

from apps.payments.models import Payment, Tax
from apps.users.api.serializers import ShortCustomUserSerializer


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ["id", "name", "value"]


class PaymentListSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(read_only=True, many=False)
    user = ShortCustomUserSerializer(read_only=True, many=False)

    class Meta:
        model = Payment
        fields = ["id", "payment_id", "user", "method", "status", "price", "tax", "total_price"]
        extra_kwargs = {"total_price": {"read_only": True}}


class PaymentCreateSerializer(PaymentListSerializer):
    tax = serializers.PrimaryKeyRelatedField(queryset=Tax.objects.all(), many=False)
