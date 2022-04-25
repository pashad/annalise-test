from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from annalise_test import settings
from annalise_test.images import views as images_views
from annalise_test.tracking import views as tracking_views


router = routers.DefaultRouter()
router.register(r"images", images_views.AnnaliseImageViewSet)
router.register(r"tags", images_views.ImageTagViewSet)
router.register(r"trackings", tracking_views.APIInteractionTrackingViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
