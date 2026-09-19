from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            "id",
            "document",
            "title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField(
        min_length=1,
        max_length=10000,
    )


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Chat
        fields = [
            "id",
            "document",
            "title",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = [
            "id",
            "document",
            "created_at",
            "updated_at",
            "messages",
        ]