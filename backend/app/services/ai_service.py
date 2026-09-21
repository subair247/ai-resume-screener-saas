import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_interview_questions(job_description: str, resume_text: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    Based on the following Job Description and Candidate Resume, generate 5 targeted technical interview questions.
    
    Job Description:
    {job_description}
    
    Candidate Resume:
    {resume_text}
    
    Provide the questions clearly in a bulleted list.
    """
    
    response = model.generate_content(prompt)
    return response.text