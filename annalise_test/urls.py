from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from annalise_test import settings
from annalise_test.images import views


router = routers.DefaultRouter()
router.register(r'images', views.AnnaliseImageViewSet)
router.register(r'tags', views.ImageTagViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
