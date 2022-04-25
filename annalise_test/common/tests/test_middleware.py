from django.contrib.auth.models import User
from django.test import TestCase

from annalise_test import settings


class MediaProtectedTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.media_url = f"/{settings.MEDIA_URL}some/random/media/file/path.jpg"
        # create user
        cls.test_user = User.objects.create_user("username", "Pas$w0rd")

    def setUp(self) -> None:
        self.client.force_login(user=self.test_user)

    def test_media_endpoint_non_authorized(self) -> None:
        # non-authorized access
        self.client.logout()
        non_authorized_response = self.client.get(self.media_url)
        assert non_authorized_response.status_code == 403

    def test_media_endpoint_authorized(self) -> None:
        # authorized access
        authorized_response = self.client.get(self.media_url)
        assert authorized_response.status_code == 404
