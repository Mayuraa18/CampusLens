from django.db import transaction

from documents.models import Document, DocumentPage
from documents.services.pdf_processor import (
    PDFProcessingError,
    extract_pdf_content,
)


def process_document(document: Document) -> None:
    """
    Extract text from a document and store it page by page.
    """

    document.status = Document.Status.PROCESSING
    document.save(update_fields=["status", "updated_at"])

    try:
        pages = extract_pdf_content(document.file.path)

        with transaction.atomic():
            DocumentPage.objects.filter(document=document).delete()

            DocumentPage.objects.bulk_create(
                [
                    DocumentPage(
                        document=document,
                        page_number=page["page_number"],
                        text=page["text"],
                    )
                    for page in pages
                ]
            )

            document.status = Document.Status.PROCESSED
            document.save(update_fields=["status", "updated_at"])

    except PDFProcessingError:
        document.status = Document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise

    except Exception:
        document.status = Document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise