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

    Database write transactions are intentionally kept short so that
    long-running LLM/Ollama operations do not hold SQLite write locks.
    """

    # 1. Mark document as PROCESSING.
    document.status = document.Status.PROCESSING
    document.save(update_fields=["status", "updated_at"])

    try:
        # 2. Extract PDF content outside any database transaction.
        pages = extract_pdf_content(document.file.path)

        # 3. Save pages and chunks inside a SHORT transaction.
        # 4. This transaction is committed BEFORE any LLM/Ollama call.
        with transaction.atomic():
            DocumentPage.objects.filter(
                document=document,
            ).delete()

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

        # 5. Perform all LLM/Ollama processing AFTER the first
        #    database transaction has completely finished.

        deadlines = extract_deadlines(document)

        important_dates = extract_important_dates(
            document=document,
            deadlines=deadlines,
        )

        actions = extract_actions(document)

        # 6. Save AI-extracted results inside another SHORT transaction.
        with transaction.atomic():
            # Remove previous extracted intelligence so re-processing
            # does not create duplicates.
            Deadline.objects.filter(
                document=document,
            ).delete()

            ImportantDate.objects.filter(
                document=document,
            ).delete()

            Action.objects.filter(
                document=document,
            ).delete()

            # Save deadlines.
            Deadline.objects.bulk_create(
                [
                    Deadline(
                        document=document,
                        date=deadline["date"],
                        description=deadline["description"],
                        page_number=deadline["page"],
                    )
                    for deadline in deadlines.get("deadlines", [])
                ]
            )

            # Save important dates.
            ImportantDate.objects.bulk_create(
                [
                    ImportantDate(
                        document=document,
                        date=important_date["date"],
                        description=important_date["description"],
                        page_number=important_date["page"],
                    )
                    for important_date in important_dates.get(
                    "important_dates",
                    []
                )
                ]
            )

            # Save actions.
            Action.objects.bulk_create(
                [
                    Action(
                        document=document,
                        action=action["action"],
                        page_number=action["page"],
                    )
                    for action in actions.get("actions", [])
                ]
            )

            # Mark as processed only after everything has been saved.
            document.status = document.Status.PROCESSED
            document.save(
                update_fields=["status", "updated_at"],
            )

    except PDFProcessingError:
        # 8. Mark failed and re-raise the original exception.
        document.status = document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise

    except Exception:
        # 9. Mark failed and re-raise the original exception.
        document.status = document.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        raise