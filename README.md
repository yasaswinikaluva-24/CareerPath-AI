# CareerPath AI - Next-Gen Career Guidance Platform

CareerPath AI is a premium, glassmorphic Streamlit application designed to help users identify target career tracks, perform detailed skill gap audits, generate structured learning roadmaps, analyze resumes, and participate in mock interviews with voice and speech features.

## 🌟 Key Features

1. **🔒 Secure Authentication**: Multi-user system with local SQLite encryption (SHA-256 password hashing) and profile persistence.
2. **🧠 Core Career Matcher**: Algorithmic assessment matching users against **20+ specialized tech careers** based on self-reported slider traits, custom subjects, work environments, math interest, and teamwork preferences.
3. **📊 Visual Dashboards**: Real-time Matplotlib-generated horizontal alignment graphs and custom polar radar charts comparing personal traits vs. target careers.
4. **💬 Stateful AI Chat Assistant**: Full multi-turn dialog history stored in SQLite. Integrated with Google Gemini 2.0 via OpenRouter, fully reading user prompts within profile context.
5. **🎙️ Web-Native Voice Support**: Native browser Speech-to-Text widget for hands-free dictation, plus automated Text-to-Speech playback for AI replies.
6. **📄 PDF Resume Auditor**: Interactive ATS parser scoring files out of 100, checking missing keywords, grammar, formatting, and suggesting role-specific projects.
7. **🎭 Mock Interview Room**: Simulates a standard 5-question recruiter chat. Speaks the interviewer queries and evaluates transcript scores (Confidence, Grammar, Tech Knowledge, Communication).
8. **📥 PDF dossiers**: Generates print-ready PDFs outlining personality traits, roadmap guides, and recommended course hyperlinks (Coursera, Udemy, freeCodeCamp, etc.) using `FPDF2`.

## 📁 Project Structure

```
career_bot/
│
├── app.py              # Main entry routing and UI widgets layout
├── database.py         # SQLite setup, profiles, histories, and credential hashing
├── career_engine.py    # Career DB definitions, matching logic, and skill gaps
├── ai_chat.py          # OpenRouter client API wrapper and conversation manager
├── dashboard.py        # Visual graphs builder (Radar chart & Bar plots)
├── utils.py            # FPDF2 reports builder, PDF text parser, and course database
├── prompts.py          # Centralized LLM prompt templates
├── styles.py           # Premium Glassmorphism CSS rules
├── requirements.txt    # Required python dependencies list
└── README.md           # Getting started guide
```

## 🚀 Getting Started

### 1. Setup Environment
Initialize virtual environment and install the required modules:

```bash
# Activate virtual environment (if not already done)
.\venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt
```

### 2. Configure Credentials
Create or check the `.env` file in the root directory and specify your OpenRouter API token:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

### 3. Run Application
Launch Streamlit using the python command:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.
Create a new profile or sign in using existing credentials to explore.
