import json
import re

from documents.agent.agent import create_agent
from documents.models import Document
from documents.services.retriever import retrieve_chunks


ACTION_QUERY = """
must submit required submit upload pay register apply complete
provide attach fill sign attend respond renew download collect
students must student should required action instructions
"""


def extract_actions(document: Document) -> dict:
    """
    Extract required student actions from a document.

    Returns:
        {
            "actions": [
                {
                    "action": "...",
                    "page": 1
                }
            ]
        }
    """

    chunks = retrieve_chunks(
        document=document,
        query=ACTION_QUERY,
        top_k=5,
        min_score=0.0,
    )

    if not chunks:
        return {"actions": []}

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
Identify the actions that a student is required or instructed
to perform according to the document.

An action means something the student/person must actually do.

Examples:

"Students must submit the examination form."
→ ACTION

"Students must pay the examination fee."
→ ACTION

"Applicants should upload a passport-size photograph."
→ ACTION

"Students are required to register before the deadline."
→ ACTION

Do NOT extract:

- Dates without an associated action
- Event dates
- Examination dates
- Dates when something becomes available
- General information
- Descriptions of what the system does
- Actions performed by administrators, organizers, or staff
  unless the document explicitly requires the student to do them
- Hypothetical or optional actions unless the document clearly
  instructs students to perform them

Important distinction:

"Submit the examination form by 20 October 2026."
→ ACTION: Submit the examination form

"Students must pay the examination fee before 22 October 2026."
→ ACTION: Pay the examination fee

"The admit card will be available from 25 October 2026."
→ NOT AN ACTION

Rules:

1. Only use information explicitly supported by the document.
2. Never invent an action.
3. Keep the action concise and actionable.
4. Do not include the deadline date inside the action unless
   necessary to understand the action.
5. For each action provide:
   - action
   - chunk number
6. Do not provide page numbers.
7. Python will attach the trusted page number.
8. If the same action appears multiple times, return it only once.
9. Return ONLY valid JSON.
10. If there are no required student actions, return an empty list.

Required format:

{{
    "actions": [
        {{
            "action": "Submit the examination form",
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
        return {"actions": []}

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return {"actions": []}

    extracted_actions = data.get("actions", [])

    if not isinstance(extracted_actions, list):
        return {"actions": []}

    final_actions = []
    seen_actions = set()

    for action_data in extracted_actions:
        if not isinstance(action_data, dict):
            continue

        action = action_data.get("action")
        chunk_number = action_data.get("chunk")

        if not action:
            continue

        if not isinstance(chunk_number, int):
            continue

        if chunk_number < 1 or chunk_number > len(chunks):
            continue

        normalized_action = " ".join(
            str(action).strip().lower().split()
        )

        if normalized_action in seen_actions:
            continue

        seen_actions.add(normalized_action)

        page_number = chunks[chunk_number - 1]["page_number"]

        final_actions.append(
            {
                "action": str(action).strip(),
                "page": page_number,
            }
        )

    return {
        "actions": final_actions,
    }