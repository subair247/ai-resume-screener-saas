import os
from dotenv import load_dotenv

load_dotenv()

def generate_interview_questions(job_description: str, resume_text: str):
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        
    genai.configure(api_key=api_key)
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