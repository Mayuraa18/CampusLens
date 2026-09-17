# CampusLens API Documentation

This document describes the current backend API and the planned AI endpoints.

## Base URL

Local development:

```text
http://127.0.0.1:8000/api/
```

All protected endpoints require a JWT access token unless explicitly stated otherwise.

```http
Authorization: Bearer <access-token>
```

---

## Authentication

### Obtain JWT Token

```http
POST /api/auth/token/
Content-Type: application/json
```

Request:

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

Response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

### Refresh JWT Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json
```

Request:

```json
{
  "refresh": "<refresh-token>"
}
```

Response:

```json
{
  "access": "<new-access-token>"
}
```

### Planned: Current User

```http
GET /api/auth/me/
```

Status: **Not implemented yet.**

---

# Documents

## List User Documents

```http
GET /api/documents/
Authorization: Bearer <access-token>
```

Returns only documents belonging to the authenticated user.

Example response:

```json
[
  {
    "id": 1,
    "title": "Exam Circular",
    "file": "/media/documents/exam_circular.pdf",
    "status": "uploaded",
    "uploaded_at": "2026-09-18T00:00:00Z",
    "updated_at": "2026-09-18T00:00:00Z"
  }
]
```

---

## Upload Document

```http
POST /api/documents/
Authorization: Bearer <access-token>
Content-Type: multipart/form-data
```

Form fields:

```text
title
file
```

Example:

```text
title = Exam Circular
file = exam_circular.pdf
```

Do **not** send a `user` field.

The backend assigns ownership from the authenticated request user.

Current response:

```json
{
  "id": 1,
  "title": "Exam Circular",
  "file": "/media/documents/exam_circular.pdf",
  "status": "uploaded",
  "uploaded_at": "2026-09-18T00:00:00Z",
  "updated_at": "2026-09-18T00:00:00Z"
}
```

### Current status values

```text
uploaded
processing
processed
failed
```

The processing states are part of the model and will be used by the document-processing pipeline.

---

## Retrieve Document

```http
GET /api/documents/<id>/
Authorization: Bearer <access-token>
```

Returns a document only if it belongs to the authenticated user.

If the document does not exist or belongs to another user:

```json
{
  "detail": "Document not found."
}
```

Status:

```text
404 Not Found
```

---

## Delete Document

```http
DELETE /api/documents/<id>/
Authorization: Bearer <access-token>
```

Successful response:

```text
204 No Content
```

Deleting a document also deletes its related chats and messages through Django cascade relationships.

---

# Conversations

Conversation database models currently exist, but conversation API endpoints are not implemented yet.

Planned endpoints:

```text
GET    /api/documents/<id>/chats/
POST   /api/documents/<id>/chats/
GET    /api/chats/<id>/
DELETE /api/chats/<id>/

GET    /api/chats/<id>/messages/
POST   /api/chats/<id>/messages/
```

---

# AI Endpoints — Planned

The AI API should eventually expose functionality similar to:

```text
POST /api/documents/<id>/process/
GET  /api/documents/<id>/analysis/
POST /api/documents/<id>/ask/
```

These endpoints are **planned, not currently implemented**.

A target structured AI response is:

```json
{
  "summary": "...",
  "deadlines": [
    {
      "title": "Registration deadline",
      "date": "2026-10-20",
      "source": {
        "page": 2
      }
    }
  ],
  "actions": [
    {
      "action": "Complete examination registration",
      "source": {
        "page": 2
      }
    }
  ],
  "answer": "...",
  "sources": [
    {
      "page": 2,
      "text": "..."
    }
  ]
}
```

The exact schema will be finalized when the AI pipeline is implemented.

---

# Error Handling

Expected authentication errors:

```text
401 Unauthorized
```

Expected missing-resource errors:

```text
404 Not Found
```

Expected validation errors:

```text
400 Bad Request
```

Frontend developers should handle:

- Loading
- Success
- Validation errors
- Authentication errors
- Not found
- Server errors
- Empty document lists
- Document processing states

---

# Ownership and Security

The client must never decide document ownership.

Bad:

```json
{
  "title": "Circular",
  "file": "...",
  "user": 5
}
```

Correct:

```json
{
  "title": "Circular",
  "file": "..."
}
```

The backend uses:

```python
request.user
```

to determine ownership.

This prevents one authenticated user from requesting another user's documents through the normal document endpoints.

---

# Development Notes

The API is currently optimized for local MVP development.

Current storage:

```text
SQLite + Django FileField
```

Planned production storage:

```text
Amazon S3
```

The API contract may evolve as Strands, Bedrock, retrieval, and frontend integration are implemented.
