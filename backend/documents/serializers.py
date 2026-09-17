from rest_framework import serializers

from .models import Document


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