# Career Path alignment engine and database of careers

CAREERS_DB = {
    "AI Engineer": {
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "APIs"],
        "ideal_traits": {"logic": 9, "creativity": 8, "communication": 6},
        "salary": "₹18 - ₹35 LPA",
        "demand": "Very High",
        "growth": "30%",
        "difficulty": 5,
        "work_style": "Remote",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding", "Mathematics"]
    },
    "Machine Learning Engineer": {
        "required_skills": ["Python", "Machine Learning", "Statistics", "Scikit-Learn", "SQL", "MLOps", "Git"],
        "ideal_traits": {"logic": 10, "creativity": 6, "communication": 6},
        "salary": "₹16 - ₹32 LPA",
        "demand": "Very High",
        "growth": "28%",
        "difficulty": 5,
        "work_style": "Hybrid",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding", "Mathematics"]
    },
    "Data Scientist": {
        "required_skills": ["Python", "R", "Statistics", "Pandas", "SQL", "Tableau", "Data Visualization"],
        "ideal_traits": {"logic": 9, "creativity": 6, "communication": 8},
        "salary": "₹14 - ₹28 LPA",
        "demand": "High",
        "growth": "25%",
        "difficulty": 4,
        "work_style": "Hybrid",
        "prefers_math": True,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Mathematics", "Strategy"]
    },
    "Data Analyst": {
        "required_skills": ["SQL", "Excel", "Tableau", "PowerBI", "Python", "Statistics", "Data Cleaning"],
        "ideal_traits": {"logic": 7, "creativity": 5, "communication": 8},
        "salary": "₹6 - ₹14 LPA",
        "demand": "High",
        "growth": "18%",
        "difficulty": 2,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Mathematics", "Strategy"]
    },
    "Frontend Developer": {
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "Vue", "TypeScript", "Figma"],
        "ideal_traits": {"logic": 7, "creativity": 9, "communication": 7},
        "salary": "₹7 - ₹18 LPA",
        "demand": "High",
        "growth": "15%",
        "difficulty": 3,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Design", "Coding"]
    },
    "Backend Developer": {
        "required_skills": ["Python", "NodeJS", "Java", "Go", "SQL", "APIs", "Docker", "Git"],
        "ideal_traits": {"logic": 9, "creativity": 6, "communication": 6},
        "salary": "₹8 - ₹22 LPA",
        "demand": "High",
        "growth": "20%",
        "difficulty": 4,
        "work_style": "Remote",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": False,
        "fav_subjects": ["Coding"]
    },
    "Full Stack Developer": {
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "NodeJS", "SQL", "APIs", "Git"],
        "ideal_traits": {"logic": 8, "creativity": 8, "communication": 7},
        "salary": "₹9 - ₹24 LPA",
        "demand": "Very High",
        "growth": "22%",
        "difficulty": 4,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding", "Design"]
    },
    "Cybersecurity Engineer": {
        "required_skills": ["Networking", "Linux", "Cryptography", "Wireshark", "Firewalls", "Python"],
        "ideal_traits": {"logic": 9, "creativity": 7, "communication": 6},
        "salary": "₹10 - ₹25 LPA",
        "demand": "Very High",
        "growth": "32%",
        "difficulty": 4,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Security", "Coding"]
    },
    "Ethical Hacker": {
        "required_skills": ["Metasploit", "Nmap", "Linux", "Penetration Testing", "Networking", "Python", "Bash"],
        "ideal_traits": {"logic": 9, "creativity": 9, "communication": 6},
        "salary": "₹10 - ₹26 LPA",
        "demand": "High",
        "growth": "28%",
        "difficulty": 4,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": False,
        "fav_subjects": ["Security", "Hardware"]
    },
    "Cloud Engineer": {
        "required_skills": ["AWS", "Azure", "Linux", "Terraform", "Docker", "Kubernetes", "Networking"],
        "ideal_traits": {"logic": 8, "creativity": 6, "communication": 7},
        "salary": "₹11 - ₹26 LPA",
        "demand": "Very High",
        "growth": "24%",
        "difficulty": 4,
        "work_style": "Hybrid",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding", "Security"]
    },
    "DevOps Engineer": {
        "required_skills": ["CI/CD", "Jenkins", "Docker", "Kubernetes", "Linux", "Python", "Ansible", "AWS"],
        "ideal_traits": {"logic": 9, "creativity": 6, "communication": 7},
        "salary": "₹12 - ₹28 LPA",
        "demand": "Very High",
        "growth": "26%",
        "difficulty": 4,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding", "Security"]
    },
    "Software Engineer": {
        "required_skills": ["Java", "C++", "Python", "Data Structures", "Algorithms", "Git", "System Design"],
        "ideal_traits": {"logic": 9, "creativity": 7, "communication": 7},
        "salary": "₹8 - ₹22 LPA",
        "demand": "High",
        "growth": "19%",
        "difficulty": 4,
        "work_style": "Hybrid",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding"]
    },
    "Mobile App Developer": {
        "required_skills": ["Swift", "Kotlin", "Flutter", "React Native", "APIs", "Git", "Mobile Design"],
        "ideal_traits": {"logic": 7, "creativity": 8, "communication": 7},
        "salary": "₹8 - ₹20 LPA",
        "demand": "High",
        "growth": "17%",
        "difficulty": 3,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Design", "Coding"]
    },
    "UI UX Designer": {
        "required_skills": ["Figma", "Sketch", "Prototyping", "User Research", "Wireframing", "Adobe XD"],
        "ideal_traits": {"logic": 5, "creativity": 10, "communication": 9},
        "salary": "₹6 - ₹16 LPA",
        "demand": "High",
        "growth": "16%",
        "difficulty": 3,
        "work_style": "Hybrid",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Design", "Strategy"]
    },
    "Blockchain Developer": {
        "required_skills": ["Solidity", "Ethereum", "Cryptography", "Smart Contracts", "Web3.js", "Go", "C++"],
        "ideal_traits": {"logic": 10, "creativity": 8, "communication": 6},
        "salary": "₹15 - ₹35 LPA",
        "demand": "High",
        "growth": "35%",
        "difficulty": 5,
        "work_style": "Remote",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": False,
        "fav_subjects": ["Security", "Coding"]
    },
    "Game Developer": {
        "required_skills": ["C++", "C#", "Unity", "Unreal Engine", "Linear Algebra", "3D Modeling", "Git"],
        "ideal_traits": {"logic": 8, "creativity": 10, "communication": 6},
        "salary": "₹6 - ₹16 LPA",
        "demand": "Medium",
        "growth": "12%",
        "difficulty": 5,
        "work_style": "Hybrid",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Design", "Coding"]
    },
    "Embedded Engineer": {
        "required_skills": ["C", "C++", "Microcontrollers", "RTOS", "IoT", "PCB Design", "Debugging"],
        "ideal_traits": {"logic": 9, "creativity": 6, "communication": 6},
        "salary": "₹7 - ₹18 LPA",
        "demand": "Medium",
        "growth": "10%",
        "difficulty": 4,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": False,
        "fav_subjects": ["Hardware", "Coding"]
    },
    "QA Engineer": {
        "required_skills": ["Selenium", "Automation Testing", "Jira", "Python", "Manual Testing", "SQL", "Git"],
        "ideal_traits": {"logic": 7, "creativity": 5, "communication": 7},
        "salary": "₹5 - ₹14 LPA",
        "demand": "Medium",
        "growth": "11%",
        "difficulty": 2,
        "work_style": "Remote",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Coding"]
    },
    "Database Administrator": {
        "required_skills": ["SQL", "Oracle", "MySQL", "Database Tuning", "Backup & Recovery", "Linux", "NoSQL"],
        "ideal_traits": {"logic": 8, "creativity": 4, "communication": 6},
        "salary": "₹7 - ₹16 LPA",
        "demand": "Medium",
        "growth": "9%",
        "difficulty": 3,
        "work_style": "Office",
        "prefers_math": False,
        "prefers_speaking": False,
        "prefers_teamwork": False,
        "fav_subjects": ["Coding"]
    },
    "Business Analyst": {
        "required_skills": ["Requirements Gathering", "Agile", "SQL", "Excel", "Data Analysis", "Jira", "Communication"],
        "ideal_traits": {"logic": 7, "creativity": 6, "communication": 9},
        "salary": "₹7 - ₹16 LPA",
        "demand": "High",
        "growth": "14%",
        "difficulty": 2,
        "work_style": "Hybrid",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Strategy", "Mathematics"]
    },
    "Product Manager": {
        "required_skills": ["Product Strategy", "Roadmapping", "Agile", "User Analytics", "A/B Testing", "Market Research"],
        "ideal_traits": {"logic": 8, "creativity": 8, "communication": 10},
        "salary": "₹16 - ₹35 LPA",
        "demand": "Very High",
        "growth": "20%",
        "difficulty": 4,
        "work_style": "Hybrid",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Strategy", "Design"]
    },
    "UPSC Civil Services (IAS / IPS / IFS)": {
        "required_skills": ["General Studies", "Indian Polity", "Economics", "Current Affairs", "Analytical Essay Writing", "Ethics & Integrity", "Public Administration"],
        "ideal_traits": {"logic": 8, "creativity": 7, "communication": 9},
        "salary": "₹7 - ₹25 LPA (+ Govt Perks & Allowances)",
        "demand": "Very High",
        "growth": "20%",
        "difficulty": 5,
        "work_style": "Office",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Strategy", "Humanities", "Leadership"]
    },
    "SSC CGL Inspector & Officer": {
        "required_skills": ["Quantitative Aptitude", "Reasoning Ability", "General Awareness", "English Comprehension", "Data Interpretation", "Computer Proficiency"],
        "ideal_traits": {"logic": 8, "creativity": 5, "communication": 7},
        "salary": "₹6 - ₹16 LPA",
        "demand": "High",
        "growth": "18%",
        "difficulty": 4,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Mathematics", "Strategy"]
    },
    "Bank PO & RBI Grade B Officer": {
        "required_skills": ["Banking Awareness", "Financial Management", "Quantitative Aptitude", "Economic & Social Issues", "English Language", "Reasoning"],
        "ideal_traits": {"logic": 9, "creativity": 6, "communication": 8},
        "salary": "₹8 - ₹24 LPA",
        "demand": "High",
        "growth": "22%",
        "difficulty": 4,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Mathematics", "Strategy", "Finance"]
    },
    "Professor & Lecturer (UGC NET)": {
        "required_skills": ["Subject Matter Expertise", "Research Methodology", "Classroom Pedagogy", "Curriculum Design", "Academic Writing", "Communication"],
        "ideal_traits": {"logic": 7, "creativity": 8, "communication": 10},
        "salary": "₹6 - ₹18 LPA",
        "demand": "Medium",
        "growth": "14%",
        "difficulty": 3,
        "work_style": "Office",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Humanities", "Strategy", "Teaching"]
    },
    "School Teacher & Educator (CTET)": {
        "required_skills": ["Child Pedagogy", "Curriculum Planning", "Classroom Management", "Educational Psychology", "Subject Knowledge", "Parent Communication"],
        "ideal_traits": {"logic": 6, "creativity": 8, "communication": 9},
        "salary": "₹4 - ₹10 LPA",
        "demand": "High",
        "growth": "12%",
        "difficulty": 2,
        "work_style": "Office",
        "prefers_math": False,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Humanities", "Teaching"]
    },
    "Defense Officer (NDA / CDS / AFCAT)": {
        "required_skills": ["Physical Fitness", "Strategic Leadership", "General Knowledge", "Analytical Reasoning", "Team Command", "Psychological Aptitude"],
        "ideal_traits": {"logic": 8, "creativity": 6, "communication": 9},
        "salary": "₹9 - ₹24 LPA (+ Defense Perks)",
        "demand": "High",
        "growth": "15%",
        "difficulty": 5,
        "work_style": "Office",
        "prefers_math": True,
        "prefers_speaking": True,
        "prefers_teamwork": True,
        "fav_subjects": ["Strategy", "Leadership", "Physical Training"]
    },
    "Chartered Accountant (CA)": {
        "required_skills": ["Financial Accounting", "Auditing", "Direct & Indirect Tax", "Corporate Law", "Financial Management", "Cost Accounting"],
        "ideal_traits": {"logic": 10, "creativity": 5, "communication": 7},
        "salary": "₹8 - ₹30 LPA",
        "demand": "Very High",
        "growth": "25%",
        "difficulty": 5,
        "work_style": "Hybrid",
        "prefers_math": True,
        "prefers_speaking": False,
        "prefers_teamwork": True,
        "fav_subjects": ["Mathematics", "Finance", "Strategy"]
    }
}


