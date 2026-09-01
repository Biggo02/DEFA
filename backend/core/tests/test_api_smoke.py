from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class DefaApiSmokeTests(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username="defa-test-client",
            password="TestPassword-2026!",
        )

    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))

    def test_unauthenticated_profile_is_rejected(self):
        response = self.client.get("/me/")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_authenticated_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/me/")
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))

    def test_unauthenticated_payment_collection_is_rejected(self):
        response = self.client.post("/payments/collect/", {"amount": "100"}, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_invalid_qr_does_not_return_success(self):
        response = self.client.get("/qr/defa-invalid-smoke-token-0001/")
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_application_endpoint_requires_authentication(self):
        response = self.client.get("/applications/")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
