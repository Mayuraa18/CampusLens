import re


DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150


def normalize_text(text: str) -> str:
    """
    Normalize extracted PDF text before chunking.
    """
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(
        text: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Split text into overlapping chunks while preserving word boundaries.

    Args:
        text: Text to split.
        chunk_size: Maximum approximate size of each chunk.
        chunk_overlap: Approximate number of characters shared
            between consecutive chunks.

    Returns:
        A list of text chunks.
    """

    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text = normalize_text(text)
    words = text.split()

    chunks = []
    current_words = []
    current_length = 0

    for word in words:
        word_length = len(word)

        if current_words:
            word_length += 1  # Space before the word

        if (
                current_words
                and current_length + word_length > chunk_size
        ):
            chunks.append(" ".join(current_words))

            # Keep the last ~chunk_overlap characters as overlap.
            overlap_words = []
            overlap_length = 0

            for previous_word in reversed(current_words):
                added_length = len(previous_word)

                if overlap_words:
                    added_length += 1

                if overlap_length + added_length > chunk_overlap:
                    break

                overlap_words.insert(0, previous_word)
                overlap_length += added_length

            current_words = overlap_words
            current_length = overlap_length

        if current_words:
            current_length += 1

        current_words.append(word)
        current_length += len(word)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks