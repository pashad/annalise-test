from django.contrib.auth.models import User
from django.db import models


class APIInteractionTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    endpoint = models.CharField(max_length=100)
    headers = models.JSONField()
    status_code = models.IntegerField()
    data = models.JSONField()
    cookies = models.JSONField()
    method = models.CharField(max_length=8)
    response = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
