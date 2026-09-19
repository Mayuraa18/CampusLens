from django.db import transaction

from documents.models import Document, DocumentChunk


def chunk_document(document: Document) -> int:
    """
    Create chunks for every page of a processed document.

    Returns:
        Number of chunks created.
    """

    with transaction.atomic():
        DocumentChunk.objects.filter(
            page__document=document
        ).delete()

        chunks_to_create = []

        for page in document.pages.all():
            from .chunking import chunk_text

            chunks = chunk_text(page.text)

            for chunk_index, text in enumerate(chunks):
                chunks_to_create.append(
                    DocumentChunk(
                        page=page,
                        chunk_index=chunk_index,
                        text=text,
                    )
                )

        DocumentChunk.objects.bulk_create(chunks_to_create)

    return len(chunks_to_create)