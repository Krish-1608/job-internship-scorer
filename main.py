from fastapi import FastAPI , UploadFile ,File ,Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel
import io
import os
from openai import OpenAI
from groq import Groq
import json
import mysql.connector
from datetime import date

app = FastAPI() #creates your FastAPI application.


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password= os.getenv("MYSQL_PASSWORD"),
    database="Application_tracker"
)
cursor = db.cursor()

cursor.execute("SELECT * FROM cand_info")

for row in cursor.fetchall():
    print(row)

from pydantic import BaseModel
from datetime import date


class Application(BaseModel):
    name: str
    company: str
    application_date: date


@app.post("/applications")
def save_application(application: Application):

    cursor = db.cursor()

    query = """
        INSERT INTO cand_info (name, company, Application_date)
        VALUES (%s, %s, %s)
    """

    values = (
        application.name,
        application.company,
        application.application_date
    )

    cursor.execute(query, values)
    db.commit()

    cursor.close()

    return {
        "message": "Application saved successfully"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq()

def analyze_with_llm(resume_text, job_description):

    prompt = f"""
    Compare this resume with this job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Return ONLY valid JSON with these fields:

    {{
        "fit_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "experience_match": "",
        "education_match": "",
        "explanation": ""
    }}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are an HR professional. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return ResumeAnalysis.model_validate_json(
        response.choices[0].message.content
    )

class ResumeAnalysis(BaseModel):
    fit_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    experience_match: str
    education_match: str
    explanation: str

@app.get("/") #creates an endpoint.
def home():
    return { "message": "Job tracking API is running "}

@app.post("/analyze-resume")
async def analyse_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    pdf_bytes = await resume.read()

    reader = PdfReader(io.BytesIO(pdf_bytes))

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    analysis = analyze_with_llm(resume_text, job_description)

    return {
        "resume_filename": resume.filename,
        "fit_score": analysis.fit_score,
        "matched_skills": analysis.matched_skills,
        "missing_skills": analysis.missing_skills,
        "strengths": analysis.strengths,
        "weaknesses": analysis.weaknesses,
        "experience_match": analysis.experience_match,
        "education_match": analysis.education_match,
        "explanation": analysis.explanation
    }

