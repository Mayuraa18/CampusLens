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

class DocumentPage(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="pages",
    )
    page_number = models.PositiveIntegerField()
    text = models.TextField(blank=True)

    class Meta:
        ordering = ["page_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "page_number"],
                name="unique_document_page",
            )
        ]

    def __str__(self):
        return f"{self.document.title} - Page {self.page_number}"

class DocumentChunk(models.Model):
    page = models.ForeignKey(
        DocumentPage,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    chunk_index = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        ordering = ["page__page_number", "chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["page", "chunk_index"],
                name="unique_page_chunk",
            )
        ]

    def __str__(self):
        return (
            f"{self.page.document.title} - "
            f"Page {self.page.page_number} - "
            f"Chunk {self.chunk_index}"
        )

class Deadline(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="deadlines",
    )
    date = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    page_number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"{self.document.title} - "
            f"Deadline: {self.date}"
        )


class ImportantDate(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="important_dates",
    )
    date = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    page_number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"{self.document.title} - "
            f"Important Date: {self.date}"
        )


class Action(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    action = models.CharField(max_length=500)
    page_number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"{self.document.title} - "
            f"Action: {self.action}"
        )