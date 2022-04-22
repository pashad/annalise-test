from rest_framework import viewsets
from rest_framework import permissions

from annalise_test.images.filters import AnnaliseImageFilter
from annalise_test.images.models import AnnaliseImage, ImageTag
from annalise_test.images.serializers import AnnaliseImageSerializer, ImageTagSerializer


class AnnaliseImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations with AnnaliseImages.
    """
    queryset = AnnaliseImage.objects.all().order_by('-created_at')
    serializer_class = AnnaliseImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = AnnaliseImageFilter


class ImageTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations with ImageTags.
    """
    queryset = ImageTag.objects.all()
    serializer_class = ImageTagSerializer
    permission_classes = [permissions.IsAuthenticated]
