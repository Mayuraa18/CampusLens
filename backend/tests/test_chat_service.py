import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from documents.models import Document
from conversations.models import Chat, Message


@pytest.fixture
def user():
    return User.objects.create_user(
        username="student",
        password="TestPassword123!",
    )


@pytest.fixture
def document(user):
    return Document.objects.create(
        user=user,
        title="Examination Notice",
    )


@pytest.fixture
def chat(user, document):
    return Chat.objects.create(
        user=user,
        document=document,
        title="Exam Notice Chat",
    )


@pytest.mark.django_db
def test_successful_chat_message(
        user,
        chat,
        monkeypatch,
):
    client = APIClient()
    client.force_authenticate(user=user)

    def mock_generate_chat_response(chat, user_message):
        return {
            "answer": (
                "You need to submit the examination form "
                "by 20 October 2026. [Source: Page 1]"
            ),
            "sources": [
                {
                    "page_number": 1,
                }
            ],
        }

    monkeypatch.setattr(
        "conversations.views.generate_chat_response",
        mock_generate_chat_response,
    )

    response = client.post(
        f"/api/chats/{chat.id}/messages/",
        {
            "content": "What do I need to do?",
        },
        format="json",
    )

    assert response.status_code == 201

    assert response.data["user_message"]["content"] == (
        "What do I need to do?"
    )

    assert response.data["assistant_message"]["content"] == (
        "You need to submit the examination form "
        "by 20 October 2026. [Source: Page 1]"
    )

    assert response.data["sources"] == [
        {
            "page_number": 1,
        }
    ]

    assert Message.objects.filter(
        chat=chat,
        role=Message.Role.USER,
    ).count() == 1

    assert Message.objects.filter(
        chat=chat,
        role=Message.Role.ASSISTANT,
    ).count() == 1

@pytest.mark.django_db
def test_chat_message_handles_ai_failure(
        user,
        chat,
        monkeypatch,
):
    client = APIClient()
    client.force_authenticate(user=user)

    def mock_generate_chat_response(chat, user_message):
        raise RuntimeError("AI service unavailable")

    monkeypatch.setattr(
        "conversations.views.generate_chat_response",
        mock_generate_chat_response,
    )

    response = client.post(
        f"/api/chats/{chat.id}/messages/",
        {
            "content": "What is the deadline?",
        },
        format="json",
    )

    assert response.status_code == 500
    assert response.data == {
        "detail": "Unable to generate an AI response."
    }

    # The user message is saved before AI generation.
    assert Message.objects.filter(
        chat=chat,
        role=Message.Role.USER,
    ).count() == 1

    # No assistant message should be created after the failure.
    assert Message.objects.filter(
        chat=chat,
        role=Message.Role.ASSISTANT,
    ).count() == 0