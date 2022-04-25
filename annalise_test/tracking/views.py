from rest_framework import permissions, viewsets

from annalise_test.tracking.models import APIInteractionTracking
from annalise_test.tracking.serializers import APIInteractionTrackingSerializer


class APIInteractionTrackingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing user api interactions.
    """

    queryset = APIInteractionTracking.objects.order_by("-created_at")
    serializer_class = APIInteractionTrackingSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ("user", "endpoint")
