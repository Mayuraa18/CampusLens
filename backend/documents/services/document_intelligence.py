import json

from documents.agent.agent import create_agent
from documents.models import Document, DocumentChunk


def extract_document_intelligence(document: Document) -> dict:
    """
    Extract deadlines, important dates, and required actions
    using a single LLM call.

    The LLM only extracts information from the stored document
    chunks. Python validates the returned structure and page numbers
    before the data is persisted.
    """

    chunks = (
        DocumentChunk.objects
        .filter(page__document=document)
        .select_related("page")
        .order_by(
            "page__page_number",
            "chunk_index",
        )
    )

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
CONTEXT {index}
PAGE: {chunk.page.page_number}

TEXT:
{chunk.text}
"""
        )

    if not context_parts:
        return {
            "deadlines": [],
            "important_dates": [],
            "actions": [],
        }

    document_context = "\n".join(context_parts)

    agent = create_agent()

    prompt = f"""
You are CampusLens, an AI document intelligence extractor.

Analyze the supplied document context and extract three categories:

1. DEADLINES

A deadline is a date by which the document explicitly requires
something to be completed.

2. REQUIRED ACTIONS

An action is something the student is explicitly required to do.

3. IMPORTANT DATES

A date that is relevant to the student but is not itself a
required action or deadline.

DOCUMENT:
{document.title}

DOCUMENT CONTEXT:
{document_context}

STRICT RULES:

1. Extract information ONLY from the supplied document context.

2. Do not invent information.

3. Do not infer an action from an informational statement.

4. Do not turn an announcement date, availability date,
exam date, or other informational date into a student action
unless the document explicitly requires that action.

5. Every extracted item MUST use the page number where the
information appears.

6. A required action should only be included when the document
explicitly requires the student to perform it.

7. A deadline should only be included when the document
explicitly associates the date with a requirement or task.

8. If an item does not exist, return an empty array.

9. Avoid duplicates.

10. Keep descriptions concise and faithful to the document.

11. Return ONLY valid JSON.

Return exactly this structure:

{{
    "deadlines": [
        {{
            "date": "string",
            "description": "string",
            "page": 1
        }}
    ],
    "important_dates": [
        {{
            "date": "string",
            "description": "string",
            "page": 1
        }}
    ],
    "actions": [
        {{
            "action": "string",
            "page": 1
        }}
    ]
}}
"""

    response = agent(prompt)

    raw_response = str(response).strip()

    if not raw_response:
        raise ValueError(
            "LLM returned an empty response for document intelligence."
        )

    # Handle accidental Markdown JSON fences.
    if raw_response.startswith("```"):
        lines = raw_response.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw_response = "\n".join(lines).strip()

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "LLM returned invalid JSON for document intelligence."
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Document intelligence response must be a JSON object."
        )

    deadlines = result.get("deadlines", [])
    important_dates = result.get("important_dates", [])
    actions = result.get("actions", [])

    if not isinstance(deadlines, list):
        raise ValueError("deadlines must be a list.")

    if not isinstance(important_dates, list):
        raise ValueError("important_dates must be a list.")

    if not isinstance(actions, list):
        raise ValueError("actions must be a list.")

    # Validate that every LLM-generated page number actually exists
    # in this document.
    valid_pages = set(
        DocumentChunk.objects
        .filter(page__document=document)
        .values_list(
            "page__page_number",
            flat=True,
        )
    )

    for deadline in deadlines:
        if not isinstance(deadline, dict):
            raise ValueError(
                "Each deadline must be an object."
            )

        if deadline.get("page") not in valid_pages:
            raise ValueError(
                f"Invalid deadline page: {deadline.get('page')}"
            )

        if not deadline.get("date"):
            raise ValueError(
                "Deadline is missing a date."
            )

        if not deadline.get("description"):
            raise ValueError(
                "Deadline is missing a description."
            )

    for important_date in important_dates:
        if not isinstance(important_date, dict):
            raise ValueError(
                "Each important date must be an object."
            )

        if important_date.get("page") not in valid_pages:
            raise ValueError(
                "Invalid important date page: "
                f"{important_date.get('page')}"
            )

        if not important_date.get("date"):
            raise ValueError(
                "Important date is missing a date."
            )

        if not important_date.get("description"):
            raise ValueError(
                "Important date is missing a description."
            )

    for action in actions:
        if not isinstance(action, dict):
            raise ValueError(
                "Each action must be an object."
            )

        if action.get("page") not in valid_pages:
            raise ValueError(
                f"Invalid action page: {action.get('page')}"
            )

        if not action.get("action"):
            raise ValueError(
                "Action is missing its description."
            )

    return {
        "deadlines": deadlines,
        "important_dates": important_dates,
        "actions": actions,
    }