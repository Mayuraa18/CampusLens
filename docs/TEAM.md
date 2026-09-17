# CampusLens Team Guide

This document explains how the team should work on CampusLens during development.

---

# Team Structure

## Backend + AI Agent

**Owner: Naman**

Responsibilities:

- Django
- Django REST Framework
- JWT authentication
- Document APIs
- User ownership
- PDF processing
- Strands Agents SDK
- Amazon Bedrock
- Agent tools
- AI response API
- Deadline extraction
- Action extraction
- Source/page references

Current backend foundation is already available.

Next backend tasks:

```text
Registration
    ↓
/api/auth/me/
    ↓
PDF validation
    ↓
PDF extraction
    ↓
Processing pipeline
    ↓
Retrieval
    ↓
Strands Agent
    ↓
Bedrock
    ↓
AI API
```

---

# Frontend + UI/UX

Responsibilities:

- React/Vite setup
- Login
- Registration
- Dashboard
- Document upload
- Document list
- Document details
- Summary
- Deadlines
- Required actions
- Chat
- Source/page references
- Loading states
- Error states
- Empty states

## Start immediately

The frontend does **not** need to wait for the AI backend.

Use mock data for unfinished AI endpoints.

Current backend API:

```text
POST   /api/auth/token/
POST   /api/auth/token/refresh/

GET    /api/documents/
POST   /api/documents/
GET    /api/documents/<id>/
DELETE /api/documents/<id>/
```

Local API:

```text
http://127.0.0.1:8000/api/
```

---

# AWS / DevOps

Responsibilities:

- IAM
- S3
- Bedrock access
- AWS environment setup
- CloudWatch
- Deployment
- Production configuration

Coordinate with Backend + AI when S3 and Bedrock integration begins.

Never commit AWS credentials.

---

# AI / RAG / QA

Responsibilities:

- PDF extraction
- Chunking
- Retrieval
- Prompt design
- Strands research
- Bedrock testing
- Deadline extraction
- Action extraction
- Source attribution
- Evaluation
- AI response testing

Start with a simple retrieval pipeline.

---

# Local Development

Every teammate must create their own environment.

Each person gets their own:

```text
.env
SECRET_KEY
db.sqlite3
Django superuser
JWT tokens
```

Never share these.

---

## Setup

```bash
git clone <repository-url>
cd CampusLens
cd backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

Windows activation:

```powershell
.venv\Scripts\activate
```

---

# Environment Variables

Create:

```text
backend/.env
```

Example:

```env
SECRET_KEY=your-own-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
AWS_REGION=ap-south-1
```

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Never commit `.env`.

---

# Database

Each developer has a separate SQLite database.

Run:

```bash
python manage.py migrate
```

Do not copy another developer's `db.sqlite3`.

Do not commit it.

---

# Superuser

Each teammate should create their own:

```bash
python manage.py createsuperuser
```

Do not share admin credentials.

---

# Git Workflow

Never directly develop on `main`.

Start with:

```bash
git checkout main
git pull origin main
```

Create a branch:

```bash
git checkout -b feature/your-feature
```

Examples:

```bash
feature/frontend-dashboard
feature/bedrock-agent
feature/aws-deployment
feature/document-retrieval
```

---

# Commit Workflow

Make a focused change:

```bash
git add .
git commit -m "feat: add document dashboard"
```

Push:

```bash
git push -u origin feature/your-feature
```

Then open a Pull Request into:

```text
main
```

---

# Before Pull Request

Run:

```bash
git status
```

Make sure no secrets or local files are staged.

Run backend checks:

```bash
python manage.py check
```

Run tests when available:

```bash
pytest
```

---

# Files That Must Never Be Committed

```text
.env
db.sqlite3
.venv/
__pycache__/
*.pyc
AWS credentials
API keys
JWT tokens
private credentials
```

---

# Parallel Development

The team should work independently where possible.

```text
                         ┌── Frontend
                         │
                         ├── AWS / DevOps
main ────────────────────┼── AI / RAG
                         │
                         └── Backend
```

Do not wait for another component to be completely finished.

Use:

```text
Mock UI
Mock AI responses
API contracts
Small integration tests
```

to keep development moving.

---

# Integration Rules

## Frontend ↔ Backend

Use the API contract in:

```text
docs/API.md
```

Do not invent request fields without coordinating with the backend.

For document upload, send:

```text
title
file
```

Do not send:

```text
user
```

The backend determines ownership from the authenticated user.

---

# AI ↔ Backend

AI functionality should be exposed through clear service/API boundaries.

Avoid placing large amounts of agent logic directly inside Django views.

Prefer:

```text
Django View
    ↓
Service
    ↓
Agent
    ↓
Tools / Retrieval
    ↓
Bedrock
```

This keeps the backend easier to test.

---

# Definition of Done

A feature is ready for integration when:

- It works locally.
- It has been tested.
- It does not expose secrets.
- It follows the existing project structure.
- It has a focused commit.
- The branch is pushed.
- A Pull Request is opened.
- Any known limitations are documented.

---

# MVP Target

The team should ultimately deliver:

```text
Student
   ↓
Login
   ↓
Upload College PDF
   ↓
CampusLens processes document
   ↓
Summary
   ↓
Deadlines
   ↓
Required Actions
   ↓
Ask Questions
   ↓
Grounded Answer
   ↓
Source / Page References
```

The goal is not to build the largest system.

The goal is to build a **working, useful document-to-action experience for students**.

---

# Communication

When handing work to another teammate, include:

```text
What changed
What is ready
How to test it
What API/interface is expected
What is still missing
```

Keep `main` stable and communicate before making changes that affect another team's interface.
