import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    response = client.post(
        "/api/auth/register/",
        {
            "username": "teststudent",
            "email": "teststudent@example.com",
            "password": "TestPassword123!",
        },
        format="json",
    )

    assert response.status_code == 201
    assert User.objects.filter(
        username="teststudent"
    ).exists()


@pytest.mark.django_db
def test_login_user():
    User.objects.create_user(
        username="teststudent",
        email="teststudent@example.com",
        password="TestPassword123!",
    )

    client = APIClient()

    response = client.post(
        "/api/auth/token/",
        {
            "username": "teststudent",
            "password": "TestPassword123!",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_protected_endpoint_requires_authentication():
    client = APIClient()

    response = client.get("/api/documents/")

    assert response.status_code == 401