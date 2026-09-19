# CampusLens Architecture

## 1. Purpose

CampusLens is a document-to-action system for students.

The system takes college documents and turns them into:

```text
Summary
Deadlines
Required Actions
Important Information
Questions & Answers
Source / Page References
```

The architecture is intentionally simple for the hackathon, while leaving room for AWS deployment and future expansion.

---

# 2. High-Level Architecture

```text
┌───────────────────────────────┐
│           Student             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        React Frontend         │
│             Vite              │
└───────────────┬───────────────┘
                │ HTTP / JSON
                ▼
┌───────────────────────────────┐
│       Django REST API         │
│                               │
│  Authentication               │
│  Documents                    │
│  Conversations                │
│  AI Chat API                  │
└───────┬───────────────┬───────┘
        │               │
        │               ▼
        │      ┌──────────────────┐
        │      │  Strands Agent   │
        │      └────────┬─────────┘
        │               │
        │       ┌───────┴────────┐
        │       ▼                ▼
        │ ┌───────────┐   ┌─────────────┐
        │ │  Bedrock  │   │ Retrieval / │
        │ │   Model   │   │ Doc Tools   │
        │ └───────────┘   └──────┬──────┘
        │                        │
        ▼                        ▼
┌──────────────┐          ┌──────────────┐
│   Database   │          │ Local / S3   │
│    SQLite    │          │  Documents   │
└──────────────┘          └──────────────┘
```

During local development, the agent can use Ollama. The AWS target replaces the local model with Amazon Bedrock.

---

# 3. Current Backend Architecture

The Django backend currently contains:

```text
backend/
├── accounts/
├── config/
├── documents/
├── conversations/
├── scripts/
├── tests/
├── pytest.ini
└── manage.py
```

## `config`

Project configuration:

- Django settings
- Root URLs
- WSGI/ASGI configuration
- Environment configuration
- REST framework configuration

## `accounts`

Authentication functionality.

Current state:

```text
Registration              ✓
JWT login                 ✓
JWT refresh               ✓
Current user /me          ✓
Django built-in User      ✓
```

## `documents`

Responsible for:

- Document ownership
- PDF upload and validation
- Document processing
- Page extraction
- Text chunking
- Deadline extraction
- Important-date extraction
- Required-action extraction
- Document insights
- Document APIs

## `conversations`

Responsible for:

- Chat creation
- Chat ownership
- Message history
- AI question answering
- Source references
- Chat APIs

---

# 4. Data Model

Current relationship:

```text
User
 │
 ├───────────────< Document
 │                       │
 │                       ├────────< DocumentPage
 │                       │              │
 │                       │              └────────< DocumentChunk
 │                       │
 │                       ├────────< Deadline
 │                       │
 │                       ├────────< ImportantDate
 │                       │
 │                       ├────────< Action
 │                       │
 │                       └────────< Chat
 │                                      │
 │                                      └────────< Message
 │
 └───────────────< Chat
```

More explicitly:

```text
User 1 ──── N Document

User 1 ──── N Chat

Document 1 ──── N DocumentPage

DocumentPage 1 ──── N DocumentChunk

Document 1 ──── N Deadline

Document 1 ──── N ImportantDate

Document 1 ──── N Action

Document 1 ──── N Chat

Chat 1 ──── N Message
```

A `Document` belongs to a user. A `Chat` belongs to both a user and a document.

---

# 5. Document Lifecycle

The document model supports:

```text
uploaded
processing
processed
failed
```

Lifecycle:

```text
                 ┌──────────────┐
                 │    Upload    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   uploaded   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  processing  │
                 └──────┬───────┘
                        │
                 ┌──────┴───────┐
                 ▼              ▼
          ┌────────────┐  ┌──────────┐
          │ processed  │  │  failed  │
          └────────────┘  └──────────┘
```

---

# 6. Document Processing Pipeline

The current processing pipeline is:

```text
PDF Upload
    │
    ▼
PDF Validation
    │
    ▼
PDF Text Extraction
    │
    ▼
Document Pages
    │
    ▼
Text Chunking
    │
    ├──────────────────────┐
    ▼                      ▼
Deadline Extraction   Important-Date Extraction
    │                      │
    └──────────┬───────────┘
               ▼
       Required Action Extraction
               │
               ▼
       Persist Structured Data
               │
               ▼
          Processed Document
```

