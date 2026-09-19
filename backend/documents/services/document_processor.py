from django.db import transaction

from documents.models import (
    Action,
    Deadline,
    DocumentChunk,
    DocumentPage,
    ImportantDate,
)
from documents.services.action_extractor import extract_actions
from documents.services.chunking import chunk_text
from documents.services.deadline_extractor import extract_deadlines
from documents.services.important_date_extractor import (
    extract_important_dates,
)
from documents.services.pdf_processor import (
    PDFProcessingError,
    extract_pdf_content,
)


def process_document(document):
    """
    Process an uploaded document and store its extracted information.
    """

    document.status = document.Status.PROCESSING
    document.save(update_fields=["status", "updated_at"])

    try:
        pages = extract_pdf_content(document.file.path)

        with transaction.atomic():
            Deadline.objects.filter(document=document).delete()
            ImportantDate.objects.filter(document=document).delete()
            Action.objects.filter(document=document).delete()
            DocumentPage.objects.filter(document=document).delete()

            for page in pages:
                document_page = DocumentPage.objects.create(
                    document=document,
                    page_number=page["page_number"],
                    text=page["text"],
                )

                chunks = chunk_text(page["text"])

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

            deadlines = extract_deadlines(document)

            for deadline in deadlines.get("deadlines", []):
                Deadline.objects.create(
                    document=document,
                    date=deadline["date"],
                    description=deadline["description"],
                    page_number=deadline["page"],
                )

            important_dates = extract_important_dates(
                document=document,
                deadlines=deadlines,
            )

            for important_date in important_dates.get(
                    "important_dates",
                    [],
            ):
                ImportantDate.objects.create(
                    document=document,
                    date=important_date["date"],
                    description=important_date["description"],
                    page_number=important_date["page"],
                )

            actions = extract_actions(document)

            for action in actions.get("actions", []):
                Action.objects.create(
                    document=document,
                    action=action["action"],
                    page_number=action["page"],
                )

            document.status = document.Status.PROCESSED
            document.save(
                update_fields=["status", "updated_at"]
            )

    except PDFProcessingError:
        document.status = document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise

    except Exception:
        document.status = document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise