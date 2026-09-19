import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.services.pdf_processor import PDFProcessingError

from documents.models import (
    Action,
    Deadline,
    Document,
    DocumentChunk,
    DocumentPage,
    ImportantDate,
)
from documents.services.document_processor import process_document


@pytest.mark.django_db
def test_process_document_persists_extracted_data(monkeypatch):
    user = User.objects.create_user(
        username="student",
        password="TestPassword123!",
    )

    document = Document.objects.create(
        user=user,
        title="Examination Notice",
        file=SimpleUploadedFile(
            "exam_notice.pdf",
            b"fake pdf content",
            content_type="application/pdf",
        ),
    )

    def mock_extract_pdf_content(file_path):
        return [
            {
                "page_number": 1,
                "text": (
                    "The examination form must be submitted "
                    "by 20 October 2026. "
                    "Students must pay the examination fee "
                    "before 22 October 2026. "
                    "The admit card will be available "
                    "from 25 October 2026."
                ),
            }
        ]

    def mock_chunk_text(text):
        return [text]

    def mock_extract_deadlines(document):
        return {
            "deadlines": [
                {
                    "date": "20 October 2026",
                    "description": "Submit examination form",
                    "page": 1,
                },
                {
                    "date": "22 October 2026",
                    "description": "Pay examination fee",
                    "page": 1,
                },
            ]
        }

    def mock_extract_important_dates(document, deadlines):
        return {
            "important_dates": [
                {
                    "date": "25 October 2026",
                    "description": "Admit card available",
                    "page": 1,
                }
            ]
        }

    def mock_extract_actions(document):
        return {
            "actions": [
                {
                    "action": "Submit examination form",
                    "page": 1,
                },
                {
                    "action": "Pay examination fee",
                    "page": 1,
                },
            ]
        }

    monkeypatch.setattr(
        "documents.services.document_processor.extract_pdf_content",
        mock_extract_pdf_content,
    )

    monkeypatch.setattr(
        "documents.services.document_processor.chunk_text",
        mock_chunk_text,
    )

    monkeypatch.setattr(
        "documents.services.document_processor.extract_deadlines",
        mock_extract_deadlines,
    )

    monkeypatch.setattr(
        "documents.services.document_processor.extract_important_dates",
        mock_extract_important_dates,
    )

    monkeypatch.setattr(
        "documents.services.document_processor.extract_actions",
        mock_extract_actions,
    )

    process_document(document)

    document.refresh_from_db()

    assert document.status == Document.Status.PROCESSED

    assert DocumentPage.objects.filter(
        document=document
    ).count() == 1

    assert DocumentChunk.objects.filter(
        page__document=document
    ).count() == 1

    assert Deadline.objects.filter(
        document=document
    ).count() == 2

    assert ImportantDate.objects.filter(
        document=document
    ).count() == 1

    assert Action.objects.filter(
        document=document
    ).count() == 2

    deadline_dates = set(
        Deadline.objects.filter(
            document=document
        ).values_list("date", flat=True)
    )

    assert deadline_dates == {
        "20 October 2026",
        "22 October 2026",
    }

    actions = set(
        Action.objects.filter(
            document=document
        ).values_list("action", flat=True)
    )

    assert actions == {
        "Submit examination form",
        "Pay examination fee",
    }

@pytest.mark.django_db
def test_process_document_marks_failed_on_pdf_error(
        monkeypatch,
):
    user = User.objects.create_user(
        username="student",
        password="TestPassword123!",
    )

    document = Document.objects.create(
        user=user,
        title="Broken Document",
        file=SimpleUploadedFile(
            "broken.pdf",
            b"invalid pdf",
            content_type="application/pdf",
        ),
    )

    def mock_extract_pdf_content(file_path):
        raise PDFProcessingError(
            "Unable to process PDF"
        )

    monkeypatch.setattr(
        "documents.services.document_processor.extract_pdf_content",
        mock_extract_pdf_content,
    )

    with pytest.raises(PDFProcessingError):
        process_document(document)

    document.refresh_from_db()

    assert document.status == Document.Status.FAILED