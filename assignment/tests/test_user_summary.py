import pytest
from rest_framework.test import APIClient
from rest_framework import status
import uuid


@pytest.mark.django_db
def test_recordsjson_with_timestamp_success():
    client = APIClient()
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": 42,
        "timestamp": "2024-01-02T12:00:00Z",
    }
    client.post("/recordsjson", request, format="json")

    response = client.get(
        "/users/langaku/summary",
        {"from": "2024-01-01", "to": "2024-01-03", "granularity": "day"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
