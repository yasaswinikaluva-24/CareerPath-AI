from openai import OpenAI
import os
import database
import prompts
import config

api_key = config.OPENROUTER_API_KEY
MODEL_NAME = config.MODEL_NAME

def get_ai_client():
    """Initializes and returns the OpenRouter OpenAI client."""
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured in the environment.")
    return OpenAI(
        api_key=api_key,
        base_url=config.OPENROUTER_BASE_URL
    )

def generate_chat_response(username, user_message, chat_history, profile_context):
    """
    Generates a chat response using OpenRouter and saves history.
    profile_context should be a dict: {name, logic, creativity, communication, skills, recommended_career, match_percentage}
    """
    client = get_ai_client()
    
    # 1. Format system prompt
    sys_prompt = prompts.CHAT_SYSTEM_PROMPT.format(
        name=profile_context.get("name", "User"),
        logic=profile_context.get("logic", 5),
        creativity=profile_context.get("creativity", 5),
        communication=profile_context.get("communication", 5),
        skills=profile_context.get("skills", ""),
        recommended_career=profile_context.get("recommended_career", "Not Determined Yet"),
        match_percentage=profile_context.get("match_percentage", 0)
    )
    
    # 2. Build message log
    messages = [{"role": "system", "content": sys_prompt}]
    
    # Add historical messages (limit to last 10 messages to keep within context budgets)
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Append the new user message
    # Improve 1: Incorporate the actual user's message alongside context
    full_user_content = f"""
User Message:
{user_message}

Personality Profile:
Logic Score: {profile_context.get('logic', 5)}/10
Creativity Score: {profile_context.get('creativity', 5)}/10
Communication Score: {profile_context.get('communication', 5)}/10
Skills entered: {profile_context.get('skills', '')}
Recommended Career: {profile_context.get('recommended_career', 'None')}

Please reply to the user's message while keeping their context in mind.
"""
    messages.append({"role": "user", "content": full_user_content})
    
    # 3. Call OpenRouter API
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.6
    )
    
    reply = response.choices[0].message.content
    
    # 4. Save to SQLite
    database.save_chat_message(username, "user", user_message)
    database.save_chat_message(username, "assistant", reply)
    
    return reply

def generate_roadmap(career_name, already_have, need_to_learn):
    """Call LLM to construct 30-day learning roadmap for missing skills."""
    client = get_ai_client()
    user_prompt = prompts.ROADMAP_PROMPT.format(
        career_name=career_name,
        already_have=", ".join(already_have) if already_have else "None",
        need_to_learn=", ".join(need_to_learn) if need_to_learn else "None"
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional curriculum designer."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def analyze_resume(target_career, resume_text):
    """Analyzes resume text against target career using LLM."""
    client = get_ai_client()
    user_prompt = prompts.RESUME_ANALYZER_PROMPT.format(
        target_career=target_career,
        resume_text=resume_text
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert ATS recruiter."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def get_next_mock_question(career_name, conversation_history, persona="Standard Recruiter"):
    """Generates the next question for a mock interview based on selected interviewer persona."""
    client = get_ai_client()
    
    persona_instructions = {
        "Strict Tech Lead": "You are a demanding, details-oriented Technical Lead. You care deeply about system design, code optimization, robust logic, algorithms, and deep technical details. Ask challenging, direct technical questions. No generic HR fluff.",
        "Friendly HR Recruiter": "You are a warm, welcoming, but observant HR Specialist. Focus heavily on behavioral questions, STAR method scenarios, team conflict resolution, work culture, and interpersonal skills.",
        "Fast-Paced Startup Founder": "You are a high-energy, fast-moving Startup Founder. Focus on adaptability, speed, wearing multiple hats, working under high pressure, understanding business impact, and general product ownership."
    }
    
    selected_instruction = persona_instructions.get(persona, "You are a professional hiring manager interviewing a candidate.")
    
    system_content = f"""{selected_instruction}
You are interviewing a candidate for the role of {career_name}.
Keep questions realistic, targeted, and brief. Ask exactly one question at a time.
Do NOT output anything else except the question itself.
"""
    
    messages = [
        {"role": "system", "content": system_content}
    ]
    
    # Add interview history
    for entry in conversation_history:
        messages.append({"role": "assistant" if entry["type"] == "question" else "user", "content": entry["text"]})
        
    messages.append({"role": "user", "content": "Please ask the next interview question."})
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content


def evaluate_mock_interview(career_name, conversation_history):
    """Evaluates the mock interview transcript and yields a score report."""
    client = get_ai_client()
    
    log_text = ""
    for entry in conversation_history:
        role = "Interviewer" if entry["type"] == "question" else "Candidate"
        log_text += f"{role}: {entry['text']}\n\n"
        
    user_prompt = prompts.MOCK_INTERVIEW_EVAL_PROMPT.format(
        career_name=career_name,
        conversation_log=log_text
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR evaluator and technical recruiter."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def generate_interview_prep(career_name):
    """Generates 10 HR, 10 Tech, and 5 Coding questions/answers dossier."""
    client = get_ai_client()
    user_prompt = prompts.INTERVIEW_PREP_PROMPT.format(career_name=career_name)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
