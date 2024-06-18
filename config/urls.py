from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.users.api.urls"), name="users"),
    path("api/v1/subscriptions/", include("apps.subscriptions.api.urls"), name="subscriptions"),
    path("api/v1/payments/", include("apps.payments.api.urls"), name="payments"),
    path("api/v1/others/", include("apps.other.api.urls"), name="others"),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Schema URLs
urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Debug Tool Bar
urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
]