The processing service stores:

```text
DocumentPage
DocumentChunk
Deadline
ImportantDate
Action
```

If PDF processing fails, the document is marked as `failed`.

---

# 7. Retrieval and RAG

The current retrieval implementation is intentionally lightweight.

```text
User Question
      │
      ▼
Query Tokenization
      │
      ▼
Intent Detection
      │
      ▼
Keyword / Intent Expansion
      │
      ▼
Chunk Scoring
      │
      ▼
Top Relevant Chunks
      │
      ▼
Chat Service
      │
      ▼
Strands Agent
```

The current retriever uses the stored `DocumentChunk` records and a lightweight lexical/intent-based scoring approach.

There is currently no vector database.

This is intentional for the MVP.

A future retrieval architecture can evolve toward:

```text
S3
 ↓
Bedrock Knowledge Bases / other retrieval layer
 ↓
Relevant document content
 ↓
Strands Agent
```

A vector database should only be introduced if the application requires it.

---

# 8. AI Architecture

The current AI layer uses **Strands Agents SDK**.

The first implementation uses **one agent**, rather than a multi-agent system.

Current flow:

```text
Student Question
       │
       ▼
Django Chat Service
       │
       ├── Conversation History
       │
       ├── Retrieved Document Context
       │
       └── Structured Insights
               │
               ▼
        Strands Agent
               │
               ▼
        Local Model / Ollama
```

AWS target:

```text
Student Question
       │
       ▼
Django Chat Service
       │
       ├── Conversation History
       ├── Retrieved Document Context
       └── Structured Insights
               │
               ▼
        Strands Agent
               │
               ▼
        Amazon Bedrock
```

---

# 9. Agent Responsibilities

The CampusLens agent is responsible for:

- Answering questions about uploaded documents
- Using retrieved document context
- Using structured document insights
- Understanding conversational follow-up questions
- Providing page references
- Avoiding unsupported claims

The agent should not invent information that is absent from the document.

When the document does not contain the requested information, the application should communicate that clearly.

---

# 10. Retrieval / Agent Tools

The current architecture is centered around document retrieval.

Primary tool:

```text
search_document()
```

The system also has dedicated extraction services for:

```text
extract_deadlines()
extract_important_dates()
extract_actions()
```

These extraction services are used during document processing to create structured insights.

Potential future agent tools include:

```text
search_document()
extract_deadlines()
extract_actions()
explain_section()
```

The architecture should remain single-agent until a multi-agent design provides a clear benefit.

---

# 11. Conversation Architecture

Chat requests follow this flow:

```text
POST /chats/<chat_id>/messages/
                │
                ▼
         Validate Message
                │
                ▼
       Save User Message
                │
                ▼
       Build Conversation History
                │
                ▼
       Retrieve Document Context
                │
                ▼
       Load Structured Insights
                │
                ▼
          Strands Agent
                │
                ▼
         Generate Answer
                │
                ▼
       Save Assistant Message
                │
                ▼
       Return Answer + Sources
```

The API returns:

```text
user_message
assistant_message
sources
```

---

# 12. Source Attribution

Source references are a core CampusLens feature.

The system preserves page numbers during PDF extraction and stores them with structured insights and retrieved chunks.

Target response:

```text
The examination registration deadline is 20 October.

[Source: Page 2]
```

For extracted actions:

```text
Action:
Upload a passport-size photograph.

[Source: Page 3]
```

Source information should remain tied to the actual document content rather than being generated independently by the model.

---

# 13. API Architecture

The frontend communicates with Django through REST APIs.

Current API groups:

```text
/auth/
/documents/
/documents/<id>/insights/
/documents/<id>/chats/
/chats/
/chats/<id>/messages/
```

Authentication uses JWT.

The complete endpoint contract is documented in:

```text
docs/API.md
```

---

# 14. Security Architecture

## Authentication

Protected APIs use JWT authentication.

## Authorization

Resources are scoped to the authenticated user.

Examples:

```python
Document.objects.get(
    pk=document_id,
    user=request.user,
)
```

and:

```python
Chat.objects.get(
    pk=chat_id,
    user=request.user,
)
```

Users cannot access another user's:

- Documents
- Chats
- Messages

Unauthorized resource access returns `404 Not Found`.

## File Validation

Document uploads validate:

- File type
- PDF readability
- Maximum file size

Current maximum upload size:

```text
10 MB
```

## Secrets

Secrets must never be committed to Git.

Examples:

```text
.env
AWS credentials
API keys
JWT tokens
```

---

# 15. Testing Architecture

CampusLens now has an automated pytest suite.

Current coverage:

```text
Authentication       3 tests
Documents            3 tests
Chats                6 tests
Security             7 tests
Chat service         2 tests
Document processing  2 tests
──────────────────────────────
Total               23 tests
```

The suite verifies:

- Authentication
- Protected endpoints
- Document ownership
- Chat ownership
- Message validation
- AI success handling
- AI failure handling
- Document processing
- PDF processing failure handling

AI-dependent tests mock the AI service, so the automated suite does not require Ollama to be running.

---

# 16. Development Architecture

## Local Development

```text
React / Vite
     │
     ▼
Django REST API
     │
     ├── SQLite
     │
     ├── Local media storage
     │
     ├── Strands Agents
     │
     └── Ollama
```

This environment is used for rapid development and testing.

---

# 17. AWS Architecture

The planned AWS deployment separates application logic from cloud infrastructure.

Target:

```text
                         ┌──────────────┐
                         │   React      │
                         │   Frontend   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ Django API   │
                         │ Container    │
                         └───┬──────┬───┘
                             │      │
                 ┌───────────┘      └──────────────┐
                 ▼                                  ▼
          ┌──────────────┐                   ┌──────────────┐
          │      S3      │                   │   Strands    │
          │  Documents   │                   │    Agent     │
          └──────────────┘                   └──────┬───────┘
                                                    │
                                                    ▼
                                             ┌──────────────┐
                                             │   Bedrock    │
                                             │    Model     │
                                             └──────────────┘

                    Supporting infrastructure:
                    IAM + CloudWatch
```

Potential deployment components:

```text
Frontend:
Amplify Hosting or equivalent

Backend:
Containerized Django deployment
ECS / Fargate or ECS Express Mode

Storage:
Amazon S3

AI:
Amazon Bedrock + Strands Agents SDK

Observability:
CloudWatch

Access control:
IAM
```

Only services that solve an actual application requirement should be introduced.

---

# 18. Development vs Production

## Development

```text
Django
SQLite
Local media storage
Ollama
Local environment variables
Django development server
```

## Production Target

```text
Django API container
Production database
Amazon S3
Amazon Bedrock
IAM
CloudWatch
Production deployment
```

The exact production database and deployment configuration will be finalized during AWS integration.

---

# 19. Team Integration

The architecture supports separate team responsibilities:

```text
Backend / AI
    │
    ├── Django
    ├── RAG
    ├── Strands
    └── Bedrock integration

Frontend
    │
    └── React / Vite

Cloud / DevOps
    │
    ├── Containerization
    ├── S3
    ├── IAM
    ├── ECS
    └── CloudWatch

Testing / QA
    │
    ├── pytest
    ├── API testing
    └── Security testing
```

The API contract in `docs/API.md` provides the interface between the frontend and backend teams.

---

# 20. Design Principles

CampusLens follows:

```text
Simple
   ↓
Working
   ↓
Tested
   ↓
Integrated
   ↓
Deployed
   ↓
Improved
```

Priorities:

1. Correct document understanding
2. Reliable action and deadline extraction
3. Grounded answers
4. Source references
5. Clear student-focused UI
6. Simple architecture
7. Easy team integration
8. Practical AWS usage

Avoid unnecessary technology for the sake of technology.

---

# 21. Future Architecture

Potential future extensions:

```text
                    ┌── Calendar
                    │
                    ├── Notifications
                    │
Student ── CampusLens ── Email
                    │
                    ├── OCR
                    │
                    ├── Multilingual
                    │
                    ├── Multi-document reasoning
                    │
                    └── University knowledge base
```

Potential future capabilities include:

- Calendar integration
- Deadline reminders
- Email/document ingestion
- OCR for scanned documents
- Hindi/Gujarati and other multilingual support
- Multi-document reasoning
- University-specific knowledge bases
- More advanced agent workflows

These are outside the initial MVP unless time permits.
