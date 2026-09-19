from strands import tool

from documents.models import Document
from documents.services.retriever import retrieve_chunks


@tool
def search_document(
        document_id: int,
        query: str,
) -> dict:
    """
    Search a CampusLens document for information relevant to a question.

    Args:
        document_id: ID of the document to search.
        query: Student's question.

    Returns:
        Relevant document chunks with page numbers.
    """

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        return {
            "error": "Document not found."
        }

    results = retrieve_chunks(
        document=document,
        query=query,
        top_k=5,
    )

    if not results:
        return {
            "results": [],
            "message": (
                "No relevant information was found "
                "in the document."
            ),
        }

    return {
        "results": results,
    }