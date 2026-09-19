import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from conversations.models import Chat
from documents.models import Document


@pytest.fixture
def user():
    return User.objects.create_user(
        username="student1",
        password="TestPassword123!",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="student2",
        password="TestPassword123!",
    )


@pytest.fixture
def document(user):
    return Document.objects.create(
        user=user,
        title="Private Document",
    )


@pytest.fixture
def chat(user, document):
    return Chat.objects.create(
        user=user,
        document=document,
        title="Private Chat",
    )


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_documents():
    client = APIClient()

    response = client.get("/api/documents/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_document(document):
    client = APIClient()

    response = client.get(
        f"/api/documents/{document.id}/"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cannot_access_another_users_document(
        other_user,
        document,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.get(
        f"/api/documents/{document.id}/"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_delete_another_users_document(
        other_user,
        document,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.delete(
        f"/api/documents/{document.id}/"
    )

    assert response.status_code == 404
    assert Document.objects.filter(id=document.id).exists()


@pytest.mark.django_db
def test_user_cannot_access_another_users_chat(
        other_user,
        chat,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.get(
        f"/api/chats/{chat.id}/"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_access_another_users_chat_messages(
        other_user,
        chat,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.get(
        f"/api/chats/{chat.id}/messages/"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_send_message_to_another_users_chat(
        other_user,
        chat,
):
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.post(
        f"/api/chats/{chat.id}/messages/",
        {
            "content": "Can I access this chat?",
        },
        format="json",
    )

    assert response.status_code == 404