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
        {"period": "2024-01-01T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 42.0},
        {"period": "2024-01-03T00:00:00Z", "average_words_learned": 0.0},
    ]


@pytest.mark.django_db
def test_recordsjson_multiuser():
    client = APIClient()
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "user1",
            "word_count": 30,
            "timestamp": "2024-01-02T10:00:00Z",
        },
    )
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "user2",
            "word_count": 50,
            "timestamp": "2024-01-02T11:00:00Z",
        },
    )
    response_user1 = client.get(
        "/users/user1/summary",
        {"from": "2024-01-01", "to": "2024-01-03", "granularity": "day"},
    )
    response_user2 = client.get(
        "/users/user2/summary",
        {"from": "2024-01-01", "to": "2024-01-03", "granularity": "day"},
    )
    assert response_user1.status_code == status.HTTP_200_OK
    assert response_user1.data == [
        {"period": "2024-01-01T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 30.0},
        {"period": "2024-01-03T00:00:00Z", "average_words_learned": 0.0},
    ]
    assert response_user2.status_code == status.HTTP_200_OK
    assert response_user2.data == [
        {"period": "2024-01-01T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 50.0},
        {"period": "2024-01-03T00:00:00Z", "average_words_learned": 0.0},
    ]


@pytest.mark.django_db
def test_user_summary_single_day():
    client = APIClient()
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "langaku",
            "word_count": 100,
            "timestamp": "2024-01-15T09:00:00Z",
        },
    )

    response = client.get(
        "/users/langaku/summary",
        {"from": "2024-01-15", "to": "2024-01-15", "granularity": "day"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {"period": "2024-01-15T00:00:00Z", "average_words_learned": 100.0},
    ]


@pytest.mark.django_db
def test_user_summary_no_activity():
    client = APIClient()

    response = client.get(
        "/users/emptyuser/summary",
        {"from": "2024-01-01", "to": "2024-01-03", "granularity": "day"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {"period": "2024-01-01T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-03T00:00:00Z", "average_words_learned": 0.0},
    ]


@pytest.mark.django_db
def test_user_summary_active_on_even_days():
    client = APIClient()
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "langaku",
            "word_count": 100,
            "timestamp": "2024-01-02T09:00:00Z",
        },
    )
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "langaku",
            "word_count": 200,
            "timestamp": "2024-01-04T09:00:00Z",
        },
    )
    client.post(
        "/recordsjson",
        {
            "request_id": str(uuid.uuid4()),
            "user_id": "langaku",
            "word_count": 300,
            "timestamp": "2024-01-06T09:00:00Z",
        },
    )
    response = client.get(
        "/users/langaku/summary",
        {"from": "2024-01-01", "to": "2024-01-07", "granularity": "day"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {"period": "2024-01-01T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-02T00:00:00Z", "average_words_learned": 100.0},
        {"period": "2024-01-03T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-04T00:00:00Z", "average_words_learned": 200.0},
        {"period": "2024-01-05T00:00:00Z", "average_words_learned": 0.0},
        {"period": "2024-01-06T00:00:00Z", "average_words_learned": 300.0},
        {"period": "2024-01-07T00:00:00Z", "average_words_learned": 0.0},
    ]
