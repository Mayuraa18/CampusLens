import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from documents.models import Document


@pytest.fixture
def user():
    return User.objects.create_user(
        username="student",
        password="TestPassword123!",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="otherstudent",
        password="TestPassword123!",
    )


@pytest.fixture
def document(user, tmp_path):
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes(b"%PDF-1.4 test")

    document = Document.objects.create(
        user=user,
        title="Test Document",
        file=str(file_path),
    )

    return document


@pytest.mark.django_db
def test_chat_list_requires_authentication(document):
    client = APIClient()

    response = client.get(
        f"/api/documents/{document.id}/chats/"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_chat(user, document):
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        f"/api/documents/{document.id}/chats/",
        {
            "title": "Exam Notice Chat",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["title"] == "Exam Notice Chat"
    assert response.data["document"] == document.id


@pytest.mark.django_db
def test_list_user_chats(user, document):
    client = APIClient()
    client.force_authenticate(user=user)

    client.post(
        f"/api/documents/{document.id}/chats/",
        {
            "title": "Exam Notice Chat",
        },
        format="json",
    )

    response = client.get(
        f"/api/documents/{document.id}/chats/"
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Exam Notice Chat"


@pytest.mark.django_db
def test_user_cannot_access_another_users_document_chats(
        user,
        other_user,
        document,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.get(
        f"/api/documents/{document.id}/chats/"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_empty_message_is_rejected(user, document):
    client = APIClient()
    client.force_authenticate(user=user)

    create_response = client.post(
        f"/api/documents/{document.id}/chats/",
        {
            "title": "Test Chat",
        },
        format="json",
    )

    chat_id = create_response.data["id"]

    response = client.post(
        f"/api/chats/{chat_id}/messages/",
        {
            "content": "",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_oversized_message_is_rejected(user, document):
    client = APIClient()
    client.force_authenticate(user=user)

    create_response = client.post(
        f"/api/documents/{document.id}/chats/",
        {
            "title": "Test Chat",
        },
        format="json",
    )

    chat_id = create_response.data["id"]

    response = client.post(
        f"/api/chats/{chat_id}/messages/",
        {
            "content": "A" * 10001,
        },
        format="json",
    )

    assert response.status_code == 400