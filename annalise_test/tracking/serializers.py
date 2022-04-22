from rest_framework import serializers

from annalise_test.tracking.models import APIInteractionTracking


class APIInteractionTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIInteractionTracking
        fields = '__all__'
