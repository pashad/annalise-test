from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class APIInteractionTrackingTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # create users
        cls.test_user = User.objects.create_user("username", "Pas$w0rd")
        cls.test_superadmin = User.objects.create_superuser("admin", "AdminPas$w0rd")

    def setUp(self):
        self.client.force_authenticate(user=self.test_user)

    def test_trackings(self):
        # create tracking record in DB
        response = self.client.get("/api/")
        assert response.status_code == 200

        test_user_response = self.client.get("/api/trackings/")
        assert test_user_response.status_code == 403

        # admin
        self.client.force_authenticate(user=self.test_superadmin)
        admin_response = self.client.get("/api/trackings/")
        assert admin_response.status_code == 200
        assert admin_response.json()["count"] >= 1
