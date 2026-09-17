from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        PROCESSED = "processed", "Processed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(
        max_length=255,
    )

    file = models.FileField(
        upload_to="documents/",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title