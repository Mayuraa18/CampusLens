import re

from documents.models import Document, DocumentChunk


STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "what",
    "when",
    "where",
    "who",
    "how",
    "why",
    "which",
    "this",
    "that",
    "for",
    "from",
    "with",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "my",
    "me",
}


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized search tokens.
    """

    tokens = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return [
        token
        for token in tokens
        if token not in STOP_WORDS and len(token) > 2
    ]


def score_chunk(
        query: str,
        query_tokens: list[str],
        chunk_text: str,
) -> float:
    """
    Calculate relevance based on query-term coverage.
    """

    if not query_tokens:
        return 0.0

    chunk_tokens = set(tokenize(chunk_text))
    query_tokens_set = set(query_tokens)

    matched_terms = {
        query_token
        for query_token in query_tokens_set
        if any(
            query_token in chunk_token
            for chunk_token in chunk_tokens
        )
    }

    if not matched_terms:
        return 0.0

    return round(
        len(matched_terms) / len(query_tokens_set),
        4,
        )


def retrieve_chunks(
        document: Document,
        query: str,
        top_k: int = 5,
        min_score: float = 0.20,
) -> list[dict]:
    """
    Retrieve the most relevant chunks from a document.
    """

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    chunks = (
        DocumentChunk.objects
        .filter(page__document=document)
        .select_related("page")
    )

    results = []

    for chunk in chunks:
        score = score_chunk(
            query=query,
            query_tokens=query_tokens,
            chunk_text=chunk.text,
        )

        if score < min_score:
            continue

        results.append(
            {
                "chunk_id": chunk.id,
                "page_number": chunk.page.page_number,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
                "score": round(score, 4),
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results[:top_k]