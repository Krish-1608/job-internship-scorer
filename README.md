# Job / Internship Scorer

An AI-powered job and internship application tracker that analyzes a candidate's resume against a job description and helps track application decisions.

## Overview

The Job / Internship Scorer helps candidates evaluate how well their resume matches a specific job or internship before applying.

The application uses an AI-powered backend to analyze the resume and job description and provides a structured assessment including:

* Resume fit score
* Matched skills
* Missing skills
* Strengths
* Weaknesses
* Experience match
* Education match
* Overall explanation

After reviewing the analysis, the user can choose whether to apply and, if they decide to apply, save the company and application date to a MySQL database.

## Features

### Resume Analysis

* Upload a PDF resume
* Enter a job description
* Extract resume text from the PDF
* Compare resume content with the job description using an LLM
* Generate a structured analysis

### Application Tracking

After analyzing a job, the user can:

* Choose **I will Apply**
* Choose **I will NOT Apply**
* Enter the company name
* Select the application date
* Save the application to MySQL

### Structured AI Results

The analysis provides:

```text
Fit Score
Matched Skills
Missing Skills
Strengths
Weaknesses
Experience Match
Education Match
Overall Explanation
```

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Lucide React
* Replit

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* pypdf

### Database

* MySQL
* mysql-connector-python

### AI

* LLM API for resume and job-description analysis

### Development / API Exposure

* ngrok

## Architecture

```text
                    User
                      │
                      ▼
              React / TypeScript
                   Frontend
                      │
                      │ HTTPS
                      ▼
                    ngrok
                      │
                      ▼
                 FastAPI API
                      │
            ┌─────────┴─────────┐
            │                   │
            ▼                   ▼
       LLM API               MySQL
            │                   │
            ▼                   ▼
       Resume Analysis     Application Data
```

## Main API Endpoints

### Analyze Resume

```text
POST /analyze-resume
```

Accepts:

* PDF resume
* Job description

Returns structured resume-job analysis.

### Save Application

```text
POST /applications
```

Accepts:

```json
{
  "name": "Krish",
  "company": "Example Company",
  "application_date": "2026-09-28"
}
```

The application is stored in the MySQL `cand_info` table.

## Database

The application uses a MySQL database named:

```text
Application_tracker
```

The main table is:

```text
cand_info
```

with fields:

| Field            | Type    |
| ---------------- | ------- |
| id               | INT     |
| name             | VARCHAR |
| company          | VARCHAR |
| Application_date | DATE    |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Krish-1608/job-internship-scorer.git
cd job-internship-scorer
```

### 2. Create a Python virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn pypdf pydantic mysql-connector-python python-dotenv
```

Install any additional AI SDK required by the current backend configuration.

### 4. Configure environment variables

Create a `.env` file:

```text
MYSQL_PASSWORD=your_mysql_password
```

Add other API credentials required by the AI provider as environment variables.

**Never commit `.env` or API keys to GitHub.**

### 5. Start FastAPI

```bash
uvicorn main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Expose the API during development

```bash
ngrok http 8000
```

Use the generated HTTPS ngrok URL in the frontend API configuration.

## Project Workflow

```text
Upload Resume
      ↓
Enter Job Description
      ↓
AI Resume Analysis
      ↓
Review Fit Score & Analysis
      ↓
 ┌───────────────┐
 │               │
 ▼               ▼
Apply        Don't Apply
 │
 ▼
Enter Company
 │
 ▼
Select Application Date
 │
 ▼
Save Application
 │
 ▼
MySQL Database
```

## Security

Sensitive credentials are stored using environment variables rather than being hardcoded into the source code.

The following files are excluded from Git:

```text
.env
__pycache__/
*.pyc
tempCodeRunnerFile.py
```

Never commit:

* MySQL passwords
* AI API keys
* Authentication tokens
* Other private credentials

## Current Status

The core MVP is functional and includes:

* PDF resume upload
* Job description input
* AI-powered resume analysis
* Fit scoring
* Skills and strengths analysis
* Application decision
* Application tracking
* MySQL storage

The frontend can be published through Replit. During development, the FastAPI backend is exposed through ngrok.

## Future Improvements

Possible future improvements include:

* Cloud deployment of the FastAPI backend
* Cloud-hosted MySQL database
* Permanent backend URL
* Authentication and user accounts
* Application dashboard
* Application status tracking
* Search and filtering
* Application statistics
* Automated job discovery
* Email or notification reminders
* Improved resume-job matching

## Author

**Krish Dewangan**

Built as a practical project to explore:

* AI automation
* FastAPI
* REST APIs
* React
* LLM integration
* MySQL
* Full-stack application development
