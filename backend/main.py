from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agent import screen_resume, generate_onboarding_plan, draft_email
import PyPDF2
import io

app = FastAPI()

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "NovHire API is running!"}

@app.post("/screen-resume")
async def screen_resume_endpoint(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    # Extract text from PDF
    contents = await resume_file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    result = screen_resume(resume_text, job_description)
    return result

@app.post("/onboarding")
async def onboarding_endpoint(
    candidate_name: str = Form(...),
    role: str = Form(...)
):
    result = generate_onboarding_plan(candidate_name, role)
    return result

@app.post("/draft-email")
async def draft_email_endpoint(
    candidate_name: str = Form(...),
    role: str = Form(...),
    email_type: str = Form(...)
):
    result = draft_email(candidate_name, role, email_type)
    return {"email": result}