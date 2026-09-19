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
    "do",
}


QUERY_INTENTS = {
    "action": {
        "do",
        "need",
        "required",
        "must",
        "should",
        "have",
        "complete",
        "requirement",
        "requirements",
    },
    "deadline": {
        "deadline",
        "deadlines",
        "due",
        "last",
        "before",
        "by",
        "cutoff",
    },
    "important_date": {
        "date",
        "dates",
        "schedule",
        "available",
        "release",
        "result",
        "admit",
        "exam",
        "examination",
    },
}


INTENT_TERMS = {
    "action": {
        "submit",
        "pay",
        "apply",
        "register",
        "upload",
        "complete",
        "provide",
        "attach",
        "fill",
        "sign",
        "attend",
        "respond",
        "renew",
        "download",
        "collect",
        "required",
        "must",
        "should",
    },
    "deadline": {
        "deadline",
        "due",
        "submit",
        "pay",
        "apply",
        "register",
        "before",
        "by",
        "last",
        "cutoff",
        "close",
        "closes",
    },
    "important_date": {
        "date",
        "schedule",
        "available",
        "release",
        "released",
        "announcement",
        "announced",
        "exam",
        "examination",
        "result",
        "admit",
        "card",
        "orientation",
        "event",
        "starts",
        "ends",
        "opens",
    },
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


def detect_query_intents(query: str) -> set[str]:
    """
    Detect high-level intent from the user's question.
    """

    query_tokens = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower(),
        )
    )

    intents = set()

    for intent, indicators in QUERY_INTENTS.items():
        if query_tokens.intersection(indicators):
            intents.add(intent)

    return intents


def expand_query(query: str) -> list[str]:
    """
    Expand a query with terms related to its detected intent.
    """

    query_tokens = set(tokenize(query))
    expanded_tokens = set(query_tokens)

    intents = detect_query_intents(query)

    for intent in intents:
        expanded_tokens.update(
            INTENT_TERMS[intent]
        )

    return list(expanded_tokens)


def score_chunk(
        query: str,
        query_tokens: list[str],
        chunk_text: str,
) -> float:
    """
    Calculate relevance using both direct lexical matching
    and query-intent matching.
    """

    if not query_tokens:
        return 0.0

    chunk_tokens = set(tokenize(chunk_text))

    original_tokens = set(tokenize(query))
    expanded_tokens = set(query_tokens)

    # Direct query-term matches.
    direct_matches = {
        token
        for token in original_tokens
        if any(
            token in chunk_token
            for chunk_token in chunk_tokens
        )
    }

    # Expanded intent-term matches.
    expanded_matches = {
        token
        for token in expanded_tokens
        if token not in original_tokens
           and any(
            token in chunk_token
            for chunk_token in chunk_tokens
        )
    }

    # Direct matches are stronger evidence than intent matches.
    direct_score = 0.0

    if original_tokens:
        direct_score = (
                len(direct_matches)
                / len(original_tokens)
        )

    # Intent matching gives a meaningful score even when
    # the user's wording differs from the document.
    intent_score = min(
        len(expanded_matches) * 0.15,
        0.60,
        )

    score = min(
        direct_score + intent_score,
        1.0,
        )

    return round(score, 4)


def retrieve_chunks(
        document: Document,
        query: str,
        top_k: int = 5,
        min_score: float = 0.20,
) -> list[dict]:
    """
    Retrieve the most relevant chunks from a document.
    """

    query_tokens = expand_query(query)

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