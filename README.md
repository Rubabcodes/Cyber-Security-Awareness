# CyberAware — Cybersecurity Awareness Portal

## About the Project

CyberAware is a cybersecurity awareness portal built with Python and FastAPI. It helps users learn essential cybersecurity practices through educational topics and quizzes.

The project covers common online security risks and provides practical tips to help users stay safer online.

## Features

- **Cybersecurity Topics:** Learn about phishing, password security, social media safety, safe internet browsing, and data privacy.
- **Interactive Quizzes:** Retrieve quiz questions for each supported topic.
- **Quiz Submission:** Submit answers and receive a score, percentage, and feedback.
- **Result Tracking:** Retrieve individual quiz results, all results, and results for a particular user.
- **Statistics:** Access quiz statistics through the API.
- **Topic Explanations:** Request explanations of cybersecurity topics.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLite
- REST API
- Swagger UI / OpenAPI documentation

## Project Structure

```text
CyberAware/
├── cyberaware_api_fixed.py
├── requirements.txt
└── README.md
```

The SQLite database is created locally by the application when required.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CyberAware
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the API server

```bash
python -m uvicorn cyberaware_api_fixed:app --reload
```

### 4. Open the API documentation

Visit:

http://127.0.0.1:8000/docs

You can explore the available endpoints and test requests through the interactive Swagger UI.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/health` | Check API health |
| GET | `/topics` | Retrieve all topics |
| GET | `/topics/{topic_id}` | Retrieve a topic |
| GET | `/quiz/{topic_id}` | Retrieve a topic quiz |
| POST | `/quiz/submit` | Submit quiz answers |
| GET | `/results` | Retrieve all results |
| GET | `/results/{result_id}` | Retrieve one result |
| GET | `/results/user/{username}` | Retrieve results by username |
| GET | `/stats` | Retrieve quiz statistics |
| POST | `/explain` | Request a topic explanation |

## Cybersecurity Topics

1. Phishing Awareness
2. Password Security
3. Social Media Safety
4. Safe Internet Browsing
5. Data Privacy

## Purpose

The purpose of CyberAware is to make cybersecurity awareness easier to understand and encourage safer online behavior through educational content and quizzes.

## Deployment

The API can be deployed to a cloud hosting service such as Render. The public API URL and interactive documentation URL should be added here after deployment.

## Project Status

The backend has
