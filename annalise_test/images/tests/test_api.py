from datetime import date
from pathlib import Path
from typing import List

from django.contrib.auth.models import User
from django.core.files import File
from rest_framework.test import APITestCase

from annalise_test.images.models import AnnaliseImage, ImageTag


class AnnaliseImageTest(APITestCase):
    created_images: List[AnnaliseImage] = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # create user
        cls.test_user = User.objects.create_user("username", "Pas$w0rd")

        # create tags
        for tag in ("test tag 1", "test tag 2", "test tag 3"):
            ImageTag.objects.create(name=tag)

        # create images
        for image_file in ("6678.png", "396690.png"):
            with open(Path(__file__).parent.joinpath(f"test_images/{image_file}"), "rb") as f:
                image_obj = AnnaliseImage()
                image_obj.image = File(f)
                image_obj.image.name = image_file
                image_obj.save()
                cls.created_images.append(image_obj)

    @classmethod
    def tearDownClass(cls):
        for image_obj in cls.created_images:
            image_obj.delete()  # delete image from disk
        super().tearDownClass()

    def setUp(self):
        self.client.force_authenticate(user=self.test_user)

    def test_api_endpoints(self):
        response = self.client.get("/api/")

        assert response.status_code == 200
        assert "images" in response.json()
        assert "tags" in response.json()

    def test_authentication_required(self):
        # unauthenticate requests
        self.client.force_authenticate(user=None)

        images_response = self.client.get("/api/images/")
        tags_response = self.client.get("/api/tags/")

        assert images_response.status_code == tags_response.status_code == 403
        default_403_response = {"detail": "Authentication credentials were not provided."}
        assert images_response.json() == tags_response.json() == default_403_response

    def test_images_endpoint(self):
        # list all images
        list_response = self.client.get("/api/images/")
        assert list_response.status_code == 200
        assert list_response.json()["count"] == 2

        # create image
        with open(Path(__file__).parent.joinpath("test_images/6678.png"), "rb") as f:
            post_response = self.client.post(
                "/api/images/", {"tags": ["test tag 1", "test tag 2"], "image": f}, format="multipart"
            )
        assert post_response.status_code == 201
        image_data = post_response.json()
        assert image_data["image"].startswith("http://testserver/media/")
        assert image_data["tags"] == ["test tag 1", "test tag 2"]
        image_id = image_data["id"]

        # patch image tags
        patch_response = self.client.patch(
            f"/api/images/{image_id}/", {"tags": ["test tag 1", "test tag 2", "test tag 3"]}
        )
        assert patch_response.status_code == 200
        assert len(patch_response.json()["tags"]) == 3

        # search images
        tag_search_response = self.client.get("/api/images/", data={"tags": "test tag 3"})
        assert tag_search_response.status_code == 200
        assert tag_search_response.json()["count"] == 1
        date_search_response = self.client.get("/api/images/", data={"start_date": date.today().isoformat()})
        assert date_search_response.json()["count"] >= 1

        # delete image
        delete_response = self.client.delete(f"/api/images/{image_id}/")
        assert delete_response.status_code == 204

    def test_tags_endpoint(self):
        # list all tags
        list_response = self.client.get("/api/tags/")
        assert list_response.status_code == 200
        assert list_response.json()["count"] == 3

        # create tag
        post_response = self.client.post("/api/tags/", {"name": "test tag 444"})
        assert post_response.status_code == 201
        tag_name = post_response.json()["name"]

        # search tags
        name_search_response = self.client.get("/api/tags/", data={"name": "444"})
        assert name_search_response.status_code == 200
        assert name_search_response.json()["count"] == 1

        # delete tag
        delete_response = self.client.delete(f"/api/tags/{tag_name}/")
        assert delete_response.status_code == 204
