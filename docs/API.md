# CampusLens API Documentation

## Base URL

`http://127.0.0.1:8000/api/`

Protected endpoints require:

`Authorization: Bearer <access_token>`

---

# 1. Authentication

## Register

`POST /auth/register/`

Request:

```json
{
  "username": "student",
  "email": "student@example.com",
  "password": "TestPassword123!"
}
```

## Login

`POST /auth/token/`

Request:

```json
{
  "username": "student",
  "password": "TestPassword123!"
}
```

Success:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

## Refresh Token

`POST /auth/token/refresh/`

Request:

```json
{
  "refresh": "<refresh_token>"
}
```

## Current User

`GET /auth/me/`

Authentication required.

---

# 2. Documents

## List Documents

`GET /documents/`

Authentication required.

Returns only documents belonging to the authenticated user.

Example:

```json
[
  {
    "id": 9,
    "title": "Examination Notice",
    "file": "/media/documents/exam_notice.pdf",
    "status": "processed",
    "uploaded_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:01:00Z"
  }
]
```

## Upload Document

`POST /documents/`

Authentication required.

Content type: `multipart/form-data`

Form fields:

```text
title
file
```

Validation:
- Must be a PDF.
- Maximum size: 10 MB.

The backend extracts document pages, text chunks, deadlines, important dates, and required actions.

## Get Document Details

`GET /documents/<id>/`

Authentication required.

Example:

```json
{
  "id": 9,
  "title": "Examination Notice",
  "file": "/media/documents/exam_notice.pdf",
  "status": "processed",
  "deadlines": [
    {
      "id": 1,
      "date": "20 October 2026",
      "description": "Submit examination form",
      "page_number": 1
    }
  ],
  "important_dates": [
    {
      "id": 1,
      "date": "25 October 2026",
      "description": "Admit card available",
      "page_number": 1
    }
  ],
  "actions": [
    {
      "id": 1,
      "action": "Submit examination form",
      "page_number": 1
    }
  ]
}
```

## Delete Document

`DELETE /documents/<id>/`

Authentication required.

Success: `204 No Content`

---

# 3. Document Insights

## Get Insights

`GET /documents/<id>/insights/`

Authentication required.

Example:

```json
{
  "summary": "2 deadlines identified. 2 required actions identified. 1 important date identified.",
  "stats": {
    "deadlines": 2,
    "important_dates": 1,
    "actions": 2
  },
  "deadlines": [
    {
      "id": 1,
      "date": "20 October 2026",
      "description": "Submit examination form",
      "page_number": 1
    },
    {
      "id": 2,
      "date": "22 October 2026",
      "description": "Pay examination fee",
      "page_number": 1
    }
  ],
  "important_dates": [
    {
      "id": 1,
      "date": "25 October 2026",
      "description": "Admit card available",
      "page_number": 1
    }
  ],
  "actions": [
    {
      "id": 1,
      "action": "Submit examination form",
      "page_number": 1
    },
    {
      "id": 2,
      "action": "Pay examination fee",
      "page_number": 1
    }
  ]
}
```

If processing is incomplete: `409 Conflict`

---

# 4. Chats

## List Document Chats

`GET /documents/<document_id>/chats/`

Authentication required.

## Create Chat

`POST /documents/<document_id>/chats/`

Request:

```json
{
  "title": "Exam Notice Chat"
}
```

Success:

```json
{
  "id": 2,
  "document": 9,
  "title": "Exam Notice Chat",
  "created_at": "2026-09-20T10:00:00Z",
  "updated_at": "2026-09-20T10:00:00Z"
}
```

## Get Chat

`GET /chats/<id>/`

Authentication required.

Returns the chat and message history.

## Delete Chat

`DELETE /chats/<id>/`

Authentication required.

Success: `204 No Content`

---

# 5. Chat Messages

## Get Messages

`GET /chats/<chat_id>/messages/`

Authentication required.

Example:

```json
[
  {
    "id": 1,
    "role": "user",
    "content": "What do I need to do?",
    "created_at": "2026-09-20T10:00:00Z"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "You need to submit the examination form. [Source: Page 1]",
    "created_at": "2026-09-20T10:00:02Z"
  }
]
```

## Send Message

`POST /chats/<chat_id>/messages/`

Authentication required.

Request:

```json
{
  "content": "What do I need to do?"
}
```

Maximum message length: `10,000 characters`

Success:

```json
{
  "user_message": {
    "id": 1,
    "role": "user",
    "content": "What do I need to do?",
    "created_at": "2026-09-20T10:00:00Z"
  },
  "assistant_message": {
    "id": 2,
    "role": "assistant",
    "content": "You need to submit the examination form. [Source: Page 1]",
    "created_at": "2026-09-20T10:00:02Z"
  },
  "sources": [
    {
      "page_number": 1
    }
  ]
}
```

AI failure:

```json
{
  "detail": "Unable to generate an AI response."
}
```

HTTP status: `500`

---

# 6. HTTP Status Codes

| Status | Meaning |
|---|---|
| `200` | Successful request |
| `201` | Resource created |
| `204` | Resource deleted |
| `400` | Invalid request |
| `401` | Authentication required or invalid |
| `404` | Resource not found or inaccessible |
| `409` | Document processing is not complete |
| `500` | Internal or AI processing error |

---

# 7. Security and Ownership

CampusLens enforces user ownership at the API level.

Users cannot:
- Access another user's documents.
- Delete another user's documents.
- Access another user's chats.
- Read another user's messages.
- Send messages to another user's chats.

Unauthorized resources return `404 Not Found`.

---

# 8. Frontend Application Flow

```text
Register / Login
       ↓
Dashboard
       ↓
Upload PDF
       ↓
Document Processing
       ↓
Document Details
       ↓
Insights
   ├── Summary
   ├── Required Actions
   ├── Deadlines
   └── Important Dates
       ↓
Create Chat
       ↓
Ask Question
       ↓
AI Answer + Source Page
```

## Primary CampusLens Interaction

The document page should prominently provide:

`What do I need to do?`

The response should prioritize:
1. Required actions
2. Corresponding deadlines
3. Relevant source pages

Informational dates should remain separate from required actions unless the document explicitly requires the student to perform an action.
