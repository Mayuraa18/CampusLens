from django.db import transaction

from documents.models import Document, DocumentPage
from documents.services.chunking import chunk_text
from documents.services.pdf_processor import (
    PDFProcessingError,
    extract_pdf_content,
)


def process_document(document: Document) -> None:
    """
    Extract text from a PDF, store it page by page,
    and create chunks for each page.
    """

    document.status = Document.Status.PROCESSING
    document.save(update_fields=["status", "updated_at"])

    try:
        pages = extract_pdf_content(document.file.path)

        with transaction.atomic():
            DocumentPage.objects.filter(
                document=document
            ).delete()

            for page in pages:
                document_page = DocumentPage.objects.create(
                    document=document,
                    page_number=page["page_number"],
                    text=page["text"],
                )

                chunks = chunk_text(page["text"])

                # Import here to keep model dependencies simple.
                from documents.models import DocumentChunk

                DocumentChunk.objects.bulk_create(
                    [
                        DocumentChunk(
                            page=document_page,
                            chunk_index=chunk_index,
                            text=chunk,
                        )
                        for chunk_index, chunk in enumerate(chunks)
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