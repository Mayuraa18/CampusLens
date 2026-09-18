from pathlib import Path

from pypdf import PdfReader
from rest_framework import serializers

from .models import Document


MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB


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

    def validate_file(self, file):
        if file.size > MAX_DOCUMENT_SIZE:
            raise serializers.ValidationError(
                "File size must not exceed 10 MB."
            )

        extension = Path(file.name).suffix.lower()

        if extension != ".pdf":
            raise serializers.ValidationError(
                "Only PDF files are supported."
            )

        try:
            PdfReader(file)
        except Exception as exc:
            raise serializers.ValidationError(
                "The uploaded file is not a valid or readable PDF."
            ) from exc

        file.seek(0)

        return file