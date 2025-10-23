import pytest
from rest_framework.test import APIClient
from rest_framework import status
import uuid

@pytest.mark.django_db
def test_recordsjson_success():
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": 42,
    }
    response = APIClient().post("/recordsjson", request, format="json")
    assert response.data == "OK"
    assert response.status_code == status.HTTP_200_OK
