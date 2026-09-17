# CampusLens

AI-powered document understanding agent for students.

## Problem

Students receive confusing academic and administrative documents such as:

- Examination notices
- Syllabi
- Scholarship documents
- Fee notices
- Internship circulars
- Hostel notices

Important information such as deadlines, requirements, and required actions can be difficult to find.

## Solution

CampusLens allows students to upload a document and receive:

- Simple explanations
- Summaries
- Important deadlines
- Required actions
- Document-based question answering
- Source references

## Planned Architecture

Frontend
↓
Django Backend
↓
Strands Agent
↓
Amazon Bedrock
↓
Document Retrieval
↓
AWS Storage/Services

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Async Python

### AI
- Strands Agents
- Amazon Bedrock

### AWS
- Amazon S3
- DynamoDB
- Additional AWS services as required

### Frontend
- To be finalized

## Repository Structure

```text
CampusLens/
├── backend/
├── frontend/
├── tests/
├── docs/
└── infrastructure/