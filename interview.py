import ai_chat
import config
import re

def get_next_question(career_name, conversation_history, persona="Standard Recruiter"):
    """Retrieves the next interviewer question in the dialog sequence."""
    return ai_chat.get_next_mock_question(career_name, conversation_history, persona)

def generate_full_prep_dossier(career_name):
    """Generates 10 HR, 10 Tech, and 5 Coding questions dossier."""
    return ai_chat.generate_interview_prep(career_name)

def analyze_speech_metrics(conversation_history):
    """
    Scans candidate responses in interview transcript for filler words and counts density.
    Returns summary analytics dict.
    """
    filler_words = ["uhm", "uh", "um", "like", "actually", "basically", "so", "you know"]
    total_words = 0
    filler_details = {w: 0 for w in filler_words}
    total_fillers = 0
    
    user_answers = [entry["text"] for entry in conversation_history if entry.get("type") == "answer" or entry.get("role") == "user"]
    
    for answer in user_answers:
        words = re.findall(r'\b\w+\b', answer.lower())
        total_words += len(words)
        
        for w in filler_words:
            pattern = r'\b' + re.escape(w) + r'\b'
            count = len(re.findall(pattern, answer.lower()))
            filler_details[w] += count
            total_fillers += count

    density = round((total_fillers / total_words * 100), 1) if total_words > 0 else 0.0
    
    suggestions = ""
    if density > 8:
        suggestions = "⚠️ Your responses contain a high frequency of filler words (e.g., 'like', 'um'). Try to pause silently for a second when formulating your next sentence."
    elif density > 3:
        suggestions = "⚡ Moderate filler word usage detected. Work on slowing down slightly to structure your technical arguments cleanly."
    else:
        suggestions = "✅ Excellent! Your responses are clear, articulated, and free from excessive verbal fillers."
        
    return {
        "total_words": total_words,
        "filler_count": total_fillers,
        "filler_density": density,
        "details": {k: v for k, v in filler_details.items() if v > 0},
        "suggestions": suggestions
    }

def evaluate_interview_performance(career_name, conversation_history):
    """Evaluates the mock interview dialogue transcript and appends speech fluency metrics."""
    gemini_eval = ai_chat.evaluate_mock_interview(career_name, conversation_history)
    
    # Calculate local verbal fluency metrics
    metrics = analyze_speech_metrics(conversation_history)
    
    metrics_md = f"""
---
### 🎙️ Speech Pacing & Fluency Analysis
* **Total Words Spoken:** {metrics['total_words']}
* **Filler Words Count:** {metrics['filler_count']} (density of **{metrics['filler_density']}%**)

#### Filler Word Frequency:
"""
    if metrics['details']:
        for w, c in metrics['details'].items():
            metrics_md += f"- **\"{w}\"**: {c} time{'s' if c > 1 else ''}\n"
    else:
        metrics_md += "- *No verbal tics detected!*\n"
        
    metrics_md += f"\n**Fluency Coach Recommendation:**\n{metrics['suggestions']}\n"
    
    return gemini_eval + "\n" + metrics_md

