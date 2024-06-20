from rest_framework import generics, permissions

from apps.analytics.models import TrackPlayed
from apps.core.permissions import IsOwnerUserPermission
