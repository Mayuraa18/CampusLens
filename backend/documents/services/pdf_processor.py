from pypdf import PdfReader


class PDFProcessingError(Exception):
    """Raised when a PDF cannot be processed."""


def extract_pdf_content(file_path):
    """
    Extract text from a PDF while preserving page numbers.

    Returns:
        list[dict]: One dictionary per page.
    """

    try:
        reader = PdfReader(file_path)
    except Exception as exc:
        raise PDFProcessingError(
            f"Unable to read PDF: {exc}"
        ) from exc

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            raise PDFProcessingError(
                f"Unable to extract page {page_number}: {exc}"
            ) from exc

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip(),
            }
        )

    return pages