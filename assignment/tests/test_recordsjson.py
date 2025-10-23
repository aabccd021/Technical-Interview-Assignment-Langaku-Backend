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
    response = APIClient().post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_duplicate_request_id_idempotent():
    client = APIClient()
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": 42,
    }
    client.post(
        "/recordsjson",
        request,
    )
    response = client.post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.django_db
def test_missing_field_bad_request():
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        # "word_count" is missing
    }
    response = APIClient().post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_field_type_bad_request():
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": "forty-two",  # invalid type
    }
    response = APIClient().post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_recordsjson_with_timestamp_success():
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": 42,
        "timestamp": "2024-01-01T12:00:00Z",
    }
    response = APIClient().post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_timestamp_with_timezone_success():
    request = {
        "request_id": str(uuid.uuid4()),
        "user_id": "langaku",
        "word_count": 42,
        "timestamp": "2024-01-01T12:00:00+09:00",
    }
    response = APIClient().post(
        "/recordsjson",
        request,
    )
    assert response.status_code == status.HTTP_201_CREATED
