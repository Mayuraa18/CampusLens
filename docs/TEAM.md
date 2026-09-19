# CampusLens Team Guide

This document explains how the team should work on CampusLens during development.

---

# Team Structure

## Backend + AI Agent

**Owner: Backend + AI Developer**

Responsibilities:

- Django
- Django REST Framework
- JWT authentication
- Document APIs
- User ownership
- PDF processing
- Document chunking
- Retrieval
- Strands Agents SDK
- Local Ollama integration
- Amazon Bedrock integration
- Agent tools
- AI response API
- Deadline extraction
- Important-date extraction
- Action extraction
- Document Q&A
- Source/page references

### Current Status

The backend foundation is already available.

Completed:

```text
Django / DRF
    ↓
Authentication
    ↓
Document APIs
    ↓
PDF processing
    ↓
Pages + chunks
    ↓
Deadlines
    ↓
Important dates
    ↓
Required actions
    ↓
Retrieval
    ↓
Strands Agent
    ↓
Ollama local AI
    ↓
Document Q&A
    ↓
Source/page references
```

Current next tasks:

```text
Frontend integration
        ↓
Bedrock integration
        ↓
S3 integration
        ↓
AI quality improvements
        ↓
Production deployment
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
- Important dates
- Chat
- Source/page references
- Loading states
- Error states
- Empty states
- Backend API integration

## Start immediately

The frontend does **not** need to wait for the AI backend.

Use mock data for features that are not yet connected.

Current backend API:

```text
POST   /api/auth/register/
POST   /api/auth/token/
POST   /api/auth/token/refresh/
GET    /api/auth/me/

GET    /api/documents/
POST   /api/documents/
GET    /api/documents/<id>/
DELETE /api/documents/<id>/
GET    /api/documents/<id>/insights/

GET    /api/documents/<document_id>/chats/
POST   /api/documents/<document_id>/chats/

GET    /api/chats/<id>/
DELETE /api/chats/<id>/

GET    /api/chats/<chat_id>/messages/
POST   /api/chats/<chat_id>/messages/
```

Local API:

```text
http://127.0.0.1:8000/api/
```

The complete API contract is maintained in:

```text
docs/API.md
```

---

# AWS / DevOps

Responsibilities:

- AWS environment setup
- IAM
- Amazon S3
- Amazon Bedrock access
- Containerization
- Docker / Finch
- Deployment
- CloudWatch
- Production configuration
- AWS security configuration

### Planned deployment architecture

```text
Frontend
    ↓
Containerized Django API
    ↓
┌───────────────┬───────────────┐
│      S3       │    Bedrock    │
│   Documents   │   AI Models   │
└───────────────┴───────────────┘
        │
      IAM
        │
   CloudWatch
```

The deployment target may use ECS/Fargate or ECS Express Mode depending on the final deployment requirements.

### Development strategy

AWS work should be prepared locally first where possible.

```text
Build locally
    ↓
Test locally
    ↓
Containerize
    ↓
Configure AWS
    ↓
Deploy
    ↓
Test deployed application
```

Do not add AWS services simply to increase the number of services used.

Every service should have a real project requirement.

Never commit AWS credentials.

---

# Testing / QA

Responsibilities:

- pytest
- pytest-django
- API testing
- Authentication testing
- Authorization testing
- Ownership/security testing
- Document-processing testing
- Chat-service testing
- Regression testing
- AI response evaluation
- Integration testing
- CI setup when appropriate

### Current automated tests

The backend currently has:

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

Run:

```bash
pytest -v
```

AI-dependent functionality is mocked in the automated tests where appropriate, so the complete test suite does not require Ollama to be running.

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

Recommended branches:

```text
feature/backend
feature/frontend
feature/aws
feature/rag
feature/tests
```

More specific branches can be created when needed:

```text
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

Run:

```bash
python manage.py check
```

Run the test suite:

```bash
pytest
```

Then push the branch and open a Pull Request.

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
main ────────────────────┼── Backend + AI
                         │
                         └── Testing / QA
```

Do not wait for another component to be completely finished.

Use:

```text
Mock UI
Mock AI responses
API contracts
Unit tests
Integration tests
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
AI Model
```

Local development:

```text
AI Model → Ollama
```

AWS deployment:

```text
AI Model → Amazon Bedrock
```

This separation keeps the backend easier to test and makes local-to-AWS migration simpler.

---

# AWS ↔ Backend

The AWS/DevOps and Backend/AI developers should coordinate around:

```text
S3
    ↓
Document storage

Bedrock
    ↓
AI inference

IAM
    ↓
AWS permissions

CloudWatch
    ↓
Logs / monitoring

Container deployment
    ↓
Django API
```

AWS credentials should never be placed inside the repository.

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

The core experience is:

> **"Tell me what I need to do."**

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
Known limitations
```

Keep `main` stable and communicate before making changes that affect another team's interface.
