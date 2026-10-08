import career_engine

def is_skill_matched(required_skill, user_skills_list):
    """
    Checks if a required skill matches any skill in user's skills list.
    Supports exact, substring, case-insensitive, and alias matching.
    """
    r = required_skill.strip().lower()
    for u in user_skills_list:
        u_clean = u.strip().lower()
        if not u_clean:
            continue
        # Exact match
        if r == u_clean:
            return True
        # Substring / partial match (e.g. "python" in "basic python", "react" in "react.js", "html" in "html/css")
        if r in u_clean or u_clean in r:
            return True
        # Common tech & competitive exam aliases
        aliases = {
            "ml": "machine learning",
            "dl": "deep learning",
            "ai": "artificial intelligence",
            "js": "javascript",
            "ts": "typescript",
            "py": "python",
            "postgres": "postgresql",
            "c++": "cpp",
            "k8s": "kubernetes",
            "polity": "indian polity",
            "gk": "general awareness",
            "gs": "general studies",
            "quant": "quantitative aptitude",
            "aptitude": "quantitative aptitude",
            "reasoning": "reasoning ability",
            "teaching": "child pedagogy",
            "accounts": "financial accounting",
            "tax": "direct & indirect tax",
            "audit": "auditing"
        }
        if aliases.get(u_clean) == r or aliases.get(r) == u_clean:
            return True
    return False

def calculate_intelligent_recommendations(logic, creativity, communication, user_skills, preferences):
    """
    Computes weighted multi-vector career recommendation scores.
    """
    results = []
    
    # Clean user skills
    user_skills_clean = [s.strip().lower() for s in user_skills.split(",")] if user_skills else []
    
    for name, data in career_engine.CAREERS_DB.items():
        # 1. Traits Alignment (25% weight - 25 points max)
        diff_logic = abs(logic - data["ideal_traits"]["logic"])
        diff_creat = abs(creativity - data["ideal_traits"]["creativity"])
        diff_comm = abs(communication - data["ideal_traits"]["communication"])
        
        total_diff = diff_logic + diff_creat + diff_comm
        traits_score = 25 * (1 - (total_diff / 27.0))
        
        # 2. Hard Skills Alignment (25% weight - 25 points max)
        required_skills = data["required_skills"]
        match_count = sum(1 for skill in required_skills if is_skill_matched(skill, user_skills_clean))
                
        skills_score = 0
        if required_skills:
            skills_score = 25 * (match_count / len(required_skills))
            
        # 3. Preference Compatibility (25% weight - 25 points max)
        pref_score = 0
        
        # Work Style (5 points)
        pref_work = preferences.get("work_style", "Hybrid")
        if pref_work == "Hybrid" or data["work_style"] == "Hybrid":
            pref_score += 5
        elif pref_work == data["work_style"]:
            pref_score += 5
        else:
            pref_score += 2.5
            
        # Subject Alignment (10 points)
        user_fav_subjects = preferences.get("fav_subjects", [])
        subject_overlap = set(user_fav_subjects).intersection(set(data["fav_subjects"]))
        if subject_overlap:
            pref_score += 10
        else:
            pref_score += 3
            
        # Programming Experience (5 points)
        prog_exp = preferences.get("programming_exp", "Beginner")
        is_coding_role = "Coding" in data["fav_subjects"]
        if is_coding_role:
            if prog_exp == "Expert":
                pref_score += 5
            elif prog_exp == "Intermediate":
                pref_score += 4
            elif prog_exp == "Beginner":
                pref_score += 2.5
            else: # None
                pref_score += 1
        else:
            pref_score += 5 # Full points for non-coding heavy roles
            
        # Math Alignment (5 points)
        user_math = preferences.get("interest_math", False)
        if user_math == data["prefers_math"]:
            pref_score += 5
        else:
            pref_score += 2
            
        # 4. Soft Work Preferences (25% weight - 25 points max)
        soft_score = 0
        
        # Public speaking (8 points)
        user_speaking = preferences.get("public_speaking", False)
        if user_speaking == data["prefers_speaking"]:
            soft_score += 8
        else:
            soft_score += 3
            
        # Team work (8 points)
        user_team = preferences.get("team_work", False)
        if user_team == data["prefers_teamwork"]:
            soft_score += 8
        else:
            soft_score += 3
            
        # Leadership (9 points)
        # Roles like Product Manager and Business Analyst benefit from leadership interest
        user_leadership = preferences.get("leadership_interest", False)
        is_leadership_role = name in ["Product Manager", "Business Analyst"]
        if is_leadership_role:
            if user_leadership:
                soft_score += 9
            else:
                soft_score += 3
        else:
            soft_score += 9
            
        # Total Alignment Percentage
        final_pct = traits_score + skills_score + pref_score + soft_score
        final_pct = max(30.0, min(100.0, final_pct))
        
        # Skill Gap Lists
        already_have = [s for s in required_skills if is_skill_matched(s, user_skills_clean)]
        need_to_learn = [s for s in required_skills if not is_skill_matched(s, user_skills_clean)]
        
        # completion %
        completion_pct = 0
        if required_skills:
            completion_pct = round((len(already_have) / len(required_skills)) * 100, 1)
            
        results.append({
            "career_name": name,
            "match_percentage": round(final_pct, 1),
            "completion_percentage": completion_pct,
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
        
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results
