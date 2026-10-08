import ai_chat
import prompts
import config
import utils

def analyze_resume_ats(target_career, resume_file):
    """
    Parses PDF resume, extracts text, and evaluates against target career.
    
    Returns structured markdown dictionary with ATS score, strengths, weaknesses, missing keywords, and suggestions.
    """
    resume_text = utils.extract_text_from_pdf(resume_file)
    if "Error" in resume_text or not resume_text.strip():
        return f"Error: Could not extract text from the resume. Please ensure it is a valid, uncorrupted PDF file."
        
    client = ai_chat.get_ai_client()
    user_prompt = prompts.RESUME_ANALYZER_PROMPT.format(
        target_career=target_career,
        resume_text=resume_text
    )
    
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a senior recruiter and ATS algorithm validator."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def generate_tailored_cover_letter(target_career, job_description, resume_file):
    """
    Extracts text from PDF resume and prompts Gemini to write a tailored cover letter based on target job description.
    """
    resume_text = utils.extract_text_from_pdf(resume_file)
    if "Error" in resume_text or not resume_text.strip():
        return "Error: Could not extract text from the resume. Please ensure it is a valid, uncorrupted PDF file."
        
    client = ai_chat.get_ai_client()
    prompt = f"""
    You are an expert career advisor and professional copywriter.
    Write a highly tailored, compelling, and professional cover letter (under 400 words) for a candidate applying for the role of {target_career}.
    
    Here is the Target Job Description:
    \"\"\"{job_description}\"\"\"
    
    Here is the Candidate's Resume details:
    \"\"\"{resume_text}\"\"\"
    
    The cover letter should:
    1. Align the candidate's skills and experiences from their resume to the key requirements of the job description.
    2. Highlight how they can bridge any skill gaps (showing enthusiasm and transferability).
    3. Be written in a polished, engaging tone, formatted with placeholder fields for [Recruiter Name], [Company Name], and [Date].
    
    Output ONLY the completed cover letter in clean markdown format. Do NOT wrap the output in markdown code blocks.
    """
    
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer and recruiter advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