def is_skill_matched(required_skill, user_skills_list):
    r = required_skill.strip().lower()
    for u in user_skills_list:
        u_clean = u.strip().lower()
        if not u_clean:
            continue
        if r == u_clean or r in u_clean or u_clean in r:
            return True
        aliases = {
            "ml": "machine learning", "dl": "deep learning", "ai": "artificial intelligence",
            "js": "javascript", "ts": "typescript", "py": "python", "postgres": "postgresql",
            "c++": "cpp", "k8s": "kubernetes", "polity": "indian polity", "gk": "general awareness",
            "gs": "general studies", "quant": "quantitative aptitude", "aptitude": "quantitative aptitude",
            "reasoning": "reasoning ability", "teaching": "child pedagogy", "accounts": "financial accounting"
        }
        if aliases.get(u_clean) == r or aliases.get(r) == u_clean:
            return True
    return False

def calculate_career_matches(logic, creativity, communication, user_skills, preferences):
    """
    Calculates alignment scores for all careers in the database.
    """
    results = []
    
    user_skills_clean = [s.strip().lower() for s in user_skills] if isinstance(user_skills, list) else [s.strip().lower() for s in user_skills.split(",")] if user_skills else []
    
    for name, data in CAREERS_DB.items():
        # 1. Personality Match (35 points max)
        diff_logic = abs(logic - data["ideal_traits"]["logic"])
        diff_creat = abs(creativity - data["ideal_traits"]["creativity"])
        diff_comm = abs(communication - data["ideal_traits"]["communication"])
        
        total_diff = diff_logic + diff_creat + diff_comm
        personality_score = 35 * (1 - (total_diff / 27.0))
        
        # 2. Preferences Match (35 points max)
        pref_score = 0
        
        # Work style alignment
        pref_work = preferences.get("work_style", "Hybrid")
        if pref_work == "Hybrid" or data["work_style"] == "Hybrid":
            pref_score += 10
        elif pref_work == data["work_style"]:
            pref_score += 10
        else:
            pref_score += 5
            
        # Favorite Subject alignment
        user_fav_subjects = preferences.get("fav_subjects", [])
        subject_overlap = set(user_fav_subjects).intersection(set(data["fav_subjects"]))
        if subject_overlap:
            pref_score += 10
        else:
            pref_score += 2
            
        # Math Interest
        user_math = preferences.get("interest_math", False)
        if user_math == data["prefers_math"]:
            pref_score += 5
        else:
            pref_score += 1
            
        # Public speaking
        user_speaking = preferences.get("public_speaking", False)
        if user_speaking == data["prefers_speaking"]:
            pref_score += 5
        else:
            pref_score += 1
            
        # Team work
        user_team = preferences.get("team_work", False)
        if user_team == data["prefers_teamwork"]:
            pref_score += 5
        else:
            pref_score += 1
            
        # 3. Skill Alignment (30 points max)
        required_skills = data["required_skills"]
        match_count = sum(1 for skill in required_skills if is_skill_matched(skill, user_skills_clean))
                
        skill_score = 0
        if required_skills:
            skill_score = 30 * (match_count / len(required_skills))
            
        # Total match percentage
        total_score = personality_score + pref_score + skill_score
        total_score = max(30.0, min(100.0, total_score)) # cap between 30% and 100%
        
        # Calculate Skill Gap
        already_have = [s for s in required_skills if is_skill_matched(s, user_skills_clean)]
        need_to_learn = [s for s in required_skills if not is_skill_matched(s, user_skills_clean)]
        
        results.append({
            "career_name": name,
            "match_percentage": round(total_score, 1),
            "skills_gap": {
                "already_have": already_have,
                "need_to_learn": need_to_learn
            },
            "salary": data["salary"],
            "demand": data["demand"],
            "growth": data["growth"],
            "difficulty": data["difficulty"],
            "work_style": data["work_style"]
        })
        
    # Sort results by match percentage descending
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results
