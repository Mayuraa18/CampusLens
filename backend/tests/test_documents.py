import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_document_list_requires_authentication():
    client = APIClient()

    response = client.get("/api/documents/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_document_list_authenticated_user():
    user = User.objects.create_user(
        username="student",
        password="TestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/documents/")

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_user_only_sees_own_documents():
    user1 = User.objects.create_user(
        username="student1",
        password="TestPassword123!",
    )

    user2 = User.objects.create_user(
        username="student2",
        password="TestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=user1)

    response = client.get("/api/documents/")

    assert response.status_code == 200
    assert response.data == []