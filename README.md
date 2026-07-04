# AI Resume Screener

## Overview

AI Resume Screener is a web application that analyzes resumes against a job description using Large Language Models (LLMs). It helps candidates evaluate their resumes and enables recruiters to screen multiple candidates efficiently.

## Features

- Candidate Resume Analysis
- Recruiter Bulk Resume Screening
- AI-based Resume Evaluation
- Match Score Generation
- Candidate Selection Decision
- CSV Report Generation
- Download History
- View and Delete Downloaded Reports

## Technologies Used

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### AI
- Groq API
- Llama 3.1 8B Instant

### Libraries
- PyPDF2
- Pandas
- Requests
- Python-dotenv

## Project Structure

```
AI-Resume-Screener/
│
├── app/
│   ├── agents/
│   ├── ui/
│   ├── main.py
│   ├── parsepdf.py
│   └── prompts.py
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd AI-Resume-Screener

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

## Running Backend

```bash
uvicorn app.main:app --reload
```

## Running Frontend

```bash
streamlit run app/ui/main.py
```

## Environment Variables

Create a `.env` file containing:

```
GROQ_API_KEY=your_groq_api_key
API_URL=http://127.0.0.1:8000
```

## Future Improvements

- ATS Score
- Resume Ranking
- Authentication
- Database Integration
- Resume History
- Cloud Deployment