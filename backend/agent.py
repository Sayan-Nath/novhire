import boto3
import json
import re

client = boto3.client("bedrock-runtime", region_name="us-east-1")

def clean_json(text: str) -> dict:
    # Remove markdown code blocks if present
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            if part.startswith("json"):
                text = part[4:]
                break
            elif "{" in part:
                text = part
                break
    
    text = text.strip()
    
    # Remove trailing commas before } or ]
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    
    return json.loads(text.strip())


def screen_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an expert HR recruiter. Analyze this resume against the job description.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    
    Respond in this exact JSON format:
    {{
        "score": <number 0-100>,
        "strengths": [<list of 3 strengths>],
        "weaknesses": [<list of 2 weaknesses>],
        "recommendation": "<Shortlist / Maybe / Reject>",
        "interview_questions": [<list of 3 tailored questions>],
        "summary": "<2 sentence candidate summary>"
    }}
    
    Return ONLY the JSON, nothing else.
    """

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    
    result = response["output"]["message"]["content"][0]["text"]
    return clean_json(result)


def generate_onboarding_plan(candidate_name: str, role: str) -> dict:
    prompt = f"""
    You are an HR specialist. Create a personalized 30-day onboarding plan.
    
    New Employee: {candidate_name}
    Role: {role}
    
    Respond in this exact JSON format:
    {{
        "welcome_message": "<personalized welcome message>",
        "day_1": [<list of 3 tasks>],
        "week_1": [<list of 4 goals>],
        "month_1": [<list of 4 milestones>],
        "resources": [<list of 3 recommended resources>]
    }}
    
    Return ONLY the JSON, nothing else.
    """

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    
    result = response["output"]["message"]["content"][0]["text"]
    return clean_json(result)


def draft_email(candidate_name: str, role: str, email_type: str) -> str:
    prompt = f"""
    Write a professional HR email.
    
    Candidate: {candidate_name}
    Role: {role}
    Email type: {email_type} (can be: interview_invite, rejection, offer)
    
    Write only the email body, no subject line needed.
    Keep it professional, warm, and concise.
    """

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    
    return response["output"]["message"]["content"][0]["text"]


if __name__ == "__main__":
    result = screen_resume(
        resume_text="John Doe, 5 years Python experience, built REST APIs, led a team of 3.",
        job_description="Looking for a senior Python developer with API experience."
    )
    print(json.dumps(result, indent=2))