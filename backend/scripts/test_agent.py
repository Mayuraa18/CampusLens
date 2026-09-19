import os

import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()

from documents.agent.agent import create_agent


agent = create_agent()

document_id = 5

question = input("Ask CampusLens: ")

response = agent(
    f"""
The document ID is {document_id}.

Student question:
{question}
"""
)

print("\n--- CampusLens ---")
print(response)