from fpdf import FPDF
import datetime
import utils

class CareerReportPDF(FPDF):
    def header(self):
        self.set_fill_color(11, 15, 25) # Dark theme matching UI
        self.rect(0, 0, 210, 297, 'F')
        
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(59, 130, 246) # Slate blue
        self.cell(0, 10, "CAREERPATH AI - PROFESSIONAL BRIEFING", 0, 1, "C")
        
        # Purple header line
        self.set_draw_color(147, 51, 234)
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(156, 163, 175)
        self.line(10, 280, 200, 280)
        self.cell(0, 10, f"Generated on {datetime.date.today().strftime('%Y-%m-%d')} | Confidential Page {self.page_no()}", 0, 0, "C")

def build_pdf_report(name, traits, skills, top_career, match_pct, gap, roadmap, courses, resume_ats=None, interview_score=None):
    """
    Constructs a detailed multi-page PDF career dossier.
    """
    pdf = CareerReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Title Block
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, f"Career Assessment Profile: {utils.clean_unicode(name)}", 0, 1, "L")
    pdf.ln(5)
    
    # Section 1: Personality Assessment
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(96, 165, 250)
    pdf.cell(0, 8, "1. INDIVIDUAL PROFILE METRICS", 0, 1, "L")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.cell(50, 6, f"Logical Thinking: {traits.get('logic', 5)}/10", 0, 0)
    pdf.cell(50, 6, f"Creativity Index: {traits.get('creativity', 5)}/10", 0, 0)
    pdf.cell(50, 6, f"Communication Level: {traits.get('communication', 5)}/10", 0, 1)
    
    pdf.multi_cell(0, 6, f"Current Skills Entered: {utils.clean_unicode(skills) if skills else 'None'}")
    pdf.ln(6)
    
    # Section 2: Recommendations Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(167, 139, 250)
    pdf.cell(0, 8, "2. RECOMMENDATION ALIGNMENT", 0, 1, "L")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, f"Primary Track: {utils.clean_unicode(top_career)} | Match Score: {match_pct}%", 0, 1)
    
    if resume_ats:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(243, 244, 246)
        pdf.cell(0, 6, f"Evaluated Resume ATS Score: {resume_ats}/100", 0, 1)
    if interview_score:
        pdf.cell(0, 6, f"Evaluated Mock Interview Score: {interview_score}/100", 0, 1)
    pdf.ln(6)
    
    # Section 3: Skill Gap Analysis
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(244, 114, 182)
    pdf.cell(0, 8, "3. DETAILED SKILL GAP AUDIT", 0, 1, "L")
    
    already_skills = gap.get("already_have", [])
    need_skills = gap.get("need_to_learn", [])
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 6, "Already Possessed Skills:", 0, 1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.multi_cell(0, 5, ", ".join(already_skills) if already_skills else "None recorded.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(239, 68, 68)
    pdf.cell(0, 6, "Missing Skills to Learn:", 0, 1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(243, 244, 246)
    pdf.multi_cell(0, 5, ", ".join(need_skills) if need_skills else "Qualified for roles!")
    pdf.ln(6)
    
    # Section 4: Learning Curriculum
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(96, 165, 250)
    pdf.cell(0, 8, "4. STRATEGIC ROADMAP GUIDE", 0, 1, "L")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(243, 244, 246)
    
    import roadmap as rm_module
    formatted_roadmap = rm_module.format_roadmap_for_text(roadmap)
    cleaned_roadmap = utils.clean_unicode(formatted_roadmap)
    pdf.multi_cell(0, 4.5, cleaned_roadmap)
    pdf.ln(6)
    
    # Section 5: Online Courses
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(167, 139, 250)
    pdf.cell(0, 8, "5. RECOMMENDED EDUCATIONAL RESOURCES", 0, 1, "L")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(156, 163, 175)
    
    cleaned_courses = utils.clean_unicode(courses)
    pdf.multi_cell(0, 4.5, cleaned_courses if cleaned_courses else "Self-study curriculum complete.")
    
    return bytes(pdf.output())
