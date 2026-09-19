from documents.models import Document


def generate_document_insights(document: Document) -> dict:
    """
    Generate a structured overview of a processed document.
    """

    deadlines = list(
        document.deadlines.all().values(
            "id",
            "date",
            "description",
            "page_number",
        )
    )

    important_dates = list(
        document.important_dates.all().values(
            "id",
            "date",
            "description",
            "page_number",
        )
    )

    actions = list(
        document.actions.all().values(
            "id",
            "action",
            "page_number",
        )
    )

    if not deadlines and not important_dates and not actions:
        summary = (
            "No deadlines, important dates, or required actions "
            "were found in this document."
        )
    else:
        summary_parts = []

        if deadlines:
            summary_parts.append(
                f"{len(deadlines)} deadline"
                f"{'s' if len(deadlines) != 1 else ''}"
                " identified."
            )

        if actions:
            summary_parts.append(
                f"{len(actions)} required action"
                f"{'s' if len(actions) != 1 else ''}"
                " identified."
            )

        if important_dates:
            summary_parts.append(
                f"{len(important_dates)} important date"
                f"{'s' if len(important_dates) != 1 else ''}"
                " identified."
            )

        summary = " ".join(summary_parts)

    return {
        "summary": summary,
        "stats": {
            "deadlines": len(deadlines),
            "important_dates": len(important_dates),
            "actions": len(actions),
        },
        "deadlines": deadlines,
        "important_dates": important_dates,
        "actions": actions,
    }