#!/usr/bin/env python
# coding: utf-8

# In[4]:


from datetime import datetime
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# -----------------------------
# APP CONFIGURATION
# -----------------------------

app = FastAPI(
    title="CyberAware API",
    description="Cybersecurity awareness topics, quizzes, and results",
    version="1.0.0",
)

# For local testing. Restrict this to your website's origin
# before deploying the API publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_PATH = Path("cyberaware.db").resolve()


# -----------------------------
# DATABASE
# -----------------------------

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                topic TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                submitted_at TEXT NOT NULL
            )
        """)


initialize_database()


# -----------------------------
# CYBERSECURITY TOPICS
# -----------------------------

TOPICS = {
    "phishing": {
        "title": "Phishing Awareness",
        "description": (
            "Learn to identify suspicious emails, messages, "
            "fake links, and online scams."
        ),
        "tips": [
            "Check the sender's email address carefully.",
            "Avoid clicking suspicious links.",
            "Never share passwords or OTP codes.",
            "Verify unexpected messages through an official channel.",
        ],
    },
    "password_security": {
        "title": "Password Security",
        "description": (
            "Learn how to create and protect strong passwords."
        ),
        "tips": [
            "Use a long, unique password for each account.",
            "Never share your password with others.",
            "Enable multi-factor authentication when available.",
            "Use a reputable password manager if possible.",
        ],
    },
    "social_media": {
        "title": "Social Media Safety",
        "description": (
            "Protect your privacy and identity on social media."
        ),
        "tips": [
            "Avoid publicly sharing private information.",
            "Review your account privacy settings.",
            "Do not accept suspicious friend requests.",
            "Report abusive or fraudulent accounts.",
        ],
    },
    "safe_browsing": {
        "title": "Safe Internet Browsing",
        "description": (
            "Learn safer habits when visiting websites and "
            "downloading files."
        ),
        "tips": [
            "Check website addresses before entering information.",
            "Download files from trusted sources.",
            "Keep your browser and operating system updated.",
            "Avoid entering sensitive data on suspicious websites.",
        ],
    },
    "data_privacy": {
        "title": "Data Privacy",
        "description": (
            "Understand how to protect personal and sensitive data."
        ),
        "tips": [
            "Share personal information only when necessary.",
            "Review app permissions before granting access.",
            "Lock your devices when not using them.",
            "Back up important files securely.",
        ],
    },
}


# -----------------------------
# QUIZ QUESTIONS
# Correct answers are kept on the server.
# -----------------------------

QUIZZES = {
    "phishing": [
        {
            "question": "You receive a suspicious email asking for your password. What should you do?",
            "options": [
                "Reply with your password",
                "Click every link in the email",
                "Avoid the links and verify the sender",
                "Forward your password to a friend",
            ],
            "answer": 2,
            "explanation": (
                "Never share your password. Verify suspicious "
                "messages through an official channel."
            ),
        },
        {
            "question": "What is phishing?",
            "options": [
                "A computer cleaning method",
                "A trick used to steal sensitive information",
                "A type of keyboard",
                "A safe backup method",
            ],
            "answer": 1,
            "explanation": (
                "Phishing uses deceptive messages or websites "
                "to steal information."
            ),
        },
        {
            "question": "A message asks you to enter an OTP urgently. What is safest?",
            "options": [
                "Share it immediately",
                "Post it online",
                "Ignore all security warnings",
                "Never share it and verify the request",
            ],
            "answer": 3,
            "explanation": (
                "An OTP is a security code and should not be "
                "shared with another person."
            ),
        },
    ],
    "password_security": [
        {
            "question": "Which password practice is safest?",
            "options": [
                "Use your name for every account",
                "Use a unique, long password for each account",
                "Share your password with friends",
                "Write your password in a public post",
            ],
            "answer": 1,
            "explanation": (
                "Unique, long passwords reduce the risk of one "
                "compromised account affecting other accounts."
            ),
        },
        {
            "question": "What does multi-factor authentication do?",
            "options": [
                "Adds another verification step",
                "Removes every password",
                "Makes public Wi-Fi private",
                "Deletes your account",
            ],
            "answer": 0,
            "explanation": (
                "Multi-factor authentication adds another way "
                "to verify your identity."
            ),
        },
        {
            "question": "Should you reuse the same password everywhere?",
            "options": [
                "Yes, always",
                "Only on public computers",
                "No, use unique passwords",
                "Only for banking accounts",
            ],
            "answer": 2,
            "explanation": (
                "If one account is compromised, reused passwords "
                "can put other accounts at risk."
            ),
        },
    ],
    "social_media": [
        {
            "question": "What should you do before accepting a suspicious friend request?",
            "options": [
                "Send your home address",
                "Verify the account",
                "Share your password",
                "Send a security code",
            ],
            "answer": 1,
            "explanation": (
                "Verify unfamiliar accounts before trusting them "
                "or sharing information."
            ),
        },
        {
            "question": "Which information should you avoid posting publicly?",
            "options": [
                "A general hobby",
                "A public-interest article",
                "Your private address and sensitive details",
                "A public event announcement",
            ],
            "answer": 2,
            "explanation": (
                "Publicly sharing sensitive information can "
                "increase privacy and safety risks."
            ),
        },
        {
            "question": "What should you do with an account sending scams?",
            "options": [
                "Send it money",
                "Share its links",
                "Give it your OTP",
                "Report and block it",
            ],
            "answer": 3,
            "explanation": (
                "Reporting and blocking suspicious accounts "
                "helps protect you and others."
            ),
        },
    ],
    "safe_browsing": [
        {
            "question": "What should you do before downloading an unknown file?",
            "options": [
                "Check the source and whether it is trustworthy",
                "Disable all security tools",
                "Share your password first",
                "Download every file you see",
            ],
            "answer": 0,
            "explanation": (
                "Untrusted downloads may contain malware or "
                "other harmful content."
            ),
        },
        {
            "question": "A website address looks suspicious. What should you do?",
            "options": [
                "Enter your banking details",
                "Avoid the site and verify the correct address",
                "Download its files",
                "Ignore browser warnings",
            ],
            "answer": 1,
            "explanation": (
                "Suspicious addresses can lead to fraudulent "
                "or harmful websites."
            ),
        },
        {
            "question": "Why should software be updated?",
            "options": [
                "Updates always remove your files",
                "Updates share your password",
                "Updates can fix security vulnerabilities",
                "Updates make scams impossible",
            ],
            "answer": 2,
            "explanation": (
                "Security updates often fix weaknesses that "
                "attackers could exploit."
            ),
        },
    ],
    "data_privacy": [
        {
            "question": "What is the safest approach to app permissions?",
            "options": [
                "Allow every permission automatically",
                "Share all contacts with every app",
                "Ignore permission requests",
                "Allow only permissions that are necessary",
            ],
            "answer": 3,
            "explanation": (
                "Review permissions and grant only what an app "
                "reasonably needs."
            ),
        },
        {
            "question": "What should you do when leaving your computer unattended?",
            "options": [
                "Lock the screen",
                "Leave sensitive files open",
                "Share your login",
                "Disable the password",
            ],
            "answer": 0,
            "explanation": (
                "Locking your screen helps prevent unauthorized "
                "access to your device."
            ),
        },
        {
            "question": "How should you protect important files?",
            "options": [
                "Publish every file online",
                "Keep secure backups",
                "Share them with strangers",
                "Use the same public link for everything",
            ],
            "answer": 1,
            "explanation": (
                "Secure backups help you recover important data "
                "if files are lost or damaged."
            ),
        },
    ],
}


# -----------------------------
# REQUEST MODELS
# -----------------------------

class QuizSubmission(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    topic: str = Field(min_length=1, max_length=50)
    answers: list[int] = Field(min_length=1, max_length=50)


# -----------------------------
# BASIC ENDPOINTS
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "CyberAware API is running!",
        "project": "Cybersecurity Awareness Portal",
        "docs": "/docs",
        "topics_endpoint": "/topics",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -----------------------------
# TOPIC ENDPOINTS
# -----------------------------

@app.get("/topics")
def get_topics():
    return [
        {
            "id": topic_id,
            **topic_data,
        }
        for topic_id, topic_data in TOPICS.items()
    ]


@app.get("/topics/{topic_id}")
def get_topic(topic_id: str):
    topic = TOPICS.get(topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return {
        "id": topic_id,
        **topic,
    }


# -----------------------------
# QUIZ ENDPOINTS
# -----------------------------

@app.get("/quiz/{topic_id}")
def get_quiz(topic_id: str):
    questions = QUIZZES.get(topic_id)

    if questions is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found for this topic",
        )

    # Do not send correct answers to the browser.
    return {
        "topic": topic_id,
        "total_questions": len(questions),
        "questions": [
            {
                "question": item["question"],
                "options": item["options"],
            }
            for item in questions
        ],
    }


@app.post("/quiz/submit")
def submit_quiz(submission: QuizSubmission):
    username = submission.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty",
        )

    questions = QUIZZES.get(submission.topic)

    if questions is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found for this topic",
        )

    if len(submission.answers) != len(questions):
        raise HTTPException(
            status_code=400,
            detail=f"Please submit exactly {len(questions)} answers",
        )

    for answer in submission.answers:
        if answer < 0 or answer >= 4:
            raise HTTPException(
                status_code=400,
                detail="Each answer must be an option index from 0 to 3",
            )

    score = sum(
        1
        for question, answer in zip(questions, submission.answers)
        if question["answer"] == answer
    )

    total = len(questions)
    percentage = round((score / total) * 100, 2)
    submitted_at = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO quiz_results (
                username,
                topic,
                score,
                total_questions,
                percentage,
                submitted_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                submission.topic,
                score,
                total,
                percentage,
                submitted_at,
            ),
        )

        result_id = cursor.lastrowid

    feedback = (
        "Excellent work!"
        if percentage >= 80
        else "Good effort! Keep learning."
        if percentage >= 50
        else "Keep practising your cybersecurity skills."
    )

    return {
        "result_id": result_id,
        "username": username,
        "topic": submission.topic,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "feedback": feedback,
        "submitted_at": submitted_at,
    }


# -----------------------------
# RESULT ENDPOINTS
# -----------------------------

@app.get("/results")
def get_all_results():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, username, topic, score,
                   total_questions, percentage, submitted_at
            FROM quiz_results
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


@app.get("/results/{result_id}")
def get_result(result_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, username, topic, score,
                   total_questions, percentage, submitted_at
            FROM quiz_results
            WHERE id = ?
            """,
            (result_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found",
        )

    return dict(row)


