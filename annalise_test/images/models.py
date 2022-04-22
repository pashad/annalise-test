from django.contrib.auth.models import User
from django.db import models


class ImageTag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)  # TODO: lower(?)


class AnnaliseImage(models.Model):
    # file will be saved to MEDIA_ROOT/images/2022/04/22
    image = models.ImageField(upload_to='images/%Y/%m/%d/')  # TODO: post_delete remove image from disk
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(ImageTag, blank=True)
