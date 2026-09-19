import json
import re

from documents.models import Document
from documents.services.retriever import retrieve_chunks
from documents.agent.agent import create_agent


DEADLINE_QUERY = """
deadline due by submit by last date application deadline
payment deadline registration deadline submission deadline
application closes registration closes fee payment deadline
extended deadline cutoff
"""


def extract_deadlines(document: Document) -> dict:
    """
    Extract deadlines from a document using retrieved chunks
    and an LLM.

    Returns:
        {
            "deadlines": [
                {
                    "date": "...",
                    "description": "...",
                    "page": 3
                }
            ]
        }
    """

    chunks = retrieve_chunks(
        document=document,
        query=DEADLINE_QUERY,
        top_k=5,
        min_score=0.0,
    )

    if not chunks:
        return {"deadlines": []}

    # Give the LLM the retrieved text while preserving
    # the trusted page number from our database.
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
Extract ONLY actual deadlines that require a person to complete
an action by a specific date.

A deadline should normally involve an action such as:
- submit
- apply
- register
- pay
- upload
- complete
- attend
- respond
- renew
- download
- report

A date is NOT automatically a deadline.

Do NOT classify these as deadlines unless the text explicitly
says they are a deadline or cutoff:

- event dates or event durations
- hackathon dates
- course schedules
- learning schedules
- publication dates
- document dates
- meeting dates
- general calendar dates
- dates describing when something happened
- dates describing when something starts or ends if no required
student action is associated with the date

Examples:

"Submit the examination form by 20 October 2026."
→ DEADLINE

"The examination fee must be paid before 22 October 2026."
→ DEADLINE

"Applications close on 25 October 2026."
→ DEADLINE

"AWS First Commit runs from September 17–20, 2026."
→ NOT A DEADLINE

"The MVP learning material is needed by Sept 17."
→ Only classify as a deadline if the text explicitly establishes
that a person must complete an action by that date.

Rules:
1. Only extract information explicitly supported by the text.
2. Never invent a date.
3. Never convert a relative date into a calendar date unless the
document provides enough information.
4. For each deadline provide:
- date
- description
- chunk number
5. Do not provide page numbers. Python will attach the trusted
page number from the retrieved chunk.
6. If there are no actual deadlines, return an empty list.
7. Return ONLY valid JSON.

Required format:

{{
    "deadlines": [
        {{
            "date": "20 October 2026",
            "description": "Submit examination form",
            "chunk": 1
        }}
    ]
}}

DOCUMENT CHUNKS:

{context}
"""

    response = agent(prompt)

    raw_response = str(response)

    # Try to extract JSON from the model response.
    json_match = re.search(
        r"\{.*\}",
        raw_response,
        re.DOTALL,
    )

    if not json_match:
        return {"deadlines": []}

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return {"deadlines": []}

    extracted_deadlines = data.get("deadlines", [])

    if not isinstance(extracted_deadlines, list):
        return {"deadlines": []}

    final_deadlines = []

    for deadline in extracted_deadlines:
        if not isinstance(deadline, dict):
            continue

        date = deadline.get("date")
        description = deadline.get("description")
        chunk_number = deadline.get("chunk")

        if not date or not description:
            continue

        if not isinstance(chunk_number, int):
            continue

        if chunk_number < 1 or chunk_number > len(chunks):
            continue

        # IMPORTANT:
        # Never trust the LLM for the page number.
        # Use the page number attached to the retrieved chunk.
        page_number = chunks[chunk_number - 1]["page_number"]

        final_deadlines.append(
            {
                "date": str(date).strip(),
                "description": str(description).strip(),
                "page": page_number,
            }
        )

    return {
        "deadlines": final_deadlines,
    }