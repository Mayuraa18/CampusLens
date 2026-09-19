from rest_framework import serializers

from .models import (
    Action,
    Deadline,
    Document,
    ImportantDate,
)


class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = [
            "id",
            "date",
            "description",
            "page_number",
        ]


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = [
            "id",
            "date",
            "description",
            "page_number",
        ]


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = [
            "id",
            "action",
            "page_number",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "status",
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "uploaded_at",
            "updated_at",
        ]


class DocumentDetailSerializer(serializers.ModelSerializer):
    deadlines = DeadlineSerializer(
        many=True,
        read_only=True,
    )
    important_dates = ImportantDateSerializer(
        many=True,
        read_only=True,
    )
    actions = ActionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "status",
            "uploaded_at",
            "updated_at",
            "deadlines",
            "important_dates",
            "actions",
        ]

class InsightsSerializer(serializers.Serializer):
    summary = serializers.CharField(
        read_only=True,
    )
    stats = serializers.DictField(
        read_only=True,
    )
    deadlines = DeadlineSerializer(
        many=True,
        read_only=True,
    )
    important_dates = ImportantDateSerializer(
        many=True,
        read_only=True,
    )
    actions = ActionSerializer(
        many=True,
        read_only=True,
    )