# CampusLens

> AI-powered document understanding for students.

CampusLens is an AI-powered document understanding system designed to help students deal with confusing college documents such as:

- College circulars
- Exam notifications
- Syllabi
- Scholarship notices
- Fee notices
- Internship opportunities
- Hostel notices
- Academic announcements
- Other student-related PDFs

Instead of simply allowing a student to chat with a PDF, CampusLens focuses on turning documents into **clear information and actionable tasks**.

---

## 🎯 Problem

Students receive a large number of college documents, but important information is often buried inside long and confusing PDFs.

A student may need to manually search for:

- What is this document about?
- What do I need to do?
- What is the deadline?
- What documents do I need?
- Where do I submit something?
- How much do I need to pay?
- Which information applies to me?
- Where in the document was this information mentioned?

Missing one important sentence can result in a missed deadline or incomplete submission.

---

## 💡 Solution

CampusLens converts a document into:

```text
PDF
 │
 ▼
Understand
 │
 ├── Summary
 ├── Deadlines
 ├── Required Actions
 ├── Important Information
 ├── Q&A
 └── Source / Page References
```

The main interaction is:

> **"Tell me what I need to do."**

For example:

```text
📄 Exam Circular

Summary:
End-semester examination registration is now open.

Important deadlines:
• Registration: 20 October
• Fee payment: 22 October

Required actions:
1. Complete the examination registration form.
2. Pay the examination fee.
3. Upload the required photograph.
4. Download the confirmation/admit card.

Sources:
• Registration deadline — Page 2
• Fee payment deadline — Page 2
• Photograph requirement — Page 3
```

If the requested information is not present in the document, CampusLens should clearly say:

```text
I couldn't find this information in the uploaded document.
```

rather than inventing an answer.

---

# 🚀 Project Status

## Backend

### Completed

- [x] Django project
- [x] Django REST Framework
- [x] SQLite development database
- [x] Document, page, chunk, deadline, important-date, and action models
- [x] Conversation and message models
- [x] User → Document ownership
- [x] User → Chat ownership
- [x] JWT authentication
- [x] User registration
- [x] `/api/auth/me/`
- [x] Protected API endpoints
- [x] PDF upload and validation
- [x] PDF text extraction with page preservation
- [x] Document chunking
- [x] Document processing pipeline
- [x] Deadline extraction
- [x] Important-date extraction
- [x] Required-action extraction
- [x] Document insights API
- [x] Lightweight lexical / intent-based retrieval
- [x] Strands Agent integration
- [x] Local Ollama model integration
- [x] Conversational document Q&A
- [x] Source/page references
- [x] Chat history and APIs
- [x] Ownership and security checks
- [x] Automated pytest suite

### Current Test Coverage

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

All current tests pass:

```text
23 passed
```

AI-dependent tests mock the AI service, so Ollama does not need to be running for the automated test suite.

### Next

- [ ] Frontend integration
- [ ] Amazon Bedrock integration
- [ ] Amazon S3 integration
- [ ] Containerized AWS deployment
- [ ] Production environment
- [ ] Further retrieval and AI-quality improvements


# 🎨 Frontend

The frontend is being developed separately and integrates with the Django REST API.

Planned interface:

```text
Login
  │
  ▼
Dashboard
  │
  ├── Upload Document
  ├── My Documents
  │      │
  │      └── Document
  │             ├── Summary
  │             ├── Deadlines
  │             ├── Required Actions
  │             ├── Important Dates
  │             └── Ask CampusLens
  │
  └── Chat
```

Planned stack:

- React
- Vite
- JavaScript
- Tailwind CSS
- Django REST Framework API


# ☁️ AWS / AI

CampusLens is developed locally first and then prepared for AWS deployment.

## Local AI Development

```text
React / Vite
     │
     ▼
Django REST API
     │
     ▼
Strands Agent
     │
     ▼
Ollama
```

## AWS Target

```text
                     ┌──────────────┐
                     │   Frontend   │
                     └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Django API   │
                     │  Container   │
                     └──────┬───────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │      S3      │      │   Strands    │
          │  Documents   │      │    Agent     │
          └──────────────┘      └──────┬───────┘
                                       │
                                       ▼
                                ┌──────────────┐
                                │   Bedrock    │
                                │    Model     │
                                └──────────────┘

                  Supporting services:
                    IAM + CloudWatch
```

Planned AWS components:

- Amazon Bedrock
- Strands Agents SDK
- Amazon S3
- IAM
- CloudWatch
- Container deployment infrastructure
- Frontend hosting

Only services that solve an actual project requirement should be introduced.


# 🧰 Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Backend | Django |
| API | Django REST Framework |
| Authentication | JWT / Simple JWT |
| Development Database | SQLite |
| PDF Extraction | pypdf |
| Retrieval | Lightweight lexical / intent-based retrieval |
| AI Agent | Strands Agents SDK |
| Local AI Model | Ollama |
| AWS AI Model | Amazon Bedrock |
| Object Storage | Amazon S3 |
| Frontend | React + Vite |
| Testing | pytest / pytest-django |
| Linting | Ruff |
| Version Control | Git + GitHub |

The MVP intentionally avoids unnecessary infrastructure. Do not add LangChain, LlamaIndex, Redis, Celery, a vector database, or other major components unless they solve an actual requirement.


# 📁 Repository Structure

```text
CampusLens/
│
├── backend/
│   ├── accounts/
│   ├── config/
│   ├── documents/
│   ├── conversations/
│   ├── scripts/
│   │   └── test_agent.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_chats.py
│   │   ├── test_security.py
│   │   ├── test_chat_service.py
│   │   └── test_document_processing.py
│   ├── pytest.ini
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── TEAM.md
├── infrastructure/
├── .gitignore
├── .env.example
├── LICENSE
└── README.md
```


# 👥 Team Setup

## ⚠️ READ THIS BEFORE STARTING

Every teammate must create their **own local development environment**.

Each developer must have their own:

- `.env`
- Django `SECRET_KEY`
- `db.sqlite3`
- Django superuser
- JWT tokens

### Never share these between teammates.

Do not commit:

```text
.env
db.sqlite3
.venv/
AWS credentials
JWT tokens
secret keys
```

The repository contains `.env.example` as a safe configuration template.

---

# 🛠️ Backend Local Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd CampusLens
```

---

## 2. Enter the backend

```bash
cd backend
```

---

## 3. Create your own virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create your own `.env`

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

Generate a secure Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value into:

```env
SECRET_KEY=...
```

Do not use another teammate's secret key.

---

# 🗄️ Local Database

Each teammate has their own SQLite database.

Run:

```bash
python manage.py migrate
```

This creates:

```text
backend/db.sqlite3
```

You do **not** need another teammate's database.

Do not commit `db.sqlite3`.

---

# 👤 Create Your Own Superuser

Create your own Django admin account:

```bash
python manage.py createsuperuser
```

Enter your own:

```text
Username
Email
Password
```

Do not use another teammate's superuser account.

---

# ✅ Verify Backend

Run:

```bash
python manage.py check
```

Then:

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

API:

```text
http://127.0.0.1:8000/api/
```

Django admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔐 Authentication

CampusLens currently uses JWT authentication.

## Obtain token

```http
POST /api/auth/token/
```

Example:

```json
{
    "username": "your-username",
    "password": "your-password"
}
```

Response:

```json
{
    "refresh": "...",
    "access": "..."
}
```

Use the access token for protected APIs:

```http
Authorization: Bearer <access-token>
```

Every teammate should generate their own token using their own account.

---

# 📡 Current API

Base URL:

```text
http://127.0.0.1:8000/api/
```

## Authentication

```text
POST /api/auth/register/
POST /api/auth/token/
POST /api/auth/token/refresh/
GET  /api/auth/me/
```

## Documents

```text
GET    /api/documents/
POST   /api/documents/
GET    /api/documents/<id>/
DELETE /api/documents/<id>/
GET    /api/documents/<id>/insights/
```

## Chats

```text
GET    /api/documents/<document_id>/chats/
POST   /api/documents/<document_id>/chats/
GET    /api/chats/<id>/
DELETE /api/chats/<id>/
GET    /api/chats/<chat_id>/messages/
POST   /api/chats/<chat_id>/messages/
```

For complete request and response contracts, see `docs/API.md`.


# 📄 Document Upload

Upload documents using:

```text
multipart/form-data
```

Required fields:

```text
title
file
```

Example:

```text
title = Exam Circular
file = exam_circular.pdf
```

### Important

Do **not** send:

```text
user
```

The backend automatically determines document ownership from:

```text
request.user
```

This means users can only access their own documents.

---

# 🧪 Testing

The backend uses pytest and pytest-django.

Run the complete suite from `backend/`:

```bash
pytest -v
```

Current coverage:

```text
Authentication       3/3
Documents            3/3
Chats                6/6
Security             7/7
Chat service         2/2
Document processing  2/2
──────────────────────────────
Total               23/23
```

Expected result:

```text
23 passed
```

The AI service is mocked in AI-dependent tests, so Ollama does not need to be running for the automated suite.


# 👨‍💻 Team Responsibilities

## 1. Backend + AI Agent — Naman

Responsible for:

### Backend

- Django
- Django REST Framework
- Authentication
- Document APIs
- User ownership
- PDF processing
- AI API integration

### AI

- Strands Agents SDK
- Amazon Bedrock
- Agent tools
- Document retrieval
- Deadline extraction
- Action extraction
- Document Q&A
- Source/page references

### Next Tasks

```text
Registration
    ↓
/auth/me/
    ↓
PDF extraction
    ↓
Document processing
    ↓
Retrieval
    ↓
Strands Agent
    ↓
Bedrock
    ↓
AI response API
```

---

# 2. Frontend + UI/UX

**Start now. Backend AI does not need to be finished.**

Build:

- Login page
- Registration page
- Dashboard
- Document upload
- Document list
- Document details
- Summary UI
- Deadline UI
- Required actions
- Important information
- Chat interface
- Source/page references
- Loading states
- Error states
- Empty states

Use mock AI responses until the actual AI API is available.

The frontend should communicate with:

```text
http://127.0.0.1:8000/api/
```

---

# 3. AWS / DevOps

Responsible for:

- AWS account/project setup
- IAM
- Amazon S3
- Amazon Bedrock access
- AWS environment configuration
- CloudWatch
- Deployment
- Production environment

### Security

Never commit:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
```

or any other credentials.

Use environment variables or appropriate AWS credential mechanisms.

---

# 4. AI / RAG / QA

Responsible for:

- PDF extraction experiments
- Chunking
- Retrieval
- Prompt design
- Strands research
- Bedrock model testing
- Deadline extraction
- Action extraction
- Q&A evaluation
- Source/page attribution
- AI response quality testing

Start simple.

The first retrieval implementation does not need a complicated vector database.

---

# 🔄 Parallel Development

The team should work in parallel.

```text
                       ┌── Frontend
                       │
                       ├── AWS / DevOps
main ──────────────────┼── AI / RAG
                       │
                       └── Backend
```

Nobody should wait for the entire project to be completed before starting.

For example:

```text
Frontend
   ↓
Build UI using mock data
   ↓
Connect APIs when available
```

Similarly:

```text
AI/RAG
   ↓
Test PDF extraction independently
   ↓
Test retrieval
   ↓
Connect to backend
```

---

# 🌿 Git Workflow

Do not directly develop on `main`.

Before starting:

```bash
git checkout main
git pull origin main
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Examples:

```bash
git checkout -b feature/frontend-dashboard
```

```bash
git checkout -b feature/bedrock-agent
```

```bash
git checkout -b feature/aws-deployment
```

---

# 💾 Commit Workflow

After completing a logical piece of work:

```bash
git add .
```

Commit:

```bash
git commit -m "feat: add frontend dashboard"
```

Push:

```bash
git push -u origin feature/frontend-dashboard
```

Then open a Pull Request into:

```text
main
```

---

# 📌 Branches

Recommended branches:

```text
main
│
├── feature/backend
├── feature/frontend
├── feature/aws
└── feature/rag
```

If a feature needs a more specific branch, create one from the latest `main`.

---

# ⚠️ Before Creating a Pull Request

Check:

```bash
git status
```

Make sure you did not accidentally include:

```text
.env
db.sqlite3
.venv/
__pycache__/
AWS credentials
JWT tokens
```

Run:

```bash
python manage.py check
```

Run tests when available:

```bash
pytest
```

Then push your branch and create the PR.

---

# 🔒 Security Rules

Never commit:

```text
.env
db.sqlite3
.venv/
*.pyc
__pycache__/
AWS credentials
API keys
JWT tokens
private credentials
```

Never hard-code secrets in Python source code.

Use:

```text
.env
```

for local development.

Use appropriate AWS/IAM mechanisms for deployed environments.

---

# 🧠 AI Design

The initial AI architecture uses one agent.

```text
User
 │
 ▼
Django API
 │
 ▼
Strands Agent
 │
 ├── search_document()
 ├── structured document insights
 └── conversation history
 │
 ▼
Local: Ollama
AWS: Amazon Bedrock
 │
 ▼
Answer + Sources
```

The agent should answer from document evidence, preserve source/page references, understand follow-up questions, and avoid unsupported claims.

If the document does not contain enough information, CampusLens should say:

```text
I couldn't find this information in the uploaded document.
```


# 📚 Document Understanding Pipeline

```text
Upload PDF
    ↓
Validate PDF
    ↓
Extract Text
    ↓
