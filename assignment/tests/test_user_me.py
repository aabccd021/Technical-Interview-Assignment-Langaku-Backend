import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestUserMeEndpoint:

    def test_me_endpoint_with_mock_middleware_authentication(self):
        """Test that user can authenticate via X-User-NAME header"""
        client = APIClient()
        response = client.get(reverse("user-me"), HTTP_X_USER_NAME="testuser")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"username": "testuser"}

    def test_me_endpoint_with_non_existent_user_header(self):
        """Test that non-existent user in header returns 401"""
        response = client.get(reverse("user-me"), HTTP_X_USER_NAME="nonexistentuser")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
