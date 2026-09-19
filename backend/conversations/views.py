from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document

from .models import Chat, Message
from .serializers import (
    ChatDetailSerializer,
    ChatSerializer,
    MessageCreateSerializer,
    MessageSerializer,
)
from .services.chat_service import generate_chat_response


class DocumentChatListView(APIView):
    """
    Create and list chats belonging to a document.
    """

    def get(self, request, document_id):
        try:
            document = Document.objects.get(
                pk=document_id,
                user=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        chats = Chat.objects.filter(
            document=document,
            user=request.user,
        ).order_by("-updated_at")

        serializer = ChatSerializer(
            chats,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, document_id):
        try:
            document = Document.objects.get(
                pk=document_id,
                user=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        title = request.data.get(
            "title",
            "New Chat",
        )

        chat = Chat.objects.create(
            user=request.user,
            document=document,
            title=title,
        )

        serializer = ChatSerializer(chat)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ChatDetailView(APIView):
    """
    Retrieve or delete a chat belonging to the authenticated user.
    """

    def get(self, request, pk):
        try:
            chat = Chat.objects.get(
                pk=pk,
                user=request.user,
            )
        except Chat.DoesNotExist:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ChatDetailSerializer(chat)

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            chat = Chat.objects.get(
                pk=pk,
                user=request.user,
            )
        except Chat.DoesNotExist:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        chat.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class ChatMessageListView(APIView):
    """
    List messages or send a new message to a chat.
    """

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(
                pk=chat_id,
                user=request.user,
            )
        except Chat.DoesNotExist:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        messages = Message.objects.filter(
            chat=chat,
        ).order_by("created_at")

        serializer = MessageSerializer(
            messages,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(
                pk=chat_id,
                user=request.user,
            )
        except Chat.DoesNotExist:
            return Response(
                {"detail": "Chat not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MessageCreateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_content = serializer.validated_data["content"]

        user_message = Message.objects.create(
            chat=chat,
            role=Message.Role.USER,
            content=user_content,
        )

        try:
            result = generate_chat_response(
                chat=chat,
                user_message=user_content,
            )
        except Exception:
            return Response(
                {
                    "detail": (
                        "Unable to generate an AI response."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        assistant_message = Message.objects.create(
            chat=chat,
            role=Message.Role.ASSISTANT,
            content=result["answer"],
        )

        chat.save(
            update_fields=["updated_at"],
        )

        return Response(
            {
                "user_message": MessageSerializer(
                    user_message,
                ).data,
                "assistant_message": MessageSerializer(
                    assistant_message,
                ).data,
                "sources": result["sources"],
            },
            status=status.HTTP_201_CREATED,
        )