@app.get("/results/user/{username}")
def get_user_results(username: str):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, username, topic, score,
                   total_questions, percentage, submitted_at
            FROM quiz_results
            WHERE username = ? COLLATE NOCASE
            ORDER BY id DESC
            """,
            (username.strip(),),
        ).fetchall()

    return [dict(row) for row in rows]


# -----------------------------
# STATISTICS ENDPOINT
# -----------------------------

@app.get("/stats")
def get_statistics():
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_attempts,
                COUNT(DISTINCT username) AS unique_users,
                AVG(percentage) AS average_percentage
            FROM quiz_results
            """
        ).fetchone()

    return {
        "total_attempts": row["total_attempts"],
        "unique_users": row["unique_users"],
        "average_percentage": round(
            row["average_percentage"] or 0, 2
        ),
    }


# -----------------------------
# OPTIONAL AI-STYLE EXPLANATION
# This is rule-based, NOT a real AI model.
# -----------------------------

class ExplanationRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=50)
    question: str = Field(min_length=1, max_length=500)


@app.post("/explain")
def explain_topic(request: ExplanationRequest):
    topic = TOPICS.get(request.topic)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return {
        "topic": topic["title"],
        "question": request.question,
        "explanation": (
            f"{topic['description']} "
            "For safer online behaviour: "
            + " ".join(topic["tips"])
        ),
        "notice": (
            "This is a predefined educational explanation, "
            "not a response generated by an AI model."
        ),
    }


# Run using:
# python -m uvicorn cyberaware_api_fixed:app --reload


# In[ ]:




