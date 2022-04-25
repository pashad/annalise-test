from rest_framework import serializers

from annalise_test.images.models import AnnaliseImage, ImageTag


class ImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTag
        fields = ["name"]


class AnnaliseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnaliseImage
        fields = ["id", "image", "tags"]
