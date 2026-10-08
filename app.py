import streamlit as st
import os
import time
import json
import re
import urllib.parse
import config
import auth
import database
import recommendation
import roadmap
import resume_analyzer
import interview
import report_generator
import dashboard
import utils
import importlib
importlib.reload(utils)
import styles
import ai_chat
import govt_exams

import base64

parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_file_path = os.path.join(parent_dir, "assets", "logo_dark.png")

def get_logo_base64():
    if os.path.exists(logo_file_path):
        with open(logo_file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_b64 = get_logo_base64()

# Initialize DB tables
database.init_db()

# Page configs
st.set_page_config(
    page_title="CareerPath AI - Personal AI Career Companion",
    page_icon=logo_file_path if os.path.exists(logo_file_path) else "✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern glassmorphic theme styling rules (Purple + Emerald Green theme)
st.markdown(styles.MODERN_CSS, unsafe_allow_html=True)

# Declare Voice Input Custom Component
import streamlit.components.v1 as components
voice_input_component = components.declare_component("voice_input", path=os.path.join(parent_dir, "voice_component"))

# Initialize Session states
if "username" not in st.session_state:
    st.session_state.username = None
if "name" not in st.session_state:
    st.session_state.name = None

if "mock_interview" not in st.session_state:
    st.session_state.mock_interview = {
        "active": False,
        "career_name": "",
        "history": [],
        "current_question": "",
        "question_count": 0,
        "evaluation": ""
    }

# Check if authenticated
if st.session_state.username is None:
    auth.show_auth_page()
    st.stop()

# User is authenticated
username = st.session_state.username
user_profile = database.get_user_profile(username)
is_pro = database.get_user_subscription(username)
st.session_state.is_pro = is_pro

# Load profile values
logic = user_profile.get("logic", 8)
creativity = user_profile.get("creativity", 7)
communication = user_profile.get("communication", 7)
raw_skills = user_profile.get("skills")
user_skills = raw_skills.strip() if (raw_skills and raw_skills.strip()) else "Python, HTML, CSS, JavaScript, SQL, Git"
preferences = user_profile.get("preferences", {})

# Calculate dynamic recommendation data
matches = recommendation.calculate_intelligent_recommendations(
    logic, creativity, communication, user_skills, preferences
)
top_match = matches[0] if matches else {
    "career_name": "AI Engineer",
    "match_percentage": 96.0,
    "skills_gap": {"already_have": ["Python", "SQL", "Git"], "need_to_learn": ["Machine Learning", "Deep Learning", "TensorFlow"]},
    "completion_percentage": 67
}

# Helper function to speak AI text inside application
def speak_ai(text):
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')
        tts_script = f"""
        <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
        }}
        </script>
        """
        st.components.v1.html(tts_script, height=0, width=0)

# Subscription Modal Dialog (1 Month, 1 Year, 3 Years)
@st.dialog("🚀 Upgrade to CareerPath Pro", width="large")
def show_subscription_modal():
    st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
<h2 style='color: #F8FAFC; margin: 0; font-size: 1.6rem;'>Choose Your Career Acceleration Plan</h2>
<p style='color: #94A3B8; font-size: 0.95rem; margin-top: 6px;'>Select a subscription tenure to unlock unlimited AI consultations, mock interviews, and career roadmaps.</p>
</div>

<!-- 3 Subscription Cards Grid -->
<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px;'>
<div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 18px; text-align: center;'>
<div style='background: rgba(255, 255, 255, 0.08); color: #94A3B8; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 10px; display: inline-block; margin-bottom: 8px;'>FLEXIBLE</div>
<div style='color: #F8FAFC; font-weight: 700; font-size: 1.1rem;'>1 Month</div>
<div style='font-size: 1.8rem; font-weight: 800; color: #F8FAFC; margin: 6px 0;'>₹499</div>
<div style='color: #94A3B8; font-size: 0.8rem;'>₹499 / month</div>
<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 12px 0;'>
<div style='font-size: 0.8rem; color: #CBD5E1; text-align: left; line-height: 1.6;'>
✔ Unlimited AI Career Chat<br>
✔ AI Mock Interviews<br>
✔ Full ATS Resume Audits
</div>
</div>

<div style='background: rgba(139, 92, 246, 0.08); border: 2px solid #8B5CF6; border-radius: 14px; padding: 18px; text-align: center; box-shadow: 0 4px 20px rgba(139, 92, 246, 0.25);'>
<div style='background: linear-gradient(135deg, #8B5CF6, #10B981); color: white; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 10px; display: inline-block; margin-bottom: 8px;'>🔥 MOST POPULAR</div>
<div style='color: #F8FAFC; font-weight: 700; font-size: 1.1rem;'>1 Year</div>
<div style='font-size: 1.8rem; font-weight: 800; color: #A78BFA; margin: 6px 0;'>₹3,999</div>
<div style='color: #34D399; font-size: 0.8rem; font-weight: 600;'>₹333 / month (Save 33%)</div>
<hr style='border-color: rgba(139, 92, 246, 0.25); margin: 12px 0;'>
<div style='font-size: 0.8rem; color: #CBD5E1; text-align: left; line-height: 1.6;'>
✔ Everything in 1 Month<br>
✔ 24-Week Interactive Roadmap<br>
✔ Priority Internship Apply<br>
✔ Career Dossier PDF Export
</div>
</div>

<div style='background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 14px; padding: 18px; text-align: center;'>
<div style='background: rgba(16, 185, 129, 0.2); color: #34D399; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 10px; display: inline-block; margin-bottom: 8px;'>👑 BEST VALUE</div>
<div style='color: #F8FAFC; font-weight: 700; font-size: 1.1rem;'>3 Years</div>
<div style='font-size: 1.8rem; font-weight: 800; color: #34D399; margin: 6px 0;'>₹7,999</div>
<div style='color: #34D399; font-size: 0.8rem; font-weight: 600;'>₹222 / month (Save 55%)</div>
<hr style='border-color: rgba(16, 185, 129, 0.2); margin: 12px 0;'>
<div style='font-size: 0.8rem; color: #CBD5E1; text-align: left; line-height: 1.6;'>
✔ College-to-Career Pass<br>
✔ Unlimited AI Career Mentorship<br>
✔ Lifetime Access to Career Tools<br>
✔ All Future Feature Upgrades
</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    plan_key = st.radio(
        "Select Your Subscription Tenure:",
        [
            "⚡ 1 Month Plan — ₹499",
            "🔥 1 Year Plan — ₹3,999 (Most Popular • Save 33%)",
            "👑 3 Years Plan — ₹7,999 (Best Value • Save 55%)"
        ],
        index=1,
        horizontal=True
    )
    
    if "1 Month" in plan_key:
        plan_name = "1 Month Pro Pass"
        amount = 499
        tenure_label = "1 Month (30 Days)"
        subtotal = 499
        discount = 0
    elif "1 Year" in plan_key:
        plan_name = "1 Year Pro Membership"
        amount = 3999
        tenure_label = "1 Year (365 Days)"
        subtotal = 5988
        discount = 1989
    else:
        plan_name = "3 Years Pro Ultimate"
        amount = 7999
        tenure_label = "3 Years (1,095 Days)"
        subtotal = 17964
        discount = 9965

    st.markdown("---")
    
    # Order Summary & Payment Details side-by-side
    col_sum, col_pay = st.columns([1, 1.2], gap="large")
    
    with col_sum:
        st.markdown(f"""
<div class='glass-card' style='padding: 18px !important;'>
<div style='font-weight: 700; color: #F8FAFC; font-size: 1rem; margin-bottom: 12px;'>📋 Order Summary</div>
<div style='display: flex; justify-content: space-between; color: #CBD5E1; font-size: 0.88rem; margin-bottom: 8px;'>
<span>Plan:</span>
<span style='font-weight: 600; color: #F8FAFC;'>{plan_name}</span>
</div>
<div style='display: flex; justify-content: space-between; color: #CBD5E1; font-size: 0.88rem; margin-bottom: 8px;'>
<span>Duration:</span>
<span>{tenure_label}</span>
</div>
<div style='display: flex; justify-content: space-between; color: #CBD5E1; font-size: 0.88rem; margin-bottom: 8px;'>
<span>Subtotal:</span>
<span>₹{subtotal:,}</span>
</div>
<div style='display: flex; justify-content: space-between; color: #34D399; font-size: 0.88rem; margin-bottom: 8px;'>
<span>Special Discount:</span>
<span>-₹{discount:,}</span>
</div>
<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 10px 0;'>
<div style='display: flex; justify-content: space-between; color: #F8FAFC; font-weight: 800; font-size: 1.15rem;'>
<span>Total Payable:</span>
<span style='color: #34D399;'>₹{amount:,}</span>
</div>
<div style='font-size: 0.75rem; color: #94A3B8; margin-top: 6px;'>* Inclusive of 18% GST & all taxes</div>
</div>
<div style='margin-top: 12px; font-size: 0.75rem; color: #94A3B8; display: flex; align-items: center; gap: 6px;'>
🔒 <span>256-Bit SSL Encrypted &bull; RBI-Compliant Gateway UI</span>
</div>
""", unsafe_allow_html=True)

    with col_pay:
        st.markdown("<div style='font-weight: 700; color: #F8FAFC; font-size: 1rem; margin-bottom: 10px;'>💳 Payment Method (INR)</div>", unsafe_allow_html=True)
        pay_method = st.radio(
            "Select Payment Method:",
            ["⚡ UPI / QR Code", "💳 Credit / Debit Card", "🏦 Net Banking"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if "UPI" in pay_method:
            upi_opt = st.radio("UPI Mode:", ["Enter UPI ID", "Show Scan & Pay QR"], horizontal=True)
            if upi_opt == "Enter UPI ID":
                st.text_input("Enter UPI ID / VPA:", placeholder="yourname@okhdfcbank or 9876543210@paytm")
                st.caption("Supports Google Pay, PhonePe, Paytm, BHIM & all bank UPI apps.")
            else:
                st.markdown(f"""
<div style='background: rgba(255, 255, 255, 0.04); border: 1px dashed rgba(255, 255, 255, 0.25); border-radius: 12px; padding: 14px; text-align: center; margin: 8px 0;'>
<div style='font-size: 2.2rem; margin-bottom: 4px;'>📱</div>
<div style='font-weight: 700; color: #F8FAFC; font-size: 0.92rem;'>Scan to Pay ₹{amount:,}</div>
<div style='font-size: 0.78rem; color: #94A3B8; margin-top: 4px;'>Open GPay, PhonePe, Paytm, or BHIM</div>
<div style='background: white; color: black; display: inline-block; padding: 6px 14px; border-radius: 6px; font-weight: 700; font-size: 0.8rem; margin-top: 8px; letter-spacing: 0.5px;'>
UPI ID: careerpath.pro@icici
</div>
</div>
""", unsafe_allow_html=True)
        elif "Card" in pay_method:
            st.text_input("Cardholder Name:", placeholder="Name on Card")
            st.text_input("Card Number:", placeholder="4123 4567 8901 2345", max_chars=19)
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.text_input("Expiry (MM/YY):", placeholder="MM/YY", max_chars=5)
            with col_c2:
                st.text_input("CVV:", placeholder="•••", max_chars=4, type="password")
            st.caption("Accepted: RuPay, Visa, Mastercard, Maestro.")
        else:
            st.selectbox("Select Your Bank:", [
                "State Bank of India (SBI)",
                "HDFC Bank",
                "ICICI Bank",
                "Axis Bank",
                "Kotak Mahindra Bank",
                "Punjab National Bank",
                "Bank of Baroda",
                "Other Netbanking Banks"
            ])
            st.caption("You will be securely redirected to the bank's authentication portal.")
            
        st.write("")
        if st.button(f"💳 Pay ₹{amount:,} & Activate Pro", use_container_width=True, type="primary"):
            with st.spinner(f"Connecting to Secure Gateway for ₹{amount:,}... Please do not close or refresh."):
                time.sleep(1.2)
                database.upgrade_to_pro(username)
                st.session_state.is_pro = True
                st.success(f"🎉 Payment of ₹{amount:,} Successful! Your {plan_name} is now active!")
                st.balloons()
                st.rerun()

member_badge_html = "<div style='font-size: 0.75rem; color: #34D399; font-weight: 600;'>⚡ Pro Member</div>" if is_pro else "<div style='font-size: 0.75rem; color: #94A3B8; font-weight: 600;'>🌱 Free Member</div>"

# =========================================================
# TOP NAVIGATION / HEADER BAR (WITH REAL SEARCH & NOTIFICATIONS)
# =========================================================
top_card = st.container()
with top_card:
    h_col1, h_col2, h_col3, h_col4 = st.columns([2.6, 2.0, 0.45, 1.4], vertical_alignment="center")
    
    with h_col1:
        logo_header_html = f"<img src='data:image/png;base64,{logo_b64}' style='width: 48px; height: 48px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 18px rgba(139, 92, 246, 0.45); border: 1px solid rgba(139, 92, 246, 0.3);'>" if logo_b64 else "<div style='background: linear-gradient(135deg, #7C3AED, #10B981); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); font-size: 20px;'>✨</div>"
        st.markdown(f"""
<div style='display: flex; align-items: center; gap: 14px;'>
    {logo_header_html}
    <div>
        <h2 class='gradient-title' style='font-size: 1.9rem; text-align: left; margin: 0; line-height: 1.15;'>CareerPath AI</h2>
        <p style='margin: 0; font-size: 0.82rem; color: #94A3B8; font-weight: 400;'>Your AI-powered personal career companion</p>
    </div>
</div>
""", unsafe_allow_html=True)

    with h_col2:
        search_query = st.text_input(
            "Search",
            placeholder="🔍 Search careers, skills, or tools...",
            label_visibility="collapsed",
            key="header_search_input"
        )

    with h_col3:
        with st.popover("🔔", use_container_width=True):
            st.markdown("<h4 style='margin:0 0 10px 0; color:#F8FAFC;'>🔔 Notifications</h4>", unsafe_allow_html=True)
            st.markdown("""
<div style='display: flex; flex-direction: column; gap: 10px;'>
    <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;'>
        <div style='font-size: 0.85rem; font-weight: 700; color: #34D399;'>✨ New Feature Live!</div>
        <div style='font-size: 0.78rem; color: #CBD5E1; margin-top: 2px;'>Govt & Competitive Exams Hub added: UPSC, SSC CGL & Bank PO now supported!</div>
    </div>
    <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;'>
        <div style='font-size: 0.85rem; font-weight: 700; color: #A78BFA;'>🎯 Skill Gap Updated</div>
        <div style='font-size: 0.78rem; color: #CBD5E1; margin-top: 2px;'>You can now mark skills as acquired directly from the Skill Gap page.</div>
    </div>
    <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px;'>
        <div style='font-size: 0.85rem; font-weight: 700; color: #F59E0B;'>⚡ Pro Membership</div>
        <div style='font-size: 0.78rem; color: #CBD5E1; margin-top: 2px;'>Unlock 24-week custom roadmaps, voice mock interviews & priority internship access.</div>
    </div>
</div>
""", unsafe_allow_html=True)
            st.write("")
            if st.button("Mark All as Read", use_container_width=True):
                st.toast("✅ All notifications marked as read!")

    with h_col4:
        st.markdown(f"""
<div style='display: flex; align-items: center; gap: 10px; justify-content: flex-end;'>
    <div style='width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #8B5CF6, #10B981); display: flex; align-items: center; justify-content: center; font-weight: 700; color: white;'>
        {st.session_state.name[0] if st.session_state.name else 'Y'}
    </div>
    <div>
        <div style='font-weight: 600; color: #F8FAFC; font-size: 0.88rem;'>{st.session_state.name}</div>
        {member_badge_html}
    </div>
</div>
""", unsafe_allow_html=True)

# Instant Search Results Palette if user entered query
if search_query and search_query.strip():
    q = search_query.strip().lower()
    matching_careers = [c for c in recommendation.career_engine.CAREERS_DB.keys() if q in c.lower() or any(q in s.lower() for s in recommendation.career_engine.CAREERS_DB[c]["required_skills"])]
    page_shortcuts = {
        "AI Career Chat": ("💬 AI Career Chat", "Ask questions and get AI career guidance"),
        "Assessment": ("🎯 Assessment", "Calibrate your traits, preferences, and skills"),
        "Skill Gap": ("🧠 Skill Gap", "Analyze acquired skills vs skills to learn"),
        "Roadmap": ("📚 Roadmap", "Interactive 30/60/90-day learning roadmap"),
        "Resume Analyzer": ("📄 Resume Analyzer", "Upload your resume for instant ATS audit"),
        "Mock Interview": ("🎤 Mock Interview", "Interactive AI voice interview with scoring"),
        "Career Comparison": ("⚖️ Career Comparison", "Compare two careers head-to-head"),
        "Govt & Competitive Exams": ("🏛️ Govt & Competitive Exams", "UPSC, SSC CGL, Banking & Teaching hub"),
        "Jobs & Internships": ("💼 Jobs & Internships", "Explore curated live internships and jobs"),
        "Profile & Settings": ("👤 Profile & Settings", "Manage profile, XP, and subscriptions")
    }
    matching_pages = [(k, v[0], v[1]) for k, v in page_shortcuts.items() if q in k.lower() or q in v[1].lower()]

    with st.expander(f"🔍 Search Results for '{search_query}' ({len(matching_careers) + len(matching_pages)} found)", expanded=True):
        if not matching_careers and not matching_pages:
            st.info(f"No results found for '{search_query}'. Try searching for 'Python', 'UPSC', 'Interview', 'Resume', or 'Roadmap'.")
        else:
            if matching_pages:
                st.markdown("##### 🛠️ Matching Tools & Pages")
                p_cols = st.columns(min(len(matching_pages), 3))
                for idx, (p_name, nav_val, p_desc) in enumerate(matching_pages):
                    with p_cols[idx % 3]:
                        st.markdown(f"<div style='font-weight:600; color:#A78BFA; font-size:0.9rem;'>{p_name}</div><div style='font-size:0.75rem; color:#94A3B8; margin-bottom:6px;'>{p_desc}</div>", unsafe_allow_html=True)
                        def make_nav_cb(nv):
                            def cb():
                                st.session_state.nav_page = nv
                            return cb
                        st.button(f"Go to {p_name} ↗", key=f"search_nav_{p_name}", on_click=make_nav_cb(nav_val))
            if matching_careers:
                st.markdown("##### 🎯 Matching Careers")
                c_cols = st.columns(min(len(matching_careers), 3))
                for idx, c_name in enumerate(matching_careers[:6]):
                    c_data = recommendation.career_engine.CAREERS_DB[c_name]
                    with c_cols[idx % 3]:
                        st.markdown(f"""
<div class='glass-card' style='padding: 10px !important; margin-bottom: 6px;'>
    <div style='font-weight: 700; color: #F8FAFC; font-size: 0.88rem;'>{c_name}</div>
    <div style='font-size: 0.75rem; color: #34D399;'>💰 {c_data['salary']}</div>
</div>
""", unsafe_allow_html=True)
                        def make_career_cb(cn):
                            def cb():
                                st.session_state.nav_page = "📚 Roadmap"
                                st.session_state.target_roadmap_role = cn
                            return cb
                        st.button(f"View {c_name} ↗", key=f"search_c_{c_name}", on_click=make_career_cb(c_name))

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
logo_sidebar_html = f"<img src='data:image/png;base64,{logo_b64}' style='width: 78px; height: 78px; border-radius: 18px; margin-bottom: 10px; box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4); border: 1px solid rgba(139, 92, 246, 0.35);'>" if logo_b64 else ""
st.sidebar.markdown(f"""
<div style='text-align: center; padding: 10px 0 16px 0;'>
    {logo_sidebar_html}
    <div style='font-size: 1.3rem; font-weight: 800; color: #F8FAFC; margin-bottom: 2px;'>CareerPath AI</div>
    <span class='badge-have' style='font-size: 0.75rem;'>@{username}</span>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "🏠 Dashboard",
    "💬 AI Career Chat",
    "🎯 Assessment",
    "🧠 Skill Gap",
    "📚 Roadmap",
    "📄 Resume Analyzer",
    "🎤 Mock Interview",
    "⚖️ Career Comparison",
    "🏛️ Govt & Competitive Exams",
    "💼 Jobs & Internships",
    "👤 Profile & Settings"
]

if "nav_page" not in st.session_state or st.session_state.nav_page not in nav_options:
    st.session_state.nav_page = "🏠 Dashboard"

page = st.sidebar.radio(
    "Navigation",
    nav_options,
    key="nav_page",
    label_visibility="collapsed"
)

st.sidebar.divider()

# PRO UPGRADE / STATUS CARD AT SIDEBAR BOTTOM
if is_pro:
    st.sidebar.markdown("""
<div class='glass-card' style='padding: 16px !important; margin-top: 20px; border-color: rgba(16, 185, 129, 0.35) !important; background: rgba(16, 185, 129, 0.05);'>
<div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;'>
<div style='font-weight: 700; color: #34D399; font-size: 0.95rem;'>⚡ Pro Plan Active</div>
<span style='background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.4);'>PRO</span>
</div>
<p style='font-size: 0.8rem; color: #94A3B8; margin: 0; line-height: 1.4;'>All premium AI models, ATS analysis, and internship tools unlocked.</p>
</div>
""", unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
<div class='glass-card' style='padding: 16px !important; margin-top: 20px; border-color: rgba(139, 92, 246, 0.25) !important;'>
<div style='font-weight: 700; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 4px;'>🚀 Upgrade to Pro</div>
<p style='font-size: 0.8rem; color: #94A3B8; margin-bottom: 10px; line-height: 1.3;'>1 Month (₹499) &bull; 1 Year (₹3,999) &bull; 3 Years (₹7,999). Unlock full AI career acceleration.</p>
</div>
""", unsafe_allow_html=True)
    if st.sidebar.button("Upgrade to Pro ✨", use_container_width=True, type="primary"):
        show_subscription_modal()

if st.sidebar.button("🚪 Log Out"):
    st.session_state.username = None
    st.session_state.name = None
    st.rerun()

# =========================================================
# PAGE 1: 🏠 DASHBOARD MAIN VIEW
# =========================================================
if page == "🏠 Dashboard":
    # 5 REAL DYNAMIC TOP STATISTICS CARDS
    have_cnt = len(top_match['skills_gap'].get('already_have', []))
    total_cnt = have_cnt + len(top_match['skills_gap'].get('need_to_learn', []))
    skills_stat = f"{have_cnt} / {total_cnt}" if total_cnt > 0 else "0 / 0"
    skills_sub = f"{int(have_cnt/total_cnt*100)}% Matched" if total_cnt > 0 else "Pending Review"
    
    ats_score = st.session_state.get('latest_ats_score', None)
    ats_stat = f"{ats_score} / 100" if ats_score is not None else "-- / 100"
    ats_sub = "ATS Audited" if ats_score is not None else "Pending Scan"
    
    int_history = database.get_mock_interview_history(username)
    int_score = int(int_history[0]['score']) if int_history and int_history[0].get('score') else None
    int_stat = f"{int_score} / 100" if int_score is not None else "-- / 100"
    int_sub = "Latest Interview" if int_score is not None else "Not Tested"
    
    rm_tasks = database.get_roadmap_progress(username, top_match['career_name'])
    rm_count = len(rm_tasks) if rm_tasks else 0
    rm_stat = f"{rm_count} Tasks"
    rm_sub = "Milestones Done"

    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-left: 3px solid #8B5CF6;'>
            <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>Career Match</div>
            <div style='font-size: 1.8rem; font-weight: 800; color: #A78BFA; margin: 4px 0;'>{top_match['match_percentage']}%</div>
            <div style='font-size: 0.75rem; color: #34D399; font-weight: 600;'>{top_match['career_name']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-left: 3px solid #10B981;'>
            <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>Skills Acquired</div>
            <div style='font-size: 1.8rem; font-weight: 800; color: #34D399; margin: 4px 0;'>{skills_stat}</div>
            <div style='font-size: 0.75rem; color: #CBD5E1;'>{skills_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-left: 3px solid #10B981;'>
            <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>ATS Score</div>
            <div style='font-size: 1.8rem; font-weight: 800; color: #34D399; margin: 4px 0;'>{ats_stat}</div>
            <div style='font-size: 0.75rem; color: #34D399;'>{ats_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-left: 3px solid #8B5CF6;'>
            <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>Interview Score</div>
            <div style='font-size: 1.8rem; font-weight: 800; color: #A78BFA; margin: 4px 0;'>{int_stat}</div>
            <div style='font-size: 0.75rem; color: #A78BFA;'>{int_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-left: 3px solid #8B5CF6;'>
            <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>Learning Progress</div>
            <div style='font-size: 1.8rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;'>{rm_stat}</div>
            <div style='font-size: 0.75rem; color: #34D399;'>{rm_sub}</div>
        </div>
        """, unsafe_allow_html=True)

    # MAIN DASHBOARD GRID
    col_left, col_right = st.columns([1.8, 1])

    with col_left:
        # AI CAREER ASSISTANT CHAT CARD
        st.markdown("""
        <div class='glass-card'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;'>
                <div>
                    <h3 style='margin: 0; color: #F8FAFC; font-size: 1.25rem;'>🤖 AI Career Assistant</h3>
                    <p style='margin: 2px 0 0 0; font-size: 0.85rem; color: #94A3B8;'>Your personalized career guidance companion</p>
                </div>
                <span class='badge-have'>Online & Ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Load Chat History for Dashboard Chat Box
        chat_history = database.get_chat_history(username)
        if not chat_history:
            st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.02); border-radius: 12px; padding: 14px; margin-bottom: 12px; border: 1px solid rgba(139, 92, 246, 0.2);'>
                <span style='color: #A78BFA; font-weight: 700;'>🤖 AI Assistant:</span>
                <p style='margin: 4px 0 0 0; color: #CBD5E1; font-size: 0.95rem;'>Hello! I'm your CareerPath AI assistant. How can I help you accelerate your trajectory today?</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in chat_history[-4:]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        profile_ctx = {
            "name": st.session_state.name,
            "logic": logic,
            "creativity": creativity,
            "communication": communication,
            "skills": user_skills,
            "recommended_career": top_match["career_name"],
            "match_percentage": top_match["match_percentage"]
        }

        # Chat Input Field Fix
        user_input_text = st.chat_input("Tell me about your interests, goals, or career questions...")
        if user_input_text:
            with st.chat_message("user"):
                st.write(user_input_text)
            with st.chat_message("assistant"):
                with st.spinner("AI is analyzing your query..."):
                    reply = ai_chat.generate_chat_response(username, user_input_text, chat_history, profile_ctx)
                    st.write(reply)
                    database.add_user_xp(username, 20)
                    speak_ai(reply)
                    st.rerun()

        # SKILL GAP ANALYSIS CARD
        gap_info = top_match.get("skills_gap", {"already_have": ["Python", "SQL", "Git"], "need_to_learn": ["Machine Learning", "Deep Learning", "TensorFlow"]})
        already_badges = "".join([f"<span class='badge-have'>{s}</span>" for s in gap_info["already_have"]])
        need_badges = "".join([f"<span class='badge-need'>{s}</span>" for s in gap_info["need_to_learn"]])

        st.markdown(f"""
        <div class='glass-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                <h3 style='margin: 0; color: #F8FAFC;'>🧠 Skill Gap Analysis</h3>
                <span style='color: #34D399; font-weight: 700; font-size: 0.9rem;'>Skill Completion: 67%</span>
            </div>
            <div style='background: rgba(255, 255, 255, 0.08); border-radius: 999px; height: 10px; width: 100%; margin-bottom: 16px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #8B5CF6, #10B981); height: 100%; width: 67%;'></div>
            </div>
            <div style='margin-bottom: 12px;'>
                <div style='font-size: 0.85rem; color: #CBD5E1; font-weight: 600; margin-bottom: 4px;'>✅ Acquired Skills:</div>
                <div>{already_badges}</div>
            </div>
            <div>
                <div style='font-size: 0.85rem; color: #CBD5E1; font-weight: 600; margin-bottom: 4px;'>📚 Missing Skills to Learn:</div>
                <div>{need_badges}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 90-DAY LEARNING ROADMAP PREVIEW
        st.markdown("""
        <div class='glass-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;'>
                <h3 style='margin: 0; color: #F8FAFC;'>📚 90-Day Learning Roadmap</h3>
                <span style='color: #A78BFA; font-size: 0.85rem; font-weight: 600;'>View Full Roadmap →</span>
            </div>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;'>
                <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 12px; border-radius: 12px;'>
                    <div style='color: #34D399; font-weight: 700; font-size: 0.85rem;'>Week 1–2</div>
                    <div style='font-size: 0.78rem; color: #F8FAFC; margin-top: 4px;'>Python & Fundamentals</div>
                    <div style='color: #34D399; font-size: 0.75rem; margin-top: 6px;'>✓ Completed</div>
                </div>
                <div style='background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.35); padding: 12px; border-radius: 12px;'>
                    <div style='color: #A78BFA; font-weight: 700; font-size: 0.85rem;'>Week 3–6</div>
                    <div style='font-size: 0.78rem; color: #F8FAFC; margin-top: 4px;'>Machine Learning Basics</div>
                    <div style='color: #A78BFA; font-size: 0.75rem; margin-top: 6px;'>⚡ In Progress</div>
                </div>
                <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); padding: 12px; border-radius: 12px;'>
                    <div style='color: #94A3B8; font-weight: 700; font-size: 0.85rem;'>Week 7–10</div>
                    <div style='font-size: 0.78rem; color: #CBD5E1; margin-top: 4px;'>Deep Learning</div>
                    <div style='color: #64748B; font-size: 0.75rem; margin-top: 6px;'>Upcoming</div>
                </div>
                <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); padding: 12px; border-radius: 12px;'>
                    <div style='color: #94A3B8; font-weight: 700; font-size: 0.85rem;'>Week 11–13</div>
                    <div style='font-size: 0.78rem; color: #CBD5E1; margin-top: 4px;'>Capstone Projects</div>
                    <div style='color: #64748B; font-size: 0.75rem; margin-top: 6px;'>Upcoming</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # QUICK ACTIONS
        st.markdown("### ⚡ Quick Actions")
        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            if st.button("📄 Resume Audit"):
                st.session_state.page = "📄 Resume Analyzer"
        with qa2:
            if st.button("🎤 Mock Interview"):
                st.session_state.page = "🎤 Mock Interview"
        with qa3:
            if st.button("📚 View Roadmap"):
                st.session_state.page = "📚 Roadmap"
        with qa4:
            if st.button("⚖️ Compare Roles"):
                st.session_state.page = "⚖️ Career Comparison"

    with col_right:
        # CAREER MATCH CIRCLE CARD
        match_pct = int(top_match['match_percentage'])
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <h4 style='margin-top: 0; color: #F8FAFC;'>🏆 Primary Match Circle</h4>
            <div class='score-circle' style='--percentage: {match_pct}%; margin: 16px auto;'>
                <span>{match_pct}%</span>
            </div>
            <div style='font-weight: 700; font-size: 1.1rem; color: #A78BFA;'>{top_match['career_name']}</div>
            <p style='font-size: 0.82rem; color: #94A3B8; margin-top: 4px;'>Based on your skills & multi-vector personality audit.</p>
        </div>
        """, unsafe_allow_html=True)

        # VOICE ASSISTANT CARD
        st.markdown("""
        <div class='glass-card'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;'>
                <div style='font-weight: 700; color: #F8FAFC; font-size: 0.95rem;'>🎤 Voice Assistant</div>
                <span style='color: #34D399; font-size: 0.8rem; font-weight: 600;'>● Listening...</span>
            </div>
            <p style='font-size: 0.8rem; color: #94A3B8; margin-bottom: 10px;'>Dictate queries using real-time browser speech recognition.</p>
        </div>
        """, unsafe_allow_html=True)
        voice_chat_dash = voice_input_component(key="voice_dash_dictate")
        if voice_chat_dash:
            with st.spinner("Processing spoken input..."):
                reply = ai_chat.generate_chat_response(username, voice_chat_dash, chat_history, profile_ctx)
                speak_ai(reply)
                st.rerun()

        # TOP CAREER MATCHES LIST
        st.markdown("<div class='glass-card'><h4 style='margin-top:0; color:#F8FAFC;'>💼 Top Career Matches</h4>", unsafe_allow_html=True)
        for m in matches[:5]:
            pct = int(m['match_percentage'])
            st.markdown(f"""
            <div style='margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; color: #CBD5E1; margin-bottom: 3px;'>
                    <span>🤖 {m['career_name']}</span>
                    <span style='color: #34D399;'>{pct}%</span>
                </div>
                <div style='background: rgba(255, 255, 255, 0.08); border-radius: 999px; height: 6px; width: 100%; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #8B5CF6, #10B981); height: 100%; width: {pct}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # RECOMMENDED COURSES CARD (CLICKABLE DIRECT TO PLATFORMS)
        if hasattr(utils, "get_recommended_courses_for_career"):
            rec_courses = utils.get_recommended_courses_for_career(top_match.get("career_name", "AI Engineer"))
        else:
            rec_courses = [
                {"title": "Machine Learning Specialization", "instructor": "by Andrew Ng • Coursera", "link": "https://www.coursera.org/specializations/machine-learning-introduction", "platform": "Coursera"},
                {"title": "Deep Learning A-Z™", "instructor": "by Kirill Eremenko • Udemy", "link": "https://www.udemy.com/course/deeplearning/", "platform": "Udemy"},
                {"title": "Python for Data Science", "instructor": "by IBM • Coursera", "link": "https://www.coursera.org/learn/python-for-applied-data-science-ai", "platform": "Coursera"}
            ]
        courses_html = ""
        for c in rec_courses:
            courses_html += f"""<a href="{c['link']}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; display: block; padding: 10px 12px; margin-bottom: 8px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; transition: all 0.2s ease;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 700; color: #A78BFA; font-size: 0.88rem;">{c['title']}</div>
<span style="color: #34D399; font-size: 0.82rem; font-weight: 700;">↗</span>
</div>
<div style="color: #94A3B8; font-size: 0.76rem; margin-top: 3px; display: flex; justify-content: space-between; align-items: center;">
<span>{c['instructor']}</span>
<span style="background: rgba(139, 92, 246, 0.15); color: #C4B5FD; padding: 1px 6px; border-radius: 4px; font-size: 0.68rem; font-weight: 600;">{c['platform']}</span>
</div>
</a>"""

        st.markdown(f"""<div class='glass-card'>
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
<h4 style='margin: 0; color: #F8FAFC;'>🎓 Recommended Courses</h4>
<span style='font-size: 0.72rem; color: #34D399; background: rgba(16, 185, 129, 0.1); padding: 2px 8px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25); font-weight: 600;'>Visit Course ↗</span>
</div>
{courses_html}
</div>""", unsafe_allow_html=True)

        # MOTIVATIONAL QUOTE CARD (Changes per user + rotating)
        if "quote_offset" not in st.session_state:
            st.session_state.quote_offset = 0
            
        user_quote = utils.get_quote_for_user(username, st.session_state.quote_offset)
        
        st.markdown(f"""
        <div class='glass-card' style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(16, 185, 129, 0.08)) !important;'>
            <div style='font-style: italic; color: #CBD5E1; font-size: 0.88rem; line-height: 1.5;'>
                "{user_quote['quote']}"
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 10px;'>
                <span style='font-size: 0.72rem; color: #94A3B8;'>Daily Wisdom for @{username}</span>
                <span style='color: #34D399; font-weight: 600; font-size: 0.8rem;'>— {user_quote['author']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Next Quote", key="btn_next_quote", help="Cycle to another inspirational quote"):
            st.session_state.quote_offset += 1
            st.rerun()

# =========================================================
# PAGE 2: 💬 AI CAREER CHAT
# =========================================================
elif page == "💬 AI Career Chat":
    st.subheader("💬 AI Career Assistant")
    st.info("Stateful conversation with Gemini. History is persisted in SQLite database.")
    
    if st.button("Clear Chat Log"):
        database.clear_chat_history(username)
        st.success("Chat history cleared!")
        st.rerun()

    st.write("##### 🎙️ Dictate Chat Message Directly")
    voice_chat_text = voice_input_component(key="voice_chat_page")

    chat_history = database.get_chat_history(username)
    for msg in chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    profile_ctx = {
        "name": st.session_state.name,
        "logic": logic,
        "creativity": creativity,
        "communication": communication,
        "skills": user_skills,
        "recommended_career": top_match["career_name"],
        "match_percentage": top_match["match_percentage"]
    }

    user_prompt = None
    if voice_chat_text:
        user_prompt = voice_chat_text

    chat_text_input = st.chat_input("Ask any career, salary, skill, or interview question...")
    if chat_text_input:
        user_prompt = chat_text_input

    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI Assistant is formulating a response..."):
                reply = ai_chat.generate_chat_response(username, user_prompt, chat_history, profile_ctx)
                st.write(reply)
                database.add_user_xp(username, 20)
                speak_ai(reply)
                st.rerun()

# =========================================================
# PAGE 3: 🎯 ASSESSMENT
# =========================================================
elif page == "🎯 Assessment":
    st.subheader("🎯 Multi-Vector Personality & Skill Assessment")
    st.info("Tune your traits and interests to re-calculate weighted career matching scores.")

    col_input, col_metric = st.columns([1.3, 1])

    with col_input:
        with st.container(border=True):
            st.write("### 🎛️ Adjust Personality Traits")
            new_logic = st.slider("Logical Thinking & Problem Solving", 1, 10, logic)
            new_creativity = st.slider("Creativity & Innovation", 1, 10, creativity)
            new_communication = st.slider("Communication & Interpersonal Skills", 1, 10, communication)

            st.write("### 🛠️ Input Current Skills")
            new_skills = st.text_input("Enter comma-separated skills", user_skills)

            st.write("### 🎯 Professional Preferences")
            pref_work = st.selectbox("Preferred Work Environment", ["Remote", "Office", "Hybrid"], index=["Remote", "Office", "Hybrid"].index(preferences.get("work_style", "Hybrid")))
            pref_subjects = st.multiselect("Favorite Focus Areas", ["Coding", "Mathematics", "Design", "Strategy", "Security", "Hardware"], default=preferences.get("fav_subjects", ["Coding"]))
            dream_comp = st.text_input("Dream Company", preferences.get("dream_company", ""))
            dream_role = st.text_input("Dream Role", preferences.get("dream_role", ""))

            pref_math = st.checkbox("Quantitative mathematical problems", value=preferences.get("interest_math", False))
            pref_speaking = st.checkbox("Public speaking tasks", value=preferences.get("public_speaking", False))
            pref_team = st.checkbox("Team collaboration", value=preferences.get("team_work", False))

            if st.button("Save Profile & Re-calculate"):
                new_pref = {
                    "work_style": pref_work,
                    "fav_subjects": pref_subjects,
                    "dream_company": dream_comp,
                    "dream_role": dream_role,
                    "interest_math": pref_math,
                    "public_speaking": pref_speaking,
                    "team_work": pref_team
                }
                database.update_user_profile(
                    username, st.session_state.name, new_skills,
                    new_logic, new_creativity, new_communication, new_pref
                )
                st.success("Profile saved!")
                st.rerun()

    with col_metric:
        with st.container(border=True):
            st.write("### 📊 Alignment Radar Visualization")
            current_pref = {
                "work_style": pref_work,
                "fav_subjects": pref_subjects,
                "dream_company": dream_comp,
                "dream_role": dream_role,
                "interest_math": pref_math,
                "public_speaking": pref_speaking,
                "team_work": pref_team
            }
            matches = recommendation.calculate_intelligent_recommendations(
                new_logic, new_creativity, new_communication, new_skills, current_pref
            )
            if matches:
                best = matches[0]
                st.metric("Top Career Recommendation", best['career_name'], f"{best['match_percentage']}% Match")
                career_details = recommendation.career_engine.CAREERS_DB[best['career_name']]
                fig_radar = dashboard.generate_plotly_radar(
                    {"logic": new_logic, "creativity": new_creativity, "communication": new_communication},
                    career_details["ideal_traits"],
                    best['career_name']
                )
                st.plotly_chart(fig_radar, use_container_width=True)

# =========================================================
# PAGE 4: 🧠 SKILL GAP
# =========================================================
elif page == "🧠 Skill Gap":
    st.subheader("🧠 Skill Gap Analysis")
    selected_career = st.selectbox("Select Role to Analyze", [m["career_name"] for m in matches])
    if selected_career:
        c_data = next(x for x in matches if x["career_name"] == selected_career)
        gap = c_data["skills_gap"]
        match_pct = c_data["match_percentage"]
        
        # Match Overview Header Card
        st.markdown(f"""
        <div class='glass-card' style='margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;'>
                <div>
                    <span style='font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;'>Role Assessment</span>
                    <h3 style='margin: 4px 0 0 0; color: #F8FAFC; font-weight: 800;'>{selected_career}</h3>
                </div>
                <div style='text-align: right;'>
                    <span style='font-size: 0.85rem; color: #34D399; font-weight: 700; text-transform: uppercase;'>Match Alignment</span>
                    <div style='font-size: 1.8rem; font-weight: 800; color: #34D399; line-height: 1.1;'>{match_pct}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Build badges HTML
        if gap["already_have"]:
            have_badges = "".join([f"<span class='badge-have'>{s}</span>" for s in gap["already_have"]])
        else:
            have_badges = "<p style='color: #94A3B8; font-size: 0.88rem; font-style: italic; margin: 8px 0;'>No matching acquired skills recorded for this role yet.</p>"
            
        if gap["need_to_learn"]:
            need_badges = "".join([f"<span class='badge-need'>{s}</span>" for s in gap["need_to_learn"]])
        else:
            need_badges = "<p style='color: #34D399; font-size: 0.88rem; font-style: italic; margin: 8px 0;'>🎉 You have already acquired all the key skills required for this role!</p>"
            
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown(f"""
            <div class='glass-card' style='height: 100%; min-height: 180px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                    <h4 style='margin: 0; color: #34D399;'>✅ Acquired Skills</h4>
                    <span style='background: rgba(16, 185, 129, 0.15); color: #34D399; padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700;'>
                        {len(gap["already_have"])} Skills
                    </span>
                </div>
                <div style='display: flex; flex-wrap: wrap; gap: 4px;'>
                    {have_badges}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_g2:
            st.markdown(f"""
            <div class='glass-card' style='height: 100%; min-height: 180px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                    <h4 style='margin: 0; color: #A78BFA;'>📚 Skills to Learn</h4>
                    <span style='background: rgba(139, 92, 246, 0.15); color: #A78BFA; padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700;'>
                        {len(gap["need_to_learn"])} Skills
                    </span>
                </div>
                <div style='display: flex; flex-wrap: wrap; gap: 4px;'>
                    {need_badges}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Interactive Skills Management for this role
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("### ⚡ Add & Update Skills for this Role")
        st.markdown("Already have experience in any of the required skills? Mark them below to instantly update your match alignment:")

        col_u1, col_u2 = st.columns([1.5, 1], gap="medium")
        with col_u1:
            if gap["need_to_learn"]:
                skills_to_add = st.multiselect(
                    "Select skills you already know from the required list:",
                    gap["need_to_learn"],
                    placeholder="Choose skills to mark as acquired..."
                )
                if st.button("✅ Mark Selected Skills as Acquired", type="primary"):
                    if skills_to_add:
                        current_skills = [s.strip() for s in user_skills.split(",") if s.strip()]
                        for s in skills_to_add:
                            if s not in current_skills:
                                current_skills.append(s)
                        updated_skills_str = ", ".join(current_skills)
                        database.update_user_profile(
                            username, st.session_state.name, updated_skills_str,
                            logic, creativity, communication, preferences
                        )
                        st.success(f"🎉 Successfully added {len(skills_to_add)} skills to your profile!")
                        st.rerun()
                    else:
                        st.warning("Please select at least one skill to add.")
            else:
                st.info("🎉 You have already acquired all the required skills for this role!")

        with col_u2:
            custom_skill = st.text_input("Add any other skill:", placeholder="e.g. Python, SQL, Excel, Reasoning...")
            if st.button("➕ Add Custom Skill"):
                if custom_skill.strip():
                    current_skills = [s.strip() for s in user_skills.split(",") if s.strip()]
                    new_s = custom_skill.strip()
                    if new_s not in current_skills:
                        current_skills.append(new_s)
                        updated_skills_str = ", ".join(current_skills)
                        database.update_user_profile(
                            username, st.session_state.name, updated_skills_str,
                            logic, creativity, communication, preferences
                        )
                        st.success(f"🎉 Added '{new_s}' to your profile!")
                        st.rerun()
                    else:
                        st.info(f"'{new_s}' is already in your skills profile.")
                else:
                    st.warning("Please enter a skill name.")

        # Call-to-action button to generate roadmap
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        def navigate_to_roadmap(target_career):
            st.session_state.nav_page = "📚 Roadmap"
            st.session_state.target_roadmap_role = target_career

        st.button(
            f"🚀 Launch Learning Roadmap for {selected_career}",
            use_container_width=True,
            type="primary",
            on_click=navigate_to_roadmap,
            args=(selected_career,)
        )

# =========================================================
# PAGE 5: 📚 ROADMAP
# =========================================================
elif page == "📚 Roadmap":
    st.subheader("📚 Dynamic Learning Roadmap")
    career_list = [m["career_name"] for m in matches]
    target_role = st.session_state.get("target_roadmap_role", career_list[0] if career_list else "AI Engineer")
    target_idx = career_list.index(target_role) if target_role in career_list else 0
    selected_career = st.selectbox("Select Target Role for Curriculum", career_list, index=target_idx)
    duration = st.selectbox("Roadmap Duration", [30, 60, 90], format_func=lambda x: f"{x}-Day Roadmap", index=1)
    
    # Auto-load existing roadmap for this career if available
    roadmap_key = f"roadmap_{selected_career}"
    if roadmap_key not in st.session_state:
        history = database.get_career_history(username)
        for h in history:
            if h["career_name"] == selected_career and h.get("roadmap"):
                st.session_state[roadmap_key] = h["roadmap"]
                break

    has_existing = roadmap_key in st.session_state and bool(st.session_state[roadmap_key])
    btn_label = "⚡ Regenerate Learning Roadmap via Gemini" if has_existing else "✨ Generate Learning Roadmap via Gemini"
    
    if st.button(btn_label):
        with st.spinner("AI is constructing your custom curriculum..."):
            gap = next(x for x in matches if x["career_name"] == selected_career)["skills_gap"]
            ai_rm = roadmap.generate_custom_roadmap(selected_career, gap["already_have"], gap["need_to_learn"], duration)
            database.save_career_result(username, selected_career, 90.0, gap, ai_rm, "")
            st.session_state[roadmap_key] = ai_rm
            st.success("Roadmap generated successfully!")
            st.rerun()

    # Render interactive roadmap UI
    current_rm = st.session_state.get(roadmap_key)
    if current_rm:
        roadmap.render_roadmap_ui(current_rm, username, selected_career)
    else:
        st.info(f"💡 Select your duration and click 'Generate Learning Roadmap via Gemini' to create your personalized curriculum for **{selected_career}**.")

# =========================================================
# PAGE 6: 📄 RESUME ANALYZER
# =========================================================
elif page == "📄 Resume Analyzer":
    st.subheader("📄 ATS Resume Scanner & Auditor")
    target_role = st.selectbox("Target Career Track", list(recommendation.career_engine.CAREERS_DB.keys()))
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Analyze Resume ATS Score"):
            with st.spinner("Scanning resume against ATS rules..."):
                feedback = resume_analyzer.analyze_resume_ats(target_role, uploaded_file)
                st.session_state['latest_resume_feedback'] = feedback
                st.session_state['latest_resume_role'] = target_role
                
                # Extract numeric score if present
                import re
                score_match = re.search(r"(?:ATS Compatibility Score|ATS Score|Score)[^\d]*(\d{1,3})", feedback, re.IGNORECASE)
                if score_match:
                    score_val = min(100, int(score_match.group(1)))
                    st.session_state['latest_ats_score'] = score_val

    # Display feedback if available in session state
    saved_feedback = st.session_state.get('latest_resume_feedback')
    if saved_feedback:
        saved_score = st.session_state.get('latest_ats_score', 80)
        score_color = "#34D399" if saved_score >= 75 else "#FBBF24" if saved_score >= 50 else "#F87171"
        st.markdown(f"""
        <div class='glass-card' style='margin: 16px 0;'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;'>
                <div>
                    <h3 style='margin: 0; color: #F8FAFC;'>ATS Audit Report</h3>
                    <p style='margin: 2px 0 0 0; font-size: 0.88rem; color: #94A3B8;'>Target Track: <b>{st.session_state.get('latest_resume_role', target_role)}</b></p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 2rem; font-weight: 800; color: {score_color}; line-height: 1;'>{saved_score}/100</div>
                    <div style='font-size: 0.78rem; color: #CBD5E1; text-transform: uppercase; font-weight: 600;'>Compatibility Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(saved_feedback)

# =========================================================
# PAGE 7: 🎤 MOCK INTERVIEW
# =========================================================
elif page == "🎤 Mock Interview":
    st.subheader("🎤 AI Mock Interview Room")
    mock_state = st.session_state.mock_interview

    if not mock_state["active"]:
        target_role = st.selectbox("Target Role", list(recommendation.career_engine.CAREERS_DB.keys()))
        persona = st.selectbox("Interviewer Style", ["Standard Recruiter", "Strict Tech Lead", "Friendly HR Recruiter"])

        if st.button("Start Mock Interview"):
            first_q = f"Hello! Welcome to your interview for {target_role}. Could you introduce yourself and explain why you're interested in this role?"
            st.session_state.mock_interview = {
                "active": True,
                "career_name": target_role,
                "persona": persona,
                "history": [{"type": "question", "text": first_q}],
                "current_question": first_q,
                "question_count": 1,
                "evaluation": ""
            }
            speak_ai(first_q)
            st.rerun()
    else:
        st.write(f"**Interviewing For:** `{mock_state['career_name']}` | Question {mock_state['question_count']} of 5")
        st.markdown(f"<div class='glass-card'><p style='color:#A78BFA; font-weight:700;'>Interviewer:</p><p>{mock_state['current_question']}</p></div>", unsafe_allow_html=True)
        speak_ai(mock_state['current_question'])

        user_ans = st.text_area("Your Response:")
        if st.button("Submit Answer"):
            if user_ans.strip():
                st.session_state.mock_interview["history"].append({"type": "answer", "text": user_ans})
                if mock_state["question_count"] < 5:
                    next_q = interview.get_next_question(mock_state["career_name"], st.session_state.mock_interview["history"], mock_state["persona"])
                    st.session_state.mock_interview["history"].append({"type": "question", "text": next_q})
                    st.session_state.mock_interview["question_count"] += 1
                    st.session_state.mock_interview["current_question"] = next_q
                    st.rerun()
                else:
                    scorecard = interview.evaluate_interview_performance(mock_state["career_name"], st.session_state.mock_interview["history"])
                    database.save_mock_interview(username, mock_state["career_name"], scorecard, 91.0)
                    st.session_state.mock_interview["active"] = False
                    st.session_state.mock_interview["evaluation"] = scorecard
                    st.success("Interview complete!")
                    st.markdown(scorecard)

# =========================================================
# PAGE 8: ⚖️ CAREER COMPARISON
# =========================================================
# =========================================================
# PAGE 8: ⚖️ CAREER COMPARISON
# =========================================================
elif page == "⚖️ Career Comparison":
    st.subheader("⚖️ Head-to-Head Role Showdown")
    col1, col2 = st.columns(2)
    with col1:
        role_a = st.selectbox("Select Role A", list(recommendation.career_engine.CAREERS_DB.keys()), index=0)
        meta_a = recommendation.career_engine.CAREERS_DB[role_a]
    with col2:
        role_b = st.selectbox("Select Role B", list(recommendation.career_engine.CAREERS_DB.keys()), index=1)
        meta_b = recommendation.career_engine.CAREERS_DB[role_b]

    # Side-by-side metric comparison cards
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #8B5CF6;'>
            <h3 style='margin: 0 0 10px 0; color: #A78BFA;'>{role_a}</h3>
            <p style='margin: 4px 0;'>💰 <b>Salary Range:</b> <span style='color: #34D399;'>{meta_a['salary']}</span></p>
            <p style='margin: 4px 0;'>📈 <b>Market Growth:</b> {meta_a['growth']}</p>
            <p style='margin: 4px 0;'>🔥 <b>Industry Demand:</b> {meta_a['demand']}</p>
            <p style='margin: 4px 0;'>🏢 <b>Typical Work Style:</b> {meta_a.get('work_style', 'Flexible')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 3px solid #3B82F6;'>
            <h3 style='margin: 0 0 10px 0; color: #60A5FA;'>{role_b}</h3>
            <p style='margin: 4px 0;'>💰 <b>Salary Range:</b> <span style='color: #34D399;'>{meta_b['salary']}</span></p>
            <p style='margin: 4px 0;'>📈 <b>Market Growth:</b> {meta_b['growth']}</p>
            <p style='margin: 4px 0;'>🔥 <b>Industry Demand:</b> {meta_b['demand']}</p>
            <p style='margin: 4px 0;'>🏢 <b>Typical Work Style:</b> {meta_b.get('work_style', 'Flexible')}</p>
        </div>
        """, unsafe_allow_html=True)

    # 3-Way Trait Comparison Radar Chart
    st.markdown("### 📊 Trait Alignment Comparison")
    comp_fig = dashboard.generate_comparison_radar(
        role_a, meta_a["ideal_traits"],
        role_b, meta_b["ideal_traits"],
        {"logic": logic, "creativity": creativity, "communication": communication}
    )
    st.plotly_chart(comp_fig, use_container_width=True)

    # Skills Venn Breakdown
    st.markdown("### 🧩 Skills Breakdown & Overlap")
    skills_a = set(meta_a.get("required_skills", []))
    skills_b = set(meta_b.get("required_skills", []))
    shared_skills = skills_a.intersection(skills_b)
    unique_a = skills_a - skills_b
    unique_b = skills_b - skills_a

    c_v1, c_v2, c_v3 = st.columns(3)
    with c_v1:
        st.markdown(f"<div class='glass-card'><h4 style='color: #A78BFA; margin-top:0;'>Unique to {role_a}</h4>", unsafe_allow_html=True)
        for s in unique_a:
            st.markdown(f"<span class='badge-need'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c_v2:
        st.markdown("<div class='glass-card'><h4 style='color: #34D399; margin-top:0;'>🤝 Shared Skills</h4>", unsafe_allow_html=True)
        for s in shared_skills:
            st.markdown(f"<span class='badge-have'>{s}</span>", unsafe_allow_html=True)
        if not shared_skills:
            st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>No direct skill overlap.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c_v3:
        st.markdown(f"<div class='glass-card'><h4 style='color: #60A5FA; margin-top:0;'>Unique to {role_b}</h4>", unsafe_allow_html=True)
        for s in unique_b:
            st.markdown(f"<span class='badge-need' style='border-color: rgba(59, 130, 246, 0.4); color: #93C5FD;'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PAGE 9: 🏛️ GOVT & COMPETITIVE EXAMS
# =========================================================
elif page == "🏛️ Govt & Competitive Exams":
    st.subheader("🏛️ Government & Competitive Exams Hub")
    st.markdown("Comprehensive blueprints, 12-month phased roadmaps, syllabus breakdowns, and AI answer evaluations for Civil Services, SSC, Banking, Teaching, Defense, and CA aspirants.")

    selected_exam_key = st.selectbox(
        "🎯 Select Target Examination Track:",
        govt_exams.get_all_exams()
    )
    exam = govt_exams.get_exam_details(selected_exam_key)

    if exam:
        # Hero card for the selected exam
        st.markdown(f"""
<div class='glass-card' style='border-left: 4px solid #8B5CF6; margin-bottom: 20px;'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;'>
<div>
<h3 style='color: #F8FAFC; margin: 0 0 6px 0;'>{selected_exam_key}</h3>
<div style='color: #A78BFA; font-weight: 600; font-size: 0.9rem;'>Conducting Body: {exam['authority']}</div>
</div>
<div>
<a href='{exam['official_url']}' target='_blank' style='text-decoration: none;'>
<button style='background: linear-gradient(135deg, #8B5CF6, #10B981); color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 0.85rem; cursor: pointer; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);'>Official Portal ↗</button>
</a>
</div>
</div>
<p style='color: #CBD5E1; font-size: 0.9rem; margin: 12px 0; line-height: 1.5;'>{exam['overview']}</p>
<div style='display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;'>
<span style='background: rgba(16, 185, 129, 0.15); color: #34D399; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 700;'>💰 {exam['salary_range']}</span>
<span style='background: rgba(255, 255, 255, 0.05); color: #CBD5E1; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem;'>🎓 {exam['eligibility']}</span>
<span style='background: rgba(255, 255, 255, 0.05); color: #CBD5E1; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem;'>⏳ Age: {exam['age_limit']}</span>
<span style='background: rgba(255, 255, 255, 0.05); color: #CBD5E1; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem;'>🔄 Attempts: {exam['attempts']}</span>
</div>
</div>
""", unsafe_allow_html=True)

        tab_blueprint, tab_roadmap, tab_ai_eval, tab_portals = st.tabs([
            "📋 Stages & Syllabus",
            "🗺️ 12-Month Preparation Roadmap",
            "✍️ AI Answer Writing & Evaluator",
            "🌐 Official Portals & Resources"
        ])

        with tab_blueprint:
            st.markdown("#### 🎯 Examination Stages & Architecture")
            col_stages = st.columns(len(exam['stages']))
            for idx, stage in enumerate(exam['stages']):
                with col_stages[idx]:
                    st.markdown(f"""
<div class='glass-card' style='height: 100%;'>
<div style='font-weight: 700; color: #A78BFA; font-size: 0.95rem; margin-bottom: 8px;'>{stage['stage']}</div>
<p style='color: #CBD5E1; font-size: 0.85rem; line-height: 1.5; margin: 0;'>{stage['details']}</p>
</div>
""", unsafe_allow_html=True)

            st.markdown("<h4 style='margin-top: 24px;'>📚 Core Syllabus Breakdown</h4>", unsafe_allow_html=True)
            cols_s = st.columns(2)
            for idx, item in enumerate(exam['syllabus_highlights']):
                with cols_s[idx % 2]:
                    st.markdown(f"""
<div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; color: #F8FAFC; font-size: 0.9rem;'>
📌 {item}
</div>
""", unsafe_allow_html=True)

        with tab_roadmap:
            st.markdown("#### 🗺️ Strategic 12-Month Phased Roadmap")
            st.markdown("Track your step-by-step preparation journey from fundamentals to exam day:")

            for p_idx, phase in enumerate(exam['roadmap_phases']):
                with st.expander(f"📍 {phase['phase']}", expanded=(p_idx == 0)):
                    for g_idx, goal in enumerate(phase['goals']):
                        st.checkbox(goal, key=f"govt_goal_{selected_exam_key}_{p_idx}_{g_idx}")

        with tab_ai_eval:
            st.markdown("#### ✍️ AI Subjective Answer & Essay Evaluator")
            st.markdown("Practice real exam-standard questions and receive instant constructive evaluation on **structure, content accuracy, missing dimensions, and scoring** out of 10.")

            q_options = [q["question"] for q in exam['sample_questions']] + ["✍️ Custom Question (Write your own)"]
            selected_q = st.selectbox("Select a Practice Question or Enter Your Own:", q_options)

            if selected_q == "✍️ Custom Question (Write your own)":
                question_text = st.text_input("Enter Question Title / Topic:", placeholder="e.g. Discuss the separation of powers under the Indian Constitution...")
            else:
                question_text = selected_q

            aspirant_answer = st.text_area(
                "Write or Paste Your Answer Below (Recommended: 150 - 250 words):",
                height=180,
                placeholder="Start typing your structured answer here (Introduction, Core Body Points, Conclusion)..."
            )

            if st.button("✨ Evaluate My Answer with AI", type="primary", use_container_width=True):
                if not aspirant_answer.strip():
                    st.warning("⚠️ Please enter your answer text before submitting for evaluation.")
                else:
                    with st.spinner("Analyzing answer structure, factual accuracy, and scoring against exam benchmarks..."):
                        evaluation_feedback = govt_exams.evaluate_aspirant_answer(
                            selected_exam_key, question_text, aspirant_answer
                        )
                        st.markdown(f"""
<div class='glass-card' style='border-color: rgba(139, 92, 246, 0.4); margin-top: 16px;'>
<h3 style='color: #A78BFA; margin-top: 0;'>📝 AI Evaluation Report</h3>
{evaluation_feedback}
</div>
""", unsafe_allow_html=True)

        with tab_portals:
            st.markdown("#### 🌐 Official Examination Authorities & Direct Portals")
            p_col1, p_col2, p_col3 = st.columns(3)
            portals = [
                {"name": "UPSC Official Portal", "desc": "Civil Services, NDA, CDS notifications & syllabus", "url": "https://upsc.gov.in"},
                {"name": "SSC Official Portal", "desc": "CGL, CHSL, CPO notifications & calendar", "url": "https://ssc.gov.in"},
                {"name": "IBPS Portal", "desc": "Bank PO, Clerk & Specialist Officer examinations", "url": "https://www.ibps.in"},
                {"name": "RBI Opportunities", "desc": "Reserve Bank of India Grade B Managerial recruitments", "url": "https://opportunities.rbi.org.in"},
                {"name": "NTA UGC NET", "desc": "National Eligibility Test for Assistant Professor & JRF", "url": "https://ugcnet.nta.ac.in"},
                {"name": "ICAI Portal", "desc": "Chartered Accountancy exam dates, RTPs & announcements", "url": "https://www.icai.org"}
            ]
            for idx, p in enumerate(portals):
                c = [p_col1, p_col2, p_col3][idx % 3]
                with c:
                    st.markdown(f"""
<div class='glass-card' style='margin-bottom: 12px;'>
<div style='font-weight: 700; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 4px;'>{p['name']}</div>
<p style='color: #94A3B8; font-size: 0.8rem; margin-bottom: 12px; line-height: 1.3;'>{p['desc']}</p>
<a href='{p['url']}' target='_blank' style='text-decoration: none;'>
<button style='background: rgba(255, 255, 255, 0.08); color: #CBD5E1; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; padding: 6px 12px; font-size: 0.8rem; font-weight: 600; cursor: pointer;'>Visit Official Site ↗</button>
</a>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 10: 💼 JOBS & INTERNSHIPS
# =========================================================
elif page in ["💼 Jobs & Internships", "💼 Job Recommendations"]:
    st.subheader("💼 Curated Jobs & Internships")
    st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-top: -8px;'>Discover high-impact internships on <b>Internshala</b>, <b>Unstop</b>, and full-time opportunities on <b>LinkedIn</b>.</p>", unsafe_allow_html=True)
    import urllib.parse
    selected_role = st.selectbox("Select Target Track", list(recommendation.career_engine.CAREERS_DB.keys()))
    
    # Filter by opportunity type and workplace type
    col_jf1, col_jf2 = st.columns(2)
    with col_jf1:
        opp_filter = st.selectbox("Opportunity Type", ["All Opportunities", "🎓 Internships (Internshala / Unstop)", "💼 Full-Time Jobs"])
    with col_jf2:
        mode_filter = st.selectbox("Workplace Mode", ["All Modes", "Remote / Work from Home", "Hybrid", "Onsite"])
    
    jobs_key = f"jobs_{selected_role}"
    if st.button("🔎 Fetch Live Jobs & Internships", use_container_width=True):
        with st.spinner(f"Retrieving top internships and job openings for {selected_role}..."):
            fetched = utils.fetch_ai_job_listings(selected_role)
            st.session_state[jobs_key] = fetched

    jobs_list = st.session_state.get(jobs_key, [])
    if jobs_list:
        filtered_jobs = []
        for j in jobs_list:
            j_type = j.get('type', 'Full-time')
            j_loc = j.get('location', '').lower()
            
            # Filter by opportunity type
            if opp_filter == "🎓 Internships (Internshala / Unstop)" and j_type != "Internship":
                continue
            if opp_filter == "💼 Full-Time Jobs" and j_type != "Full-time":
                continue
                
            # Filter by workplace mode
            if mode_filter == "Remote / Work from Home" and "remote" not in j_loc and "work from home" not in j_loc:
                continue
            if mode_filter == "Hybrid" and "hybrid" not in j_loc:
                continue
            if mode_filter == "Onsite" and ("remote" in j_loc or "hybrid" in j_loc):
                continue
                
            filtered_jobs.append(j)
            
        st.markdown(f"<div style='margin: 12px 0; color: #CBD5E1; font-size: 0.9rem;'>Showing <b>{len(filtered_jobs)}</b> openings for <b>{selected_role}</b></div>", unsafe_allow_html=True)
        
        # Official category mapping for Internshala for 100% reliable links without redirect loops
        internshala_categories = {
            "AI Engineer": "artificial-intelligence-ai",
            "Machine Learning Engineer": "machine-learning",
            "Data Scientist": "data-science",
            "Data Analyst": "data-analytics",
            "Frontend Developer": "front-end-development",
            "Backend Developer": "backend-development",
            "Full Stack Developer": "full-stack-development",
            "Cybersecurity Engineer": "cyber-security",
            "Ethical Hacker": "ethical-hacking",
            "Cloud Engineer": "cloud-computing",
            "DevOps Engineer": "devops",
            "Software Engineer": "software-development",
            "Mobile App Developer": "mobile-app-development",
            "UI UX Designer": "ui-ux-design",
            "Blockchain Developer": "blockchain",
            "Game Developer": "game-development",
            "Embedded Engineer": "embedded-systems",
            "QA Engineer": "quality-assurance",
            "Database Administrator": "database-administration",
            "Business Analyst": "business-analytics",
            "Product Manager": "product-management"
        }

        for job in filtered_jobs:
            is_internship = job.get('type', 'Full-time') == "Internship"
            skills_chips = "".join([f"<span class='badge-have' style='font-size:0.75rem;'>{sk}</span>" for sk in job.get('skills', [])])
            
            # Clean text for URLs (remove special characters like /, &, + that break routing)
            clean_job_title = re.sub(r'[^a-zA-Z0-9 ]+', ' ', job['title']).strip()
            encoded_generic = urllib.parse.quote_plus(clean_job_title)
            encoded_title = urllib.parse.quote_plus(f"{clean_job_title} {job.get('company', '')}")
            
            # Generate reliable Internshala URL using official category slug if available
            if selected_role in internshala_categories:
                internshala_url = f"https://internshala.com/internships/{internshala_categories[selected_role]}-internship/"
            else:
                clean_slug = re.sub(r'[^a-zA-Z0-9]+', '-', job['title']).strip('-').lower()
                internshala_url = f"https://internshala.com/internships/keywords-{clean_slug}/"
            
            comp_value = str(job.get('compensation', job.get('salary', '₹15,000 - ₹30,000 / month'))).replace('$', '₹')
            duration_val = job.get('duration', '3-6 Months' if is_internship else 'Permanent')
            
            card_border = "#1295D8" if is_internship else "#10B981"
            type_pill = "<span style='background: rgba(18, 149, 216, 0.15); color: #38BDF8; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.8rem; border: 1px solid rgba(56, 189, 248, 0.3);'>🎓 Internship</span>" if is_internship else "<span style='background: rgba(139, 92, 246, 0.15); color: #A78BFA; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.8rem; border: 1px solid rgba(139, 92, 246, 0.3);'>💼 Full-Time</span>"

            # Action buttons formatted without leading spaces to prevent markdown codeblock rendering
            if is_internship:
                action_buttons = (
                    f"<a href='{internshala_url}' target='_blank' style='text-decoration: none;'>"
                    f"<button style='background: #1295D8; color: white; border: none; border-radius: 6px; padding: 7px 14px; font-size: 0.8rem; font-weight: 700; cursor: pointer; box-shadow: 0 2px 8px rgba(18, 149, 216, 0.35);'>Apply on Internshala ↗</button></a> "
                    f"<a href='https://unstop.com/internships?search={encoded_generic}' target='_blank' style='text-decoration: none;'>"
                    f"<button style='background: #1C4980; color: white; border: none; border-radius: 6px; padding: 7px 12px; font-size: 0.8rem; font-weight: 600; cursor: pointer;'>Unstop ↗</button></a> "
                    f"<a href='https://www.linkedin.com/jobs/search/?keywords={encoded_generic}%20internship' target='_blank' style='text-decoration: none;'>"
                    f"<button style='background: #0A66C2; color: white; border: none; border-radius: 6px; padding: 7px 12px; font-size: 0.8rem; font-weight: 600; cursor: pointer;'>LinkedIn ↗</button></a>"
                )
            else:
                action_buttons = (
                    f"<a href='https://www.linkedin.com/jobs/search/?keywords={encoded_title}' target='_blank' style='text-decoration: none;'>"
                    f"<button style='background: #0A66C2; color: white; border: none; border-radius: 6px; padding: 7px 14px; font-size: 0.8rem; font-weight: 700; cursor: pointer; box-shadow: 0 2px 8px rgba(10, 102, 194, 0.35);'>Apply on LinkedIn ↗</button></a> "
                    f"<a href='https://www.indeed.com/jobs?q={encoded_generic}' target='_blank' style='text-decoration: none;'>"
                    f"<button style='background: #2164f3; color: white; border: none; border-radius: 6px; padding: 7px 12px; font-size: 0.8rem; font-weight: 600; cursor: pointer;'>Search Indeed ↗</button></a>"
                )

            st.markdown(f"""
<div class='glass-card' style='border-left: 4px solid {card_border}; margin-bottom: 14px;'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;'>
<div>
<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 4px;'>
<h4 style='color:#F8FAFC; margin:0; font-size: 1.15rem;'>{job['title']}</h4>
{type_pill}
</div>
<div style='font-size: 0.88rem; color: #CBD5E1;'>
🏢 <b>{job['company']}</b> &bull; 📍 {job['location']}
</div>
</div>
<div style='display: flex; gap: 6px; align-items: center;'>
<span style='background: rgba(16, 185, 129, 0.15); color: #34D399; padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 0.85rem;'>
💰 {comp_value}
</span>
<span style='background: rgba(255, 255, 255, 0.05); color: #CBD5E1; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem;'>
⏱️ {duration_val}
</span>
</div>
</div>
<p style='color: #94A3B8; font-size: 0.9rem; line-height: 1.5; margin: 10px 0;'>{job['description']}</p>
<div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-top: 10px;'>
<div style='display: flex; flex-wrap: wrap; gap: 4px;'>
{skills_chips}
</div>
<div style='display: flex; gap: 8px; flex-wrap: wrap;'>
{action_buttons}
</div>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.info(f"💡 Click **'Fetch Live Jobs & Internships'** above to search for current {selected_role} roles and internships on Internshala.")

# =========================================================
# PAGE 10: 👤 PROFILE & SETTINGS
# =========================================================
elif page == "👤 Profile & Settings":
    st.subheader("👤 User Profile & Portfolio Dossier")
    
    # User Gamification Data
    user_gam = database.get_user_gamification(username)
    xp = user_gam.get("xp", 0)
    level = (xp // 100) + 1
    
    tier_badge = "<span style='background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(16, 185, 129, 0.4); margin-right: 8px;'>⚡ Pro Member</span>" if is_pro else "<span style='background: rgba(255, 255, 255, 0.06); color: #94A3B8; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(255, 255, 255, 0.12); margin-right: 8px;'>🌱 Free Member</span>"

    st.markdown(f"""
<div class='glass-card'>
    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
        <div>
            <h2 style='margin:0; color: #F8FAFC;'>{st.session_state.name}</h2>
            <span style='color: #A78BFA; font-weight: 600;'>@{username}</span>
        </div>
        <div style='text-align: right;'>
            {tier_badge}
            <span style='background: linear-gradient(135deg, #8B5CF6, #10B981); color: white; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                Level {level} Explorer &bull; {xp} XP
            </span>
        </div>
    </div>
    <hr style='border-color: rgba(255, 255, 255, 0.08); margin: 16px 0;'>
    <p>🛠️ <b>Registered Core Skills:</b> {user_skills}</p>
    <p>🧠 <b>Trait Calibration:</b> Logic: <b>{logic}/10</b> | Creativity: <b>{creativity}/10</b> | Communication: <b>{communication}/10</b></p>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 💎 Membership & Subscription")
    if is_pro:
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            st.markdown("""
<div class='glass-card' style='border-color: rgba(16, 185, 129, 0.35); background: rgba(16, 185, 129, 0.04);'>
    <h4 style='color: #34D399; margin-top: 0;'>⚡ Active Pro Subscription</h4>
    <p style='color: #CBD5E1; font-size: 0.9rem; margin-bottom: 6px;'><b>Status:</b> Active Pro Member &bull; <b>Plans:</b> 1 Month, 1 Year, 3 Years</p>
    <p style='color: #94A3B8; font-size: 0.85rem; margin: 0;'>Unlimited AI Career Guidance, Voice Interviews, 24-Week Interactive Roadmap, & Priority Internship Applications unlocked.</p>
</div>
""", unsafe_allow_html=True)
        with col_s2:
            st.write("")
            st.write("")
            if st.button("Cancel Subscription", use_container_width=True):
                database.cancel_pro_subscription(username)
                st.session_state.is_pro = False
                st.warning("Subscription cancelled. Reverted to Free Member tier.")
                st.rerun()
    else:
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            st.markdown("""
<div class='glass-card'>
    <h4 style='color: #F8FAFC; margin-top: 0;'>🌱 Free Member Tier</h4>
    <p style='color: #CBD5E1; font-size: 0.9rem; margin-bottom: 6px;'><b>Status:</b> Free Plan &bull; Standard AI recommendations & basic job search.</p>
    <p style='color: #94A3B8; font-size: 0.85rem; margin: 0;'>Choose from 1 Month (₹499), 1 Year (₹3,999), or 3 Years (₹7,999) to unlock advanced AI mock interviews, ATS resume scoring, and full roadmaps.</p>
</div>
""", unsafe_allow_html=True)
        with col_s2:
            st.write("")
            st.write("")
            if st.button("🚀 Upgrade to Pro", use_container_width=True, type="primary"):
                show_subscription_modal()

    st.markdown("### 📥 Export Career Portfolio Dossier")
    st.markdown("Download a comprehensive PDF report containing your trait analysis, skill gap assessment, customized roadmap, and recommended courses.")
    
    # Generate PDF directly for one-click download
    pdf_bytes = report_generator.build_pdf_report(
        st.session_state.name,
        {"logic": logic, "creativity": creativity, "communication": communication},
        user_skills, top_match["career_name"], top_match["match_percentage"],
        top_match["skills_gap"], "Strategic Roadmap Included", "Curated Courses Included"
    )
    
    st.download_button(
        label="📥 Download Career Dossier PDF",
        data=pdf_bytes,
        file_name=f"{username}_career_dossier.pdf",
        mime="application/pdf",
        use_container_width=True
    )