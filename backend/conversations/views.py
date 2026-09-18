from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatListView(APIView):
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():
            document = serializer.validated_data["document"]

            if document.user != request.user:
                return Response(
                    {"detail": "Document not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            chat = serializer.save(user=request.user)
            return Response(
                ChatSerializer(chat).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChatDetailView(APIView):
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

        serializer = ChatSerializer(chat)
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
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListView(APIView):
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

        messages = chat.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)

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

        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            message = serializer.save(chat=chat)

            return Response(
                MessageSerializer(message).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )