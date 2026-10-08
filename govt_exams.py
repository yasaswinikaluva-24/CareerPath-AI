import json
import ai_chat
import config

EXAMS_DATA = {
    "🇮🇳 UPSC Civil Services (IAS / IPS / IFS)": {
        "short_name": "UPSC CSE",
        "authority": "Union Public Service Commission",
        "official_url": "https://upsc.gov.in",
        "eligibility": "Graduate in any discipline from a recognized university",
        "age_limit": "21 - 32 years (General) with category relaxations",
        "attempts": "6 attempts (General), 9 (OBC), Unlimited (SC/ST)",
        "salary_range": "₹7 - ₹25 LPA (+ Subsidized Govt Housing, Staff, Official Transport & Lifetime Pension/Perks)",
        "overview": "India's most prestigious examination to recruit officers for the Indian Administrative Service (IAS), Indian Police Service (IPS), Indian Foreign Service (IFS), and other central Group A/B services.",
        "stages": [
            {
                "stage": "Stage 1: Preliminary Exam (Objective)",
                "details": "GS Paper 1 (200 Marks, 100 Questions) + CSAT Paper 2 (200 Marks, 80 Questions - Qualifying at 33%). 1/3rd Negative Marking."
            },
            {
                "stage": "Stage 2: Main Exam (Descriptive)",
                "details": "9 Written Papers (1750 Total Marks): Essay (250), GS 1 to 4 (250 each = 1000), Optional Paper 1 & 2 (250 each = 500), 2 Qualifying Language Papers."
            },
            {
                "stage": "Stage 3: Personality Test / Interview",
                "details": "275 Marks. Evaluates mental alertness, critical assimilation, intellectual integrity, and leadership suitability by the UPSC Board."
            }
        ],
        "syllabus_highlights": [
            "Indian Polity & Constitution (Governance, Rights, Federalism)",
            "Indian Economy & Development (Monetary Policy, Budget, Inclusive Growth)",
            "Modern Indian History, Art & Culture, and World History",
            "Physical, Human & Economic Geography (India & World)",
            "Environment, Ecology, Biodiversity & Climate Change",
            "Science & Technology (AI, Space, Biotech, Defense Tech)",
            "Ethics, Integrity & Aptitude (Case Studies, Moral Philosophy)",
            "Current Affairs of National & International Importance"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1 (Months 1-3): NCERT Foundation & Core Reading",
                "goals": [
                    "Read Class 6-12 NCERTs for History, Geography, Polity, and Economy",
                    "Begin reading The Hindu or Indian Express daily (focus on Editorials)",
                    "Familiarize with UPSC CSE Syllabus and past 10 years question papers (PYQs)"
                ]
            },
            {
                "phase": "Phase 2 (Months 4-7): Standard Core Reference Books & Notes",
                "goals": [
                    "Complete Indian Polity (M. Laxmikanth), Modern History (Spectrum), Economy (Ramesh Singh/Mrunal)",
                    "Finalize and complete 70% of Optional Subject syllabus",
                    "Start weekly answer writing practice for GS Papers 1, 2, and 3"
                ]
            },
            {
                "phase": "Phase 3 (Months 8-10): Intense Answer Writing & Mock Test Series",
                "goals": [
                    "Enroll in a Prelims test series (complete at least 40 full-length mock tests)",
                    "Daily 2-question answer writing with self-evaluation or AI review",
                    "Complete Ethics (GS 4) case study frameworks and essay writing practice"
                ]
            },
            {
                "phase": "Phase 4 (Months 11-12): Final Revision & Current Affairs Consolidation",
                "goals": [
                    "Revise monthly current affairs compilations (PT 365 or similar)",
                    "Practice CSAT speed tests (Reading Comprehension & Basic Numeracy)",
                    "Re-attempt UPSC previous 5 years official Prelims papers in timed exam conditions"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "Indian Polity",
                "question": "Examine the significance of the Basic Structure doctrine in preserving constitutional democracy in India. Cite landmark judicial verdicts."
            },
            {
                "subject": "Indian Economy",
                "question": "How can India leverage digital public infrastructure (DPI) to bridge economic inequality and accelerate inclusive rural growth?"
            },
            {
                "subject": "Ethics & Integrity",
                "question": "What does 'integrity' mean to a civil servant facing political pressure? Discuss with an illustrative real-world case study."
            }
        ]
    },
    "🏛️ SSC CGL (Income Tax, Excise & ASO)": {
        "short_name": "SSC CGL",
        "authority": "Staff Selection Commission",
        "official_url": "https://ssc.gov.in",
        "eligibility": "Bachelor's Degree from a recognized university",
        "age_limit": "18 - 32 years (depending on post)",
        "attempts": "No limit within the age criteria",
        "salary_range": "₹6 - ₹16 LPA (Pay Level 4 to Level 8 + DA, HRA, Central Govt Healthcare)",
        "overview": "Recruits officers for non-technical Group B and Group C government posts such as Income Tax Inspector, Central Excise Inspector, Assistant Section Officer (ASO) in MEA and CSS, and CBI Sub-Inspector.",
        "stages": [
            {
                "stage": "Tier 1: Computer Based Examination (Objective)",
                "details": "100 Questions (200 Marks) in 60 Minutes: General Intelligence & Reasoning (50), General Awareness (50), Quantitative Aptitude (50), English Comprehension (50). Qualifying in nature."
            },
            {
                "stage": "Tier 2: Main Examination (Merit Based)",
                "details": "Paper 1: Math & Reasoning (180 Marks), English & GA (210 Marks), Computer Knowledge (60 Marks - Qualifying), Data Entry Speed Test (DEST)."
            }
        ],
        "syllabus_highlights": [
            "Quantitative Aptitude (Arithmetic, Advanced Math: Algebra, Geometry, Trigonometry)",
            "Reasoning & Mental Ability (Analogy, Blood Relations, Coding-Decoding, Non-Verbal)",
            "General Awareness (Static GK, History, Polity, Geography, Current Affairs)",
            "English Language & Comprehension (Grammar, Vocabulary, Cloze Test, Reading)",
            "Computer Knowledge (Hardware, Software, Internet, Networking, MS Office)"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1 (Months 1-2): Math & Reasoning Concept Mastery",
                "goals": [
                    "Master arithmetic shortcuts: Percentage, Ratio, Profit & Loss, SI/CI, Time & Work",
                    "Complete verbal and non-verbal reasoning chapters with 50 practice questions each",
                    "Build a daily English vocabulary list (idioms, one-word substitutions, synonyms)"
                ]
            },
            {
                "phase": "Phase 2 (Months 3-4): Advanced Math & Static GK Drill",
                "goals": [
                    "Complete Geometry, Mensuration, Trigonometry, and Algebra formulas",
                    "Revise Lucent GK for History, Polity, and General Science",
                    "Start taking sectional timed quizzes on English grammar and comprehension"
                ]
            },
            {
                "phase": "Phase 3 (Months 5-6): Speed Building & Tier 1 Mock Tests",
                "goals": [
                    "Take 1 full-length mock test daily with in-depth error analysis",
                    "Work on speed math: squares, cubes, tables up to 30, and approximation",
                    "Target 150+ score in Tier 1 mock tests"
                ]
            },
            {
                "phase": "Phase 4 (Months 7-8): Tier 2 Advanced Mocks & Typing Practice",
                "goals": [
                    "Practice 15-minute typing test daily to exceed 27 WPM with 95% accuracy",
                    "Solve Tier 2 level complex quantitative and reasoning problem sets",
                    "Revise Computer Awareness theory and shortcut keys"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "Quantitative Aptitude",
                "question": "A sum of ₹12,000 amounts to ₹15,972 in 3 years at a certain rate percent per annum at compound interest. What will be the simple interest on the same sum for 4 years at double the rate?"
            },
            {
                "subject": "General Awareness",
                "question": "Explain the concept of Fiscal Deficit. How does the Reserve Bank of India manage market liquidity through Open Market Operations (OMOs)?"
            }
        ]
    },
    "🏦 Bank PO & RBI Grade B Officer": {
        "short_name": "IBPS / SBI / RBI",
        "authority": "IBPS, State Bank of India & Reserve Bank of India",
        "official_url": "https://www.ibps.in",
        "eligibility": "Graduation in any discipline with minimum 60% for RBI Grade B",
        "age_limit": "20 - 30 years (Bank PO), 21 - 30 years (RBI Grade B)",
        "attempts": "SBI PO: 4 attempts (General); RBI Grade B: 6 attempts (General)",
        "salary_range": "₹8 - ₹24 LPA (RBI Grade B CTC exceeds ₹24 LPA with Mumbai accommodation)",
        "overview": "Premier gateway to managerial careers in India's banking and financial sector, including Probationary Officer (PO) in SBI/nationalized banks and Grade B Manager in India's central bank (RBI).",
        "stages": [
            {
                "stage": "Stage 1: Preliminary Exam (Objective)",
                "details": "100 Questions (100 Marks) in 60 Minutes: English (30), Quantitative Aptitude (35), Reasoning Ability (35) with 20 minutes sectional timing."
            },
            {
                "stage": "Stage 2: Mains Exam (Objective + Descriptive)",
                "details": "Reasoning & Computer (60), Data Analysis & Interpretation (60), General & Banking Awareness (40), English (40) + English Descriptive Essay/Letter (50 Marks)."
            },
            {
                "stage": "Stage 3: Group Discussion & Interview",
                "details": "Psychometric Test, Group Discussion / Group Exercise, and Personal Interview before senior banking executives."
            }
        ],
        "syllabus_highlights": [
            "Data Analysis & Interpretation (Bar, Pie, Radar, Caselet, Missing DI)",
            "High-Level Reasoning (Floor/Box Puzzles, Seating Arrangement, Input-Output)",
            "Banking & Financial Awareness (RBI Guidelines, Monetary Policy, Basel Norms, NPA)",
            "Economic & Social Issues (Inflation, GDP growth, Sustainable Development)",
            "English Language (Reading Comprehension, Error Spotting, Descriptive Essay & Letter)"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1 (Months 1-2): Calculation Speed & Core Puzzles",
                "goals": [
                    "Master Vedic math techniques, percentages, fractions, and quadratic equations",
                    "Solve 5 reasoning puzzles and seating arrangement sets daily",
                    "Read financial newspapers (Mint or Business Standard) to build banking vocabulary"
                ]
            },
            {
                "phase": "Phase 2 (Months 3-4): Data Interpretation & Banking Theory",
                "goals": [
                    "Master Caselet DI, Arithmetic DI, and Multi-layer graphical interpretations",
                    "Complete Banking Awareness concepts: Repo/Reverse Repo, CRR, SLR, Priority Sector Lending",
                    "Practice weekly formal letter writing and 250-word economic essays"
                ]
            },
            {
                "phase": "Phase 3 (Months 5-6): Speed Drilling & Sectional Cutoff Mocks",
                "goals": [
                    "Attempt 20 Prelims speed mocks with sectional time management",
                    "Revise 6 months of banking and financial current affairs",
                    "Simulate Mains exam condition (3 hours continuous writing)"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "Banking & Financial Awareness",
                "question": "What are the key differences between Repo Rate, Marginal Standing Facility (MSF), and Standing Deposit Facility (SDF) in RBI's liquidity management framework?"
            },
            {
                "subject": "Descriptive English",
                "question": "Write an essay on 'The Rise of Digital Lending and FinTech in India: Opportunities, Systemic Risks, and Regulatory Safeguards'."
            }
        ]
    },
    "🎓 Teaching & Professorship (UGC NET / CTET)": {
        "short_name": "UGC NET / CTET",
        "authority": "National Testing Agency (NTA) & CBSE",
        "official_url": "https://ugcnet.nta.ac.in",
        "eligibility": "Master's Degree with min 55% (for UGC NET); B.Ed / D.El.Ed (for CTET)",
        "age_limit": "JRF: 30 years; Assistant Professor / CTET: No upper age limit",
        "attempts": "No limit",
        "salary_range": "₹5 - ₹18 LPA (Assistant Professor UGC 7th Pay Commission Pay Level 10)",
        "overview": "National qualification for eligibility as Assistant Professor and Junior Research Fellowship (JRF) in Indian universities, or Central Government School Educator (Kendriya Vidyalaya, Navodaya Vidyalaya).",
        "stages": [
            {
                "stage": "Paper 1: Teaching & Research Aptitude (General)",
                "details": "50 Questions (100 Marks): Teaching Aptitude, Research Aptitude, Reading Comprehension, Communication, Mathematical Reasoning, ICT, Higher Education System."
            },
            {
                "stage": "Paper 2: Subject Specialization",
                "details": "100 Questions (200 Marks): In-depth questions in your Master's domain (e.g. Computer Science, English, Economics, Commerce, History, etc.)."
            }
        ],
        "syllabus_highlights": [
            "Teaching Aptitude (Pedagogy, Learner's Characteristics, Evaluation Systems)",
            "Research Aptitude (Methods, Thesis Writing, Ethics, ICT in Research)",
            "Communication & Classroom Dynamics",
            "Information & Communication Technology (ICT) in Education",
            "People, Development & Environment (SDGs, Pollution, Natural Hazards)",
            "Higher Education System (Governance, Value Education, National Education Policy 2020)"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1 (Months 1-2): Paper 1 Pedagogy & Research Mastery",
                "goals": [
                    "Complete Teaching Aptitude models (Bloom's Taxonomy, Gagne's conditions of learning)",
                    "Master Research methodology: Qualitative vs Quantitative, Sampling, Hypothesis testing",
                    "Understand key highlights and provisions of NEP 2020"
                ]
            },
            {
                "phase": "Phase 2 (Months 3-4): Subject Core Paper 2 Syllabus Completion",
                "goals": [
                    "Break down the 10 units of your chosen Master's subject syllabus",
                    "Create short revision flashcards for landmark theories and author concepts",
                    "Solve past 5 years Paper 2 question papers unit by unit"
                ]
            },
            {
                "phase": "Phase 3 (Months 5-6): Full Mock Tests & JRF Cutoff Strategy",
                "goals": [
                    "Complete 15 full Paper 1 + Paper 2 simulated mock tests",
                    "Refine time management: 60 mins for Paper 1, 120 mins for Paper 2",
                    "Aim for 70%+ score to qualify for both JRF and Assistant Professorship"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "Teaching Aptitude",
                "question": "Differentiate between Formative and Summative evaluation in classroom assessment. How does Continuous and Comprehensive Evaluation (CCE) foster holistic learner development?"
            },
            {
                "subject": "Higher Education & NEP 2020",
                "question": "Discuss the major structural transformations recommended by the National Education Policy (NEP) 2020 in higher education, focusing on the Academic Bank of Credits (ABC) and multidisciplinary education."
            }
        ]
    },
    "⚔️ Defense Officer (NDA / CDS / AFCAT)": {
        "short_name": "NDA / CDS / AFCAT",
        "authority": "UPSC & Indian Armed Forces",
        "official_url": "https://joinindianarmy.nic.in",
        "eligibility": "12th Pass (for NDA), Graduate in any stream (for CDS/AFCAT)",
        "age_limit": "16.5 - 19.5 years (NDA), 19 - 24 years (CDS / IMA / AFA)",
        "attempts": "Based on age eligibility",
        "salary_range": "₹9 - ₹24 LPA (+ Free Defense Accommodation, CSD Canteen, Military Hospital, Family Privileges)",
        "overview": "Prestigious commissioned officer entry into the Indian Army, Indian Navy, and Indian Air Force through the National Defence Academy (NDA), Combined Defence Services (CDS), or Air Force Common Admission Test (AFCAT).",
        "stages": [
            {
                "stage": "Stage 1: Written Examination (Objective)",
                "details": "CDS: English (100), General Knowledge (100), Elementary Mathematics (100) - 300 Marks Total. NDA: Mathematics (300), General Ability Test (600) - 900 Marks Total."
            },
            {
                "stage": "Stage 2: SSB Interview (5-Day Psychological & Leadership Test)",
                "details": "Screening (OIR + PPDT), Psychological Tests (TAT, WAT, SRT, SD), Group Testing Officer (GTO) Ground Tasks, Personal Interview, and Final Conference."
            },
            {
                "stage": "Stage 3: Special Medical Board (SMB)",
                "details": "Comprehensive physical and medical fitness examination by military medical specialists."
            }
        ],
        "syllabus_highlights": [
            "Mathematics (Arithmetic, Trigonometry, Geometry, Mensuration, Statistics)",
            "English (Synonyms, Antonyms, Ordering of Words, Comprehension, Idioms)",
            "General Knowledge (Physics, Chemistry, Biology, History, Geography, Defense Current Affairs)",
            "Officer Like Qualities (OLQs: Effective Intelligence, Initiative, Courage, Stamina, Teamwork)"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1 (Months 1-2): Written Exam Foundation & Daily Physical Fitness",
                "goals": [
                    "Establish daily physical routine: 5 km run, pushups, pull-ups, and core exercises",
                    "Complete elementary mathematics shortcuts and English grammar rules",
                    "Stay updated with national defense developments and geopolitical events"
                ]
            },
            {
                "phase": "Phase 2 (Months 3-4): Written Mocks & SSB Psychology Preparation",
                "goals": [
                    "Solve past 10 CDS/NDA question papers under timed conditions",
                    "Practice Thematic Apperception Test (TAT) positive story writing",
                    "Practice Word Association Test (WAT) and Situation Reaction Test (SRT) responses"
                ]
            },
            {
                "phase": "Phase 3 (Months 5-6): Group Discussions & Lecturette Practice",
                "goals": [
                    "Practice 3-minute impromptu lecturette speeches on current geopolitical topics",
                    "Participate in group discussions emphasizing constructive reasoning and cooperation",
                    "Final mock conference simulation with retired defense mentors or peer aspirants"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "SSB Situation Reaction Test (SRT)",
                "question": "You are leading a trekking expedition in remote hills. Suddenly, a team member slips, fractures his leg, and weather is deteriorating fast with no mobile signal. What will you do?"
            },
            {
                "subject": "Geopolitical Defense Affairs",
                "question": "Explain the strategic significance of the QUAD alliance (India, US, Japan, Australia) for security and freedom of navigation in the Indo-Pacific region."
            }
        ]
    },
    "📊 Chartered Accountant (CA Foundation & Final)": {
        "short_name": "ICAI CA",
        "authority": "Institute of Chartered Accountants of India",
        "official_url": "https://www.icai.org",
        "eligibility": "12th Pass (for Foundation) or Graduate (Direct Entry to Inter)",
        "age_limit": "No upper age limit",
        "attempts": "No limit",
        "salary_range": "₹8 - ₹30+ LPA (Corporate CA starting packages average ₹9-12 LPA; top rankers earn ₹25+ LPA)",
        "overview": "India's highest qualification in accounting, auditing, direct & indirect taxation, and corporate financial advisory. Chartered Accountants hold exclusive statutory auditing authority in India.",
        "stages": [
            {
                "stage": "Level 1: CA Foundation (4 Papers - 400 Marks)",
                "details": "Accounting, Business Laws, Quantitative Aptitude, Business Economics. Requires 40% in each paper and 50% aggregate."
            },
            {
                "stage": "Level 2: CA Intermediate (6 Papers in 2 Groups)",
                "details": "Group 1: Advanced Accounting, Corporate Laws, Taxation. Group 2: Cost & Management Accounting, Auditing & Ethics, Financial Management."
            },
            {
                "stage": "Level 3: 2-Year Practical Articleship Training",
                "details": "Mandatory 2 years of practical training under a practicing Chartered Accountant firm."
            },
            {
                "stage": "Level 4: CA Final (6 Papers in 2 Groups)",
                "details": "Financial Reporting, Advanced Financial Management, Advanced Auditing, Direct Tax Laws, Indirect Tax Laws, Integrated Business Solutions."
            }
        ],
        "syllabus_highlights": [
            "Financial Reporting & Indian Accounting Standards (Ind AS)",
            "Direct Tax Laws & International Taxation (Income Tax Act 1961)",
            "Indirect Tax Laws (Goods and Services Tax - GST & Customs)",
            "Advanced Auditing, Assurance & Professional Ethics",
            "Strategic Financial Management & Corporate Valuation",
            "Corporate and Economic Laws (Companies Act 2013, IBC, FEMA)"
        ],
        "roadmap_phases": [
            {
                "phase": "Phase 1: Conceptual Core Mastery (Accounting & Law)",
                "goals": [
                    "Complete all chapters of ICAI Study Material for Accounting and Corporate Law",
                    "Understand practical GST return filing and Income Tax computations",
                    "Solve past 5 examination papers and Revision Test Papers (RTPs)"
                ]
            },
            {
                "phase": "Phase 2: Group 2 Practical Papers (Audit & Costing)",
                "goals": [
                    "Memorize Standards on Auditing (SAs) with keyword precision",
                    "Practice practical costing methods: Standard Costing, Marginal Costing, Activity Based Costing",
                    "Write 2 full mock papers for each subject under 3-hour exam conditions"
                ]
            },
            {
                "phase": "Phase 3: Articleship & Final Advanced Specialization",
                "goals": [
                    "Gain hands-on experience in Statutory Audits, Tax Audits, and Corporate Assessments",
                    "Master Ind AS application and international transfer pricing",
                    "Consolidate summary notes for one-day before exam revision"
                ]
            }
        ],
        "sample_questions": [
            {
                "subject": "Auditing & Professional Ethics",
                "question": "What are the auditor's responsibilities under SA 240 relating to fraud in an audit of financial statements? Discuss the distinction between error and fraud."
            },
            {
                "subject": "Direct Taxation",
                "question": "Explain the conditions and tax implications under Section 54 of the Income Tax Act for exemption of capital gains arising from the transfer of a residential house property."
            }
        ]
    }
}

def get_all_exams():
    """Returns list of all supported competitive exams."""
    return list(EXAMS_DATA.keys())

def get_exam_details(exam_key):
    """Fetches details for a specific competitive exam."""
    return EXAMS_DATA.get(exam_key, None)

def evaluate_aspirant_answer(exam_name, question, user_answer):
    """
    Evaluates a competitive exam subjective answer using AI.
    Returns structured feedback on Structure, Content Accuracy, Analysis, and Score out of 10.
    """
    client = ai_chat.get_ai_client()
    
    system_prompt = (
        f"You are a seasoned senior evaluator and faculty for {exam_name}. "
        "Evaluate the candidate's answer constructively, providing specific scoring and suggestions."
    )
    
    user_prompt = f"""
Exam: {exam_name}
Question: {question}

Candidate's Answer:
\"\"\"
{user_answer}
\"\"\"

Please evaluate this answer and provide feedback formatted in markdown:
1. **Overall Score**: [Score out of 10]
2. **Structure & Presentation**: (Introduction, Body Paragraphs, Conclusion)
3. **Key Strengths**: (What was done well, relevant points, keywords)
4. **Gaps & Missing Dimensions**: (Facts, constitutional articles, economic data, or viewpoints missed)
5. **Model Value-Add Points**: (2-3 high-scoring points to elevate this answer to top percentile)
"""

    try:
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Evaluation service temporarily busy ({str(e)}). Please review the model answer guidelines above."