Create Document Pages
    ↓
Chunk Text
    ↓
Extract Deadlines
    ↓
Extract Important Dates
    ↓
Extract Required Actions
    ↓
Persist Structured Data
    ↓
Retrieve Relevant Chunks
    ↓
Strands Agent
    ↓
AI Answer + Source Pages
```

The system preserves page numbers throughout processing so that extracted information and AI answers can point back to the original document.


# 🎯 MVP

The MVP should solve one problem well:

> **Help a student understand a college document and know what they need to do.**

Minimum flow:

```text
Student
   ↓
Upload PDF
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
Get source/page references
```

Example:

```text
Student:
"What do I need to do before the deadline?"

CampusLens:

Required actions:
1. Fill the registration form.
2. Upload your photograph.
3. Pay the required fee.

Deadline:
20 October 2026

Sources:
Page 2
Page 3
```

---

# 🚫 What We Are NOT Building Initially

Do not expand the MVP unnecessarily.

Avoid initially building:

- Complex multi-agent systems
- Large-scale university knowledge graphs
- Complicated vector databases
- Full email ingestion
- Calendar automation
- Mobile applications
- Advanced personalization
- Large-scale notification systems
- Multiple AI providers
- Complex microservices

These can become future features if time allows.

---

# 🔮 Future Features

Possible future improvements:

- Hindi/Gujarati support
- OCR for scanned documents
- Email document ingestion
- Calendar integration
- Deadline reminders
- Personalized student profiles
- Multiple document reasoning
- University-specific knowledge base
- Automatic notifications
- Document comparison
- Mobile application
- Advanced agent workflows
- Offline-first capabilities

These are **not required for the initial MVP**.

---

# 🧪 Quality Requirements

CampusLens should prioritize correctness over simply generating fluent AI responses.

The AI should:

### 1. Use document evidence

Answers should be based on the uploaded document.

### 2. Avoid hallucination

If information is unavailable:

```text
I couldn't find this information in the uploaded document.
```

### 3. Show sources

Whenever possible:

```text
Source: Page 2
```

### 4. Extract actionable information

The system should prioritize:

```text
What?
When?
Who?
Where?
How?
What must I submit?
What must I pay?
What is the deadline?
```

---

# 📖 Documentation

Additional documentation is available in:

```text
docs/
├── API.md
├── ARCHITECTURE.md
└── TEAM.md
```

### `docs/API.md`

Contains API contracts and endpoint information.

### `docs/ARCHITECTURE.md`

Contains the planned system architecture and component relationships.

### `docs/TEAM.md`

Contains team responsibilities, development workflow and handoff information.

---

# 🧑‍🤝‍🧑 Team Handoff

## Frontend

**Start now. Backend AI does not need to be finished.**

Build the complete UI using mock data.

Current backend endpoints:

```text
POST   /api/auth/token/
POST   /api/auth/token/refresh/

GET    /api/documents/
POST   /api/documents/
GET    /api/documents/<id>/
DELETE /api/documents/<id>/
```

Backend:

```text
http://127.0.0.1:8000/api/
```

Authentication:

```text
Authorization: Bearer <access-token>
```

---

## AWS

Start working on AWS setup independently.

Coordinate with the backend/AI developer when Bedrock and S3 integration is ready.

---

## AI/RAG

Start experimenting with:

```text
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Retrieval
 ↓
Prompt
 ↓
Bedrock
```

The goal is to have a working AI pipeline that can later be connected to Django.

---

# 🏁 Definition of MVP Done

The MVP is considered functional when a student can:

```text
1. Register / log in
        ↓
2. Upload a college PDF
        ↓
3. See the uploaded document
        ↓
4. Get an understandable summary
        ↓
5. See important deadlines
        ↓
6. See required actions
        ↓
7. Ask questions about the document
        ↓
8. Receive answers grounded in the document
        ↓
9. See source/page references
```

---

# 📊 Development Philosophy

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

Do not optimize for the number of technologies used.

Optimize for:

- Working functionality
- Clear user experience
- Reliable answers
- Good source attribution
- Real-world usefulness
- Clean architecture
- Good teamwork

---

# 🤝 Contribution

1. Create a feature branch.
2. Make a focused change.
3. Test your change.
4. Commit with a meaningful message.
5. Push the branch.
6. Open a Pull Request into `main`.
7. Explain what changed.
8. Mention any known limitations.

Keep Pull Requests focused and easy to review.

---

# 📜 License

MIT License

---

# 🚀 CampusLens

```text
Understand the document.
Find what matters.
Know what to do.
Don't miss the deadline.
```
