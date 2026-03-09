# 🚀 NovHire — AI-Powered Hiring & Onboarding

Built for the Amazon Nova AI Hackathon.

## Features
- 📄 AI Resume Screener — score, rank and analyze candidates
- 🎯 Onboarding Plan Generator — personalized 30-day plans
- ✉️ Email Drafter — auto-generate HR emails

## Tech Stack
- **AI:** Amazon Nova Lite (via AWS Bedrock)
- **Backend:** Python, FastAPI
- **Frontend:** React

## Setup
### Backend
cd backend
pip install fastapi uvicorn python-multipart pypdf2 boto3
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm start
```

---

## Step 3: Initialize Git
In Terminal 2, navigate to your `novhire` folder and run these one by one:
```
cd D:\novhire
git init
git add .
git commit -m "Initial commit - NovHire AI Hiring Agent"