from django.db import transaction

from documents.models import (
    Action,
    Deadline,
    DocumentChunk,
    DocumentPage,
    ImportantDate,
)
from documents.services.chunking import chunk_text
from documents.services.document_intelligence import (
    extract_document_intelligence,
)
from documents.services.pdf_processor import (
    PDFProcessingError,
    extract_pdf_content,
)


def process_document(document):
    """
    Process an uploaded document.

    Processing is split into short database transactions so that
    long-running LLM operations do not hold SQLite write locks.

    Pipeline:

    1. Mark document as PROCESSING.
    2. Extract PDF pages.
    3. Save pages and chunks in a short transaction.
    4. Run ONE LLM call to extract:
       - deadlines
       - important dates
       - required actions
    5. Save extracted intelligence in a second short transaction.
    6. Mark document as PROCESSED.

    If processing fails, the document is marked as FAILED.
    """

    # ---------------------------------------------------------
    # 1. Mark document as processing
    # ---------------------------------------------------------

    document.status = document.Status.PROCESSING
    document.save(
        update_fields=["status", "updated_at"],
    )

    try:
        # -----------------------------------------------------
        # 2. Extract PDF content
        # -----------------------------------------------------

        pages = extract_pdf_content(
            document.file.path,
        )

        # -----------------------------------------------------
        # 3. Save pages and chunks
        #
        # Keep this transaction short.
        # No LLM calls happen inside this transaction.
        # -----------------------------------------------------

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

                chunks = chunk_text(
                    page["text"],
                )

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

        # -----------------------------------------------------
        # 4. ONE LLM CALL
        #
        # This replaces:
        #
        # extract_deadlines()
        # extract_important_dates()
        # extract_actions()
        #
        # with one unified extraction call.
        # -----------------------------------------------------

        intelligence = extract_document_intelligence(
            document,
        )

        deadlines = intelligence["deadlines"]
        important_dates = intelligence["important_dates"]
        actions = intelligence["actions"]

        # -----------------------------------------------------
        # 5. Save extracted intelligence
        #
        # Keep this transaction short as well.
        # -----------------------------------------------------

        with transaction.atomic():
            Deadline.objects.filter(
                document=document,
            ).delete()

            ImportantDate.objects.filter(
                document=document,
            ).delete()

            Action.objects.filter(
                document=document,
            ).delete()

            Deadline.objects.bulk_create(
                [
                    Deadline(
                        document=document,
                        date=deadline["date"],
                        description=deadline["description"],
                        page_number=deadline["page"],
                    )
                    for deadline in deadlines
                ]
            )

            ImportantDate.objects.bulk_create(
                [
                    ImportantDate(
                        document=document,
                        date=important_date["date"],
                        description=important_date["description"],
                        page_number=important_date["page"],
                    )
                    for important_date in important_dates
                ]
            )

            Action.objects.bulk_create(
                [
                    Action(
                        document=document,
                        action=action["action"],
                        page_number=action["page"],
                    )
                    for action in actions
                ]
            )

            # -------------------------------------------------
            # 6. Mark document as processed
            # -------------------------------------------------

            document.status = document.Status.PROCESSED
            document.save(
                update_fields=[
                    "status",
                    "updated_at",
                ],
            )

    except PDFProcessingError:
        document.status = document.Status.FAILED
        document.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )
        raise

    except Exception:
        document.status = document.Status.FAILED
        document.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )
        raise