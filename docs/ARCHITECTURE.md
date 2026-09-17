# CampusLens Architecture

## 1. Purpose

CampusLens is designed as a document-to-action system for students.

The system takes college documents and turns them into:

```text
Summary
Deadlines
Required Actions
Important Information
Questions & Answers
Source / Page References
```

The architecture should remain simple during the hackathon.

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
│  AI API                       │
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
│   Database   │          │      S3      │
│    SQLite    │          │   Documents  │
└──────────────┘          └──────────────┘
```

---

# 3. Current Backend Architecture

The Django backend currently contains:

```text
backend/
├── accounts/
├── config/
├── documents/
└── conversations/
```

## `config`

Project configuration:

- Settings
- Root URLs
- WSGI/ASGI configuration

## `accounts`

Authentication-related functionality.

Current state:

```text
App created
Registration: pending
/me endpoint: pending
```

Django's built-in `User` model is currently used.

## `documents`

Responsible for:

- Document model
- File upload
- Document ownership
- Document API

## `conversations`

Responsible for:

- Chat model
- Message model
- Chat/document relationships

Conversation APIs are still pending.

---

# 4. Data Model

Current relationship:

```text
User
 │
 ├───────────────< Document
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

Document 1 ──── N Chat

Chat 1 ──── N Message
```

---

# 5. Document Lifecycle

The document model supports:

```text
uploaded
processing
processed
failed
```

Target lifecycle:

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

# 6. AI Processing Pipeline

Target MVP pipeline:

```text
PDF Upload
    │
    ▼
PDF Validation
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Document Retrieval
    │
    ▼
Strands Agent
    │
    ▼
Amazon Bedrock
    │
    ▼
Structured Result
    │
    ├── Summary
    ├── Deadlines
    ├── Actions
    ├── Answer
    └── Sources
```

---

# 7. Strands Agent

The first implementation should use **one agent**.

Do not start with a multi-agent system.

Possible tools:

```text
search_document()
extract_deadlines()
extract_actions()
explain_section()
```

The agent should use these tools to ground responses in document content.

---

# 8. Retrieval

The first retrieval implementation should be simple.

Possible initial approach:

```text
PDF
 ↓
pypdf
 ↓
Plain text
 ↓
Chunks
 ↓
Relevant chunk selection
 ↓
Agent
```

If a stronger retrieval solution is required later, the architecture can evolve toward:

```text
S3
 ↓
Bedrock Knowledge Bases / other retrieval layer
 ↓
Relevant document content
 ↓
Strands Agent
```

Do not introduce a vector database unless it solves an actual requirement.

---

# 9. Source Attribution

Source references are a core feature.

The system should preserve document location information wherever possible.

Target response:

```text
Answer:
The examination registration deadline is 20 October.

Source:
Page 2
```

For extracted actions:

```text
Action:
Upload a passport-size photograph.

Source:
Page 3
```

The exact implementation will depend on the PDF extraction and retrieval approach.

---

# 10. AWS Architecture

Planned AWS components:

```text
React
  │
  ▼
Django API
  │
  ├──────────────► S3
  │
  └──────────────► Strands
                     │
                     ▼
                  Bedrock
```

Supporting services:

```text
IAM
CloudWatch
Deployment infrastructure
```

AWS credentials must never be stored in Git.

---

# 11. Development vs Production

## Development

```text
Django
SQLite
Local file storage
Local `.env`
Local development server
```

## Production target

```text
Django API
Production database
Amazon S3
Amazon Bedrock
IAM
CloudWatch
Production deployment
```

The exact production deployment architecture will be decided after the MVP is working.

---

# 12. Security Principles

### Authentication

Protected APIs use JWT authentication.

### Authorization

Documents are filtered by:

```python
user=request.user
```

### Secrets

Secrets stay outside Git:

```text
.env
AWS credentials
API keys
JWT tokens
```

### File Validation

The upload pipeline should validate that the uploaded file is actually a supported PDF, not merely rely on the filename extension.

A maximum upload size should also be enforced.

---

# 13. Design Principles

CampusLens should follow:

```text
Simple
 ↓
Working
 ↓
Tested
 ↓
Integrated
 ↓
Improved
```

Priorities:

1. Correct document understanding
2. Reliable action/deadline extraction
3. Grounded answers
4. Source references
5. Clear UI
6. Simple architecture
7. Easy team integration

Avoid unnecessary technology for the sake of technology.

---

# 14. Future Architecture

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
                    └── Multi-document reasoning
```

These are outside the initial MVP unless time permits.
