import json
import re

from documents.agent.agent import create_agent
from documents.models import Document
from documents.services.deadline_extractor import extract_deadlines
from documents.services.retriever import retrieve_chunks


IMPORTANT_DATE_QUERY = """
date dates schedule scheduled available release announcement
exam examination admit card result result announcement
orientation event starts ends opens closes begins
important date timeline
"""


def extract_important_dates(
        document: Document,
        deadlines: dict | None = None,
) -> dict:
    """
    Extract important dates from a document.

    Deadlines are extracted separately and are excluded from the
    important-date results.
    """

    chunks = retrieve_chunks(
        document=document,
        query=IMPORTANT_DATE_QUERY,
        top_k=5,
        min_score=0.0,
    )

    if not chunks:
        return {"important_dates": []}

    # Reuse already extracted deadlines when available.
    # This avoids making another LLM call.
    if deadlines is None:
        deadlines = extract_deadlines(document)

    deadline_dates = {
        deadline["date"].strip().lower()
        for deadline in deadlines.get("deadlines", [])
    }

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
CHUNK {index}
PAGE: {chunk["page_number"]}

TEXT:
{chunk["text"]}
"""
        )

    context = "\n".join(context_parts)

    agent = create_agent()

    prompt = f"""
Identify important dates from the document chunks below.

An important date is a date that is relevant to the student's
workflow but is NOT a deadline.

Examples of important dates:

- Admit card becomes available
- Examination result is announced
- Orientation date
- Scholarship results announcement
- Course registration opens
- An important event starts
- An important event ends

Do NOT extract:

- Deadlines requiring an action by a specific date
- Dates that are already deadlines
- Document publication dates unless they are relevant to the
  student's workflow
- Historical dates
- Dates that have no meaningful relevance to the student

Important distinction:

"Submit the examination form by 20 October 2026."
→ DEADLINE, not important date.

"The admit card will be available from 25 October 2026."
→ IMPORTANT DATE.

"Examinations will be conducted from 1 November to 5 November."
→ IMPORTANT DATE, if relevant to the student's workflow.

Rules:

1. Only use information explicitly present in the chunks.
2. Never invent dates.
3. Do not convert relative dates into calendar dates.
4. Do not return deadlines.
5. Do not return a date merely because it appears in the document.
6. For each important date provide:
   - date
   - description
   - chunk number
7. Do not provide page numbers.
8. Python will attach the trusted page number.
9. If the same important date appears multiple times,
   return it only once.
10. Return ONLY valid JSON.
11. If there are no important dates, return an empty list.

These dates have already been classified as deadlines.
Do NOT return them again:

{sorted(deadline_dates)}

Required format:

{{
    "important_dates": [
        {{
            "date": "25 October 2026",
            "description": "Admit card becomes available",
            "chunk": 1
        }}
    ]
}}

DOCUMENT CHUNKS:

{context}
"""

    response = agent(prompt)

    raw_response = str(response)

    json_match = re.search(
        r"\{.*\}",
        raw_response,
        re.DOTALL,
    )

    if not json_match:
        return {"important_dates": []}

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return {"important_dates": []}

    extracted_dates = data.get("important_dates", [])

    if not isinstance(extracted_dates, list):
        return {"important_dates": []}

    final_dates = []
    seen_dates = set()

    for important_date in extracted_dates:
        if not isinstance(important_date, dict):
            continue

        date = important_date.get("date")
        description = important_date.get("description")
        chunk_number = important_date.get("chunk")

        if not date or not description:
            continue

        if not isinstance(chunk_number, int):
            continue

        if chunk_number < 1 or chunk_number > len(chunks):
            continue

        normalized_date = str(date).strip().lower()

        # Extra Python-side deduplication against deadlines.
        if normalized_date in deadline_dates:
            continue

        # Prevent duplicate important dates.
        if normalized_date in seen_dates:
            continue

        seen_dates.add(normalized_date)

        page_number = chunks[chunk_number - 1]["page_number"]

        final_dates.append(
            {
                "date": str(date).strip(),
                "description": str(description).strip(),
                "page": page_number,
            }
        )

    return {
        "important_dates": final_dates,
    }