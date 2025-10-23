import pytest
from rest_framework.test import APIClient
from rest_framework import status
import uuid
import datetime


@pytest.mark.django_db
def test_recordsjson_with_timestamp_success():
    client = APIClient()
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "langaku",
            "word_count": 42,
            "timestamp": "2024-01-02T12:00:00Z",
        },
    )

    response = client.get(
        "/users/langaku/summary",
        {"from": "2024-01-01", "to": "2024-01-03", "granularity": "day"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 42.0},
    ]
