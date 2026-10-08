import os
import base64
import streamlit as st
import database
import re

def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo_dark.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def show_auth_page():
    """Renders registration, login, and password recovery pages with modern Purple + Emerald SaaS UI."""
    logo_b64 = get_logo_base64()
    logo_img_tag = f"<img src='data:image/png;base64,{logo_b64}' style='width: 90px; height: 90px; border-radius: 20px; box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4); border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 12px;'>" if logo_b64 else ""

    col_logo, col_auth = st.columns([1.2, 1])
    
    with col_logo:
        st.markdown(f"""<div style='margin-top: 10px;'>
{logo_img_tag}
<h1 style='font-size: 3.2rem; text-align: left; font-weight: 800; letter-spacing: -1px; margin-bottom: 8px; line-height: 1.1;'>
<span style='background: linear-gradient(135deg, #A78BFA, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>CareerPath</span> 
<span style='color: #34D399; text-shadow: 0 0 16px rgba(52, 211, 153, 0.4);'>AI</span>
</h1>
<p style='font-size: 1.15rem; text-align: left; color: #CBD5E1; font-weight: 400; margin-bottom: 24px; line-height: 1.5;'>
AI-powered career guidance, resume analysis, and interview preparation — all in one platform.
</p>
<div class='glass-card' style='border-left: 4px solid #10B981; margin-bottom: 20px;'>
<h3 style='margin-top: 0; color: #F8FAFC; font-size: 1.15rem;'>✨ Everything You Need to Build Your Career</h3>
<div style='display: flex; flex-direction: column; gap: 10px; margin-top: 14px; font-size: 0.92rem; color: #CBD5E1;'>
<div>⚡ <b style='color: #F8FAFC;'>20+ Career Paths</b> — Multi-vector AI career matching algorithm</div>
<div>🧩 <b style='color: #F8FAFC;'>Skill Gap Analysis</b> — Identify exact topics you need to learn</div>
<div>📅 <b style='color: #F8FAFC;'>30/60/90-Day Roadmaps</b> — Personalized dynamic learning plans</div>
<div>📄 <b style='color: #F8FAFC;'>ATS Resume Analyzer</b> — Score & optimize your resume for recruiters</div>
<div>🎤 <b style='color: #F8FAFC;'>AI Mock Interviews</b> — Practice & receive real-time audio feedback</div>
</div>
</div>
<div style='background: linear-gradient(135deg, #8B5CF6, #10B981); color: white; font-weight: 700; font-size: 1rem; padding: 12px 24px; border-radius: 12px; text-align: center; box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4); display: inline-block; cursor: pointer;'>
🚀 Explore CareerPath AI →
</div>
</div>""", unsafe_allow_html=True)
        
    with col_auth:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        auth_tab = st.radio("Access Platform", ["Sign In", "Create Account", "Forgot Password"], horizontal=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if auth_tab == "Sign In":
            st.subheader("Login to your Account")
            login_user = st.text_input("Username").strip()
            login_pass = st.text_input("Password", type="password")
            
            if st.button("Log In"):
                if login_user and login_pass:
                    user_name = database.verify_user(login_user, login_pass)
                    if user_name:
                        st.session_state.username = login_user
                        st.session_state.name = user_name
                        st.success(f"Welcome back, {user_name}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.warning("Please fill in all fields.")
                    
        elif auth_tab == "Create Account":
            st.subheader("Create Free Account")
            reg_name = st.text_input("Full Name").strip()
            reg_user = st.text_input("Choose Username").strip()
            reg_pass = st.text_input("Password", type="password")
            
            if st.button("Sign Up"):
                if reg_name and reg_user and reg_pass:
                    if not (3 <= len(reg_user) <= 20):
                        st.error("Username must be between 3 and 20 characters.")
                    elif not re.match(r"^[a-zA-Z0-9_]+$", reg_user):
                        st.error("Username must only contain letters, numbers, and underscores.")
                    elif len(reg_pass) < 8:
                        st.error("Password must be at least 8 characters long.")
                    else:
                        if database.register_user(reg_user, reg_pass, reg_name):
                            st.success("Account registered successfully! Please login.")
                            st.balloons()
                        else:
                            st.error("Username already exists.")
                else:
                    st.warning("Please fill in all fields.")
                    
        elif auth_tab == "Forgot Password":
            st.subheader("Recover Password")
            rec_user = st.text_input("Enter Username").strip()
            new_pass = st.text_input("Choose New Password", type="password")
            
            if st.button("Reset Password"):
                if rec_user and new_pass:
                    if len(new_pass) < 8:
                        st.error("Password must be at least 8 characters long.")
                    else:
                        # Query user existence
                        conn = database.get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM users WHERE username = ?", (rec_user,))
                        row = cursor.fetchone()
                        if row:
                            pw_hash = database.hash_password(new_pass)
                            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (pw_hash, rec_user))
                            conn.commit()
                            st.success("Password reset successfully! Proceed to Sign In.")
                        else:
                            st.error("Username not found.")
                        conn.close()
                else:
                    st.warning("Please enter your details.")
                    
        st.markdown("</div>", unsafe_allow_html=True)
