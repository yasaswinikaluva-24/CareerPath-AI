import pypdf
from fpdf import FPDF
import datetime

COURSES_DB = {
    "python": [
        {"platform": "Coursera", "title": "Python for Everybody Specialization", "link": "https://www.coursera.org/specializations/python"},
        {"platform": "freeCodeCamp", "title": "Python for Beginners (Full Course)", "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
        {"platform": "Udemy", "title": "2026 Complete Python Bootcamp", "link": "https://www.udemy.com/course/complete-python-bootcamp/"}
    ],
    "machine learning": [
        {"platform": "Coursera", "title": "Machine Learning Specialization (Andrew Ng)", "link": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"platform": "YouTube", "title": "StatQuest: Machine Learning Video Series", "link": "https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF"},
        {"platform": "freeCodeCamp", "title": "Machine Learning for Beginners", "link": "https://www.youtube.com/watch?v=NWONeJKn0Oc"}
    ],
    "deep learning": [
        {"platform": "Coursera", "title": "Deep Learning Specialization (deeplearning.ai)", "link": "https://www.coursera.org/specializations/deep-learning"},
        {"platform": "freeCodeCamp", "title": "PyTorch for Deep Learning Boot Camp", "link": "https://www.youtube.com/watch?v=V_xro1bcAuA"}
    ],
    "tensorflow": [
        {"platform": "Coursera", "title": "DeepLearning.AI TensorFlow Developer Professional Certificate", "link": "https://www.coursera.org/professional-certificates/tensorflow-in-practice"}
    ],
    "pytorch": [
        {"platform": "Udemy", "title": "PyTorch for Deep Learning with Bootcamp", "link": "https://www.udemy.com/course/pytorch-for-deep-learning/"}
    ],
    "nlp": [
        {"platform": "Coursera", "title": "Natural Language Processing Specialization", "link": "https://www.coursera.org/specializations/natural-language-processing"}
    ],
    "statistics": [
        {"platform": "Khan Academy", "title": "College Statistics Course (Free)", "link": "https://www.khanacademy.org/math/statistics-probability"},
        {"platform": "Coursera", "title": "Statistics with Python Specialization", "link": "https://www.coursera.org/specializations/statistics-with-python"}
    ],
    "sql": [
        {"platform": "freeCodeCamp", "title": "SQL Tutorial for Beginners", "link": "https://www.youtube.com/watch?v=HXV3zeQKqGY"},
        {"platform": "Udemy", "title": "The Complete SQL Bootcamp", "link": "https://www.udemy.com/course/the-complete-sql-bootcamp/"}
    ],
    "html": [
        {"platform": "freeCodeCamp", "title": "HTML & CSS Tutorial for Beginners", "link": "https://www.youtube.com/watch?v=mU6anWqRxRo"},
        {"platform": "W3Schools", "title": "HTML Tutorial", "link": "https://www.w3schools.com/html/"}
    ],
    "css": [
        {"platform": "YouTube", "title": "CSS Grid & Flexbox Crash Course", "link": "https://www.youtube.com/watch?v=jV8B24rSN5o"}
    ],
    "javascript": [
        {"platform": "freeCodeCamp", "title": "JavaScript Algorithms and Data Structures", "link": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"},
        {"platform": "Udemy", "title": "The Complete JavaScript Course", "link": "https://www.udemy.com/course/the-complete-javascript-course-2016/"}
    ],
    "react": [
        {"platform": "Udemy", "title": "React - The Complete Guide (incl Hooks, React Router, Redux)", "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
        {"platform": "freeCodeCamp", "title": "React JS Full Course for Beginners", "link": "https://www.youtube.com/watch?v=bMknfKXIFA8"}
    ],
    "networking": [
        {"platform": "YouTube", "title": "Computer Networking Course - Network+ Exam Prep", "link": "https://www.youtube.com/watch?v=qiQR5rTSshw"},
        {"platform": "Coursera", "title": "The Bits and Bytes of Networking", "link": "https://www.coursera.org/learn/computer-networking"}
    ],
    "linux": [
        {"platform": "freeCodeCamp", "title": "Linux Operating System for Beginners", "link": "https://www.youtube.com/watch?v=wBp0Rb-CNW0"},
        {"platform": "Coursera", "title": "Google IT Support - Linux Tools", "link": "https://www.coursera.org/learn/linux-system-administration"}
    ],
    "cryptography": [
        {"platform": "Coursera", "title": "Cryptography I (Stanford)", "link": "https://www.coursera.org/learn/crypto"}
    ],
    "aws": [
        {"platform": "freeCodeCamp", "title": "AWS Certified Cloud Practitioner Training", "link": "https://www.youtube.com/watch?v=SOTamWGuDKc"},
        {"platform": "Udemy", "title": "Ultimate AWS Certified Cloud Practitioner", "link": "https://www.udemy.com/course/aws-certified-cloud-practitioner-new/"}
    ],
    "docker": [
        {"platform": "YouTube", "title": "Docker Tutorial for Beginners", "link": "https://www.youtube.com/watch?v=3c-iM_IBg-s"}
    ],
    "kubernetes": [
        {"platform": "freeCodeCamp", "title": "Kubernetes Course for Beginners", "link": "https://www.youtube.com/watch?v=VnvRFRk_51k"}
    ],
    "figma": [
        {"platform": "YouTube", "title": "Figma UI/UX Design Tutorial", "link": "https://www.youtube.com/watch?v=FTFaQW1ZgQk"},
        {"platform": "Coursera", "title": "Google UX Design Professional Certificate", "link": "https://www.coursera.org/professional-certificates/google-ux-design"}
    ],
    "git": [
        {"platform": "freeCodeCamp", "title": "Git and GitHub for Beginners", "link": "https://www.youtube.com/watch?v=RGOj5yH7evk"}
    ]
}

CAREER_QUOTES = [
    {"quote": "The best way to predict your future is to create it.", "author": "Abraham Lincoln"},
    {"quote": "Dream, dream, dream. Dreams transform into thoughts and thoughts result in action.", "author": "Dr. A.P.J. Abdul Kalam"},
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "Arise, awake, and stop not till the goal is reached.", "author": "Swami Vivekananda"},
    {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
    {"quote": "Cultivate your mind with great thoughts, for you will never go any higher than you think.", "author": "Dr. B.R. Ambedkar"},
    {"quote": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi"},
    {"quote": "It always seems impossible until it is done.", "author": "Nelson Mandela"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt"},
    {"quote": "Opportunities don't happen. You create them.", "author": "Chris Grosser"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "Your passion is waiting for your courage to catch up.", "author": "Isabelle Lafleche"},
    {"quote": "Continuous learning is the minimum requirement for success in any field.", "author": "Brian Tracy"},
    {"quote": "You don't have to be great to start, but you have to start to be great.", "author": "Zig Ziglar"},
    {"quote": "The expert in anything was once a beginner.", "author": "Helen Hayes"},
    {"quote": "Action is the foundational key to all success.", "author": "Pablo Picasso"},
    {"quote": "Success usually comes to those who are too busy to be looking for it.", "author": "Henry David Thoreau"},
    {"quote": "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.", "author": "Roy T. Bennett"}
]

def get_quote_for_user(username, offset=0):
    """Deterministically picks a distinct quote based on the user's username, with an offset for rotating quotes."""
    if not username:
        username = "guest"
    user_hash = sum(ord(c) for c in username)
    idx = (user_hash + offset) % len(CAREER_QUOTES)
    return CAREER_QUOTES[idx]

CAREER_COURSES = {
    "AI Engineer": [
        {"title": "Machine Learning Specialization", "instructor": "by Andrew Ng • Coursera", "link": "https://www.coursera.org/specializations/machine-learning-introduction", "platform": "Coursera"},
        {"title": "Deep Learning A-Z™", "instructor": "by Kirill Eremenko • Udemy", "link": "https://www.udemy.com/course/deeplearning/", "platform": "Udemy"},
        {"title": "Python for Data Science", "instructor": "by IBM • Coursera", "link": "https://www.coursera.org/learn/python-for-applied-data-science-ai", "platform": "Coursera"}
    ],
    "Data Scientist": [
        {"title": "IBM Data Science Professional Certificate", "instructor": "by IBM • Coursera", "link": "https://www.coursera.org/professional-certificates/ibm-data-science", "platform": "Coursera"},
        {"title": "The Data Science Course: Complete Bootcamp", "instructor": "by 365 Careers • Udemy", "link": "https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/", "platform": "Udemy"},
        {"title": "Applied Data Science with Python", "instructor": "by Univ of Michigan • Coursera", "link": "https://www.coursera.org/specializations/data-science-python", "platform": "Coursera"}
    ],
    "Full Stack Developer": [
        {"title": "Meta Front-End & Back-End Developer", "instructor": "by Meta • Coursera", "link": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "platform": "Coursera"},
        {"title": "The Complete 2024 Web Development Bootcamp", "instructor": "by Angela Yu • Udemy", "link": "https://www.udemy.com/course/the-complete-web-development-bootcamp/", "platform": "Udemy"},
        {"title": "Full Stack Open (React, Node, GraphQL)", "instructor": "by Univ of Helsinki", "link": "https://fullstackopen.com/en/", "platform": "Free"}
    ],
    "Cloud Solutions Architect": [
        {"title": "AWS Certified Solutions Architect", "instructor": "by Stéphane Maarek • Udemy", "link": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "platform": "Udemy"},
        {"title": "Architecting with Google Cloud", "instructor": "by Google Cloud • Coursera", "link": "https://www.coursera.org/specializations/gcp-architecture", "platform": "Coursera"},
        {"title": "Microsoft Azure Fundamentals (AZ-900)", "instructor": "by Microsoft Learn", "link": "https://learn.microsoft.com/en-us/training/courses/az-900t00", "platform": "Microsoft"}
    ],
    "Cybersecurity Analyst": [
        {"title": "Google Cybersecurity Professional Certificate", "instructor": "by Google • Coursera", "link": "https://www.coursera.org/professional-certificates/google-cybersecurity", "platform": "Coursera"},
        {"title": "The Complete Cyber Security Course", "instructor": "by Nathan House • Udemy", "link": "https://www.udemy.com/course/the-complete-internet-security-privacy-course-volume-1/", "platform": "Udemy"},
        {"title": "CompTIA Security+ Exam Prep", "instructor": "by Jason Dion • Udemy", "link": "https://www.udemy.com/course/securityplus/", "platform": "Udemy"}
    ],
    "DevOps Engineer": [
        {"title": "Docker & Kubernetes: The Practical Guide", "instructor": "by Maximilian Schwarzmüller • Udemy", "link": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/", "platform": "Udemy"},
        {"title": "IBM DevOps and Software Engineering", "instructor": "by IBM • Coursera", "link": "https://www.coursera.org/professional-certificates/devops-and-software-engineering", "platform": "Coursera"},
        {"title": "GitLab CI: Pipelines, CI/CD and DevOps", "instructor": "by Valentin Despa • Udemy", "link": "https://www.udemy.com/course/gitlab-ci-pipelines-ci-cd-and-devops-for-beginners/", "platform": "Udemy"}
    ],
    "UI/UX Designer": [
        {"title": "Google UX Design Professional Certificate", "instructor": "by Google • Coursera", "link": "https://www.coursera.org/professional-certificates/google-ux-design", "platform": "Coursera"},
        {"title": "Figma UI UX Design Essentials", "instructor": "by Daniel Walter Scott • Udemy", "link": "https://www.udemy.com/course/figma-ux-ui-design-user-experience-tutorial-course/", "platform": "Udemy"},
        {"title": "Interaction Design Specialization", "instructor": "by UC San Diego • Coursera", "link": "https://www.coursera.org/specializations/interaction-design", "platform": "Coursera"}
    ],
    "Product Manager": [
        {"title": "Become a Product Manager | Learn the Skills", "instructor": "by Cole Mercer • Udemy", "link": "https://www.udemy.com/course/become-a-product-manager-learn-the-skills-get-a-job/", "platform": "Udemy"},
        {"title": "Digital Product Management: Modern Fundamentals", "instructor": "by Univ of Virginia • Coursera", "link": "https://www.coursera.org/learn/uva-darden-digital-product-management", "platform": "Coursera"},
        {"title": "Google Project Management Certificate", "instructor": "by Google • Coursera", "link": "https://www.coursera.org/professional-certificates/google-project-management", "platform": "Coursera"}
    ]
}

def get_recommended_courses_for_career(career_name="AI Engineer"):
    """Returns curated clickable courses for a given career track with fallback."""
    if career_name in CAREER_COURSES:
        return CAREER_COURSES[career_name]
    for k, v in CAREER_COURSES.items():
        if k.lower() in career_name.lower() or career_name.lower() in k.lower():
            return v
    return CAREER_COURSES["AI Engineer"]

def extract_text_from_pdf(pdf_file):
    """Extract text contents from an uploaded PDF file with layout preservation."""
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            try:
                # Try layout-aware extraction to preserve multi-column formatting
                t = page.extract_text(extraction_mode="layout")
            except Exception:
                # Fallback to simple extraction if layout mode is not supported by installed pypdf version
                t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def clean_unicode(text):
    """Clean emojis and special characters for standard PDF compatibility."""
    if not text:
        return ""
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "*",
        "\u2705": "[x]",
        "\u274c": "[ ]",
        "\u26a1": "[!]",
        "\u2611": "[x]",
        "\u2192": "->",
        "\u2026": "..."
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def get_recommendations_for_skills(need_to_learn):
    """Retrieve standard courses for list of skills user needs to learn."""
    recommendations = {}
    for skill in need_to_learn:
        skill_lower = skill.lower()
        # Direct lookup
        if skill_lower in COURSES_DB:
            recommendations[skill] = COURSES_DB[skill_lower]
        else:
            # Fuzzy match
            found = False
            for db_key, val in COURSES_DB.items():
                if db_key in skill_lower or skill_lower in db_key:
                    recommendations[skill] = val
                    found = True
                    break
            if not found:
                # Default generic Coursera/Udemy search link
                recommendations[skill] = [
                    {"platform": "Coursera Search", "title": f"Search for {skill} courses", "link": f"https://www.coursera.org/search?query={skill}"},
                    {"platform": "Udemy Search", "title": f"Search for {skill} tutorials", "link": f"https://www.udemy.com/courses/search/?q={skill}"}
                ]
    return recommendations

class CareerReportPDF(FPDF):
    def header(self):
        self.set_fill_color(11, 15, 25) # Deep navy background tint
        self.rect(0, 0, 210, 297, 'F') # Optional subtle page boundary background
        
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(59, 130, 246) # Blue text
        self.cell(0, 10, "CAREERPATH AI - CAREER ASSESSMENT PORTFOLIO", 0, 1, "C")
        
        # Border line
        self.set_draw_color(147, 51, 234) # Purple line
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(156, 163, 175)
        self.line(10, 280, 200, 280)
        self.cell(0, 10, f"Generated by CareerPath AI on {datetime.date.today().strftime('%Y-%m-%d')} | Page {self.page_no()}", 0, 0, "C")

def generate_career_pdf_report(name, logic, creativity, communication, skills, top_career, match_pct, skill_gap, roadmap, courses):
    """
    Creates a beautiful PDF report for the user containing:
    - Profile Overview
    - Top Recommendation Details
    - Skill Gap (Already Have, Need to Learn)
    - 30-Day Learning Roadmap
    - Recommended Courses
    """
    pdf = CareerReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Title Section
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"Career Assessment Dossier: {clean_unicode(name)}", 0, 1, "L")
    pdf.ln(5)
    
    # 1. Profile Traits
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(96, 165, 250)
    pdf.cell(0, 8, "1. PERSONALITY TRAIT SCORES", 0, 1, "L")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.cell(50, 6, f"Logical Thinking: {logic}/10", 0, 0)
    pdf.cell(50, 6, f"Creativity: {creativity}/10", 0, 0)
    pdf.cell(50, 6, f"Communication: {communication}/10", 0, 1)
    
    pdf.cell(0, 6, f"Current Skills: {clean_unicode(skills)}", 0, 1)
    pdf.ln(8)
    
    # 2. Recommendation Detail
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(167, 139, 250)
    pdf.cell(0, 8, "2. CAREER MATCH RECOMMENDATION", 0, 1, "L")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, f"Recommended Track: {clean_unicode(top_career)} (Match Score: {match_pct}%)", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.cell(0, 6, f"Estimated Starting Salary: {top_career} benchmark ranges around {top_career}.", 0, 1)
    pdf.ln(8)
    
    # 3. Skill Gap Analysis
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(244, 114, 182)
    pdf.cell(0, 8, "3. SKILL GAP ANALYSIS", 0, 1, "L")
    
    already = skill_gap.get("already_have", [])
    need = skill_gap.get("need_to_learn", [])
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 6, "Skills You Already Have:", 0, 1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.multi_cell(0, 5, ", ".join(already) if already else "None detected. Enter more skills in your profile.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(239, 68, 68)
    pdf.cell(0, 6, "Skills You Need To Learn:", 0, 1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.multi_cell(0, 5, ", ".join(need) if need else "You already possess all the primary skills for this role!")
    pdf.ln(8)
    
    # 4. Learning Roadmap
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(96, 165, 250)
    pdf.cell(0, 8, "4. 30-DAY LEARNING ROADMAP", 0, 1, "L")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(243, 244, 246)
    
    import roadmap as rm_module
    formatted_roadmap = rm_module.format_roadmap_for_text(roadmap)
    cleaned_roadmap = clean_unicode(formatted_roadmap)
    pdf.multi_cell(0, 5, cleaned_roadmap)
    pdf.ln(8)
    
    # 5. Course Recommendations
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(167, 139, 250)
    pdf.cell(0, 8, "5. RECOMMENDED ONLINE COURSES", 0, 1, "L")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(243, 244, 246)
    
    # Get course links
    rec_courses = get_recommendations_for_skills(need)
    if rec_courses:
        for skill_item, course_list in rec_courses.items():
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 6, f"* {clean_unicode(skill_item)}:", 0, 1)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(156, 163, 175)
            for crs in course_list:
                pdf.cell(10, 5, "", 0, 0)
                pdf.cell(0, 5, f"- [{clean_unicode(crs['platform'])}] {clean_unicode(crs['title'])}", 0, 1)
            pdf.ln(2)
    else:
        pdf.cell(0, 5, "No pending skills to display recommended courses for.", 0, 1)
        
    return pdf.output()

def fetch_ai_job_listings(career_name):
    """
    Queries Gemini to generate realistic job and internship listings for the selected career track.
    Includes both Full-Time jobs and Internships (tailored for Internshala and LinkedIn).
    Returns list of opportunity dictionaries.
    """
    import ai_chat
    import config
    import json
    
    client = ai_chat.get_ai_client()
    prompt = f"""
    Generate 5 highly realistic, current career opportunities for the career track: {career_name}.
    Include a balanced mix:
    - 3 Internships (specifically tailored for students/entry-level, ideal for platforms like Internshala)
    - 2 Full-Time Jobs (Junior/Mid-level)

    For each opportunity, specify:
    1. "title": Job or Internship Title (e.g. "{career_name} Intern", "Junior {career_name}")
    2. "company": Company Name (mix of startups, tech companies, or well-known organizations)
    3. "type": Must be either "Internship" or "Full-time"
    4. "location": Location (e.g. "Remote (Work from Home)", "Bengaluru (Hybrid)", "Hyderabad", "San Francisco, CA")
    5. "compensation": Stipend or Salary Range strictly in Indian Rupees (e.g. "₹15,000 - ₹30,000 / month" for internships, or "₹8 - ₹16 LPA" or "₹14 - ₹28 LPA" for full-time jobs). Never use dollar signs ($).
    6. "duration": "3 Months", "6 Months", or "Permanent"
    7. "description": 2-3 sentences outlining the role focus and day-to-day learning
    8. "skills": Exactly 3 relevant technical skills
    9. "platform": "Internshala" for internships, or "LinkedIn" for jobs

    You must format your response strictly as a valid, single JSON array of objects. Do NOT wrap the JSON in ```json``` or any markdown wraps.
    Schema:
    [
      {{
        "title": "...",
        "company": "...",
        "type": "Internship" or "Full-time",
        "location": "...",
        "compensation": "...",
        "duration": "...",
        "description": "...",
        "skills": ["Skill1", "Skill2", "Skill3"],
        "platform": "Internshala" or "LinkedIn"
      }}
    ]
    """
    try:
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional Indian recruiting database manager. Always specify compensation strictly in Indian Rupees (INR ₹ or LPA). Return only JSON data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        content = response.choices[0].message.content.strip()
        
        # Clean any markdown block wraps if model outputs them
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception:
        # Fallback list of realistic jobs & internships in INR
        return [
            {
                "title": f"{career_name} Intern",
                "company": "NextGen Innovations",
                "type": "Internship",
                "location": "Remote (Work from Home)",
                "compensation": "₹18,000 - ₹25,000 / month",
                "duration": "3 Months",
                "description": f"Hands-on internship working closely with senior mentors on live {career_name} pipelines. Certificate and pre-placement offer (PPO) opportunities available.",
                "skills": ["Python", "Git", "Core Fundamentals"],
                "platform": "Internshala"
            },
            {
                "title": f"Junior {career_name} Trainee",
                "company": "Apex Labs Startup",
                "type": "Internship",
                "location": "Bengaluru / Hybrid",
                "compensation": "₹22,000 - ₹35,000 / month",
                "duration": "6 Months",
                "description": f"Collaborate with our cross-functional engineering teams to implement and test modern {career_name} solutions.",
                "skills": ["Problem Solving", "APIs", "SQL"],
                "platform": "Internshala"
            },
            {
                "title": f"Associate {career_name}",
                "company": "Vanguard Tech Partners",
                "type": "Full-time",
                "location": "Bengaluru / Remote",
                "compensation": "₹10 - ₹16 LPA",
                "duration": "Permanent",
                "description": f"Join our digital systems group building scalable client interfaces and operations. Perfect for junior candidates seeking mentoring.",
                "skills": ["Git", "Python", "SQL"],
                "platform": "LinkedIn"
            },
            {
                "title": f"{career_name} Research Intern",
                "company": "Cerebral AI Hub",
                "type": "Internship",
                "location": "Hyderabad / Remote",
                "compensation": "₹20,000 - ₹30,000 / month",
                "duration": "3 Months",
                "description": f"Explore cutting-edge frameworks and prototype new tools with our technical research division.",
                "skills": ["Data Analysis", "Research", "Scripting"],
                "platform": "Internshala"
            },
            {
                "title": f"Staff {career_name}",
                "company": "Velocity Tech Startup",
                "type": "Full-time",
                "location": "Pune / Hybrid",
                "compensation": "₹22 - ₹35 LPA",
                "duration": "Permanent",
                "description": f"Fast-paced role responsible for core product deployments, code reliability, and tooling pipelines. High autonomy and direct impact.",
                "skills": ["Python", "Docker", "CI/CD"],
                "platform": "LinkedIn"
            }
        ]

