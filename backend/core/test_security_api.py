from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class DefaSecurityApiTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.client_user = User.objects.create_user(username="defa-client", password="safe-test-password")
        self.agent = User.objects.create_user(username="defa-agent", password="safe-test-password")
        self.admin = User.objects.create_user(username="defa-admin", password="safe-test-password", is_staff=True)

    def test_anonymous_cannot_create_application(self):
        response = self.client.post("/api/applications/", {}, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_client_cannot_collect_payment(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post("/api/payments/collect/", {"loan": 999999, "amount": 100}, format="json")
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST))

    def test_anonymous_cannot_collect_payment(self):
        response = self.client.post("/api/payments/collect/", {"loan": 999999, "amount": 100}, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_client_cannot_decide_application(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post("/api/applications/999999/decision/", {"decision": "APPROVE"}, format="json")
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))

    def test_negative_payment_is_rejected(self):
        self.client.force_authenticate(user=self.agent)
        response = self.client.post("/api/payments/collect/", {"loan": 999999, "amount": -1}, format="json")
        self.assertIn(response.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))
