from django.urls import path

from .views import (
    ChatDetailView,
    ChatMessageListView,
    DocumentChatListView,
)

urlpatterns = [
    path(
        "documents/<int:document_id>/chats/",
        DocumentChatListView.as_view(),
        name="document-chat-list",
    ),
    path(
        "chats/<int:pk>/",
        ChatDetailView.as_view(),
        name="chat-detail",
    ),
    path(
        "chats/<int:chat_id>/messages/",
        ChatMessageListView.as_view(),
        name="chat-messages",
    ),
]