from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.PaymentListCreateAPIView.as_view(), name="payment-list-create"),
    path("<int:pk>/", views.PaymentRetrieveAPIView.as_view(), name="payment-retrieve"),
    path("tax/", views.TaxListAPIView.as_view(), name="tax-list"),
]