from django.urls import path

from .views import (
    ChatDetailView,
    ChatListView,
    MessageListView,
)

urlpatterns = [
    path("chats/", ChatListView.as_view(), name="chat-list"),
    path("chats/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
    path(
        "chats/<int:chat_id>/messages/",
        MessageListView.as_view(),
        name="message-list",
    ),
]