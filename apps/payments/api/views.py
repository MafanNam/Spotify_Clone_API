from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from apps.payments.api.serializers import PaymentCreateSerializer, PaymentListSerializer, TaxSerializer
from apps.payments.models import Payment, Tax


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    """
    Payment list and create view. Only for authenticated users.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentCreateSerializer
        return PaymentListSerializer


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    Payment retrieve view. Only for authenticated users and owner of the payment.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentListSerializer
    lookup_field = "payment_id"

    def get_object(self):
        return get_object_or_404(self.request.user.payments, payment_id=self.kwargs["payment_id"])


class TaxListAPIView(generics.ListAPIView):
    """
    Tax list view. Public view.
    """

    queryset = Tax.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TaxSerializer
