# Styles file for CareerPath AI Modern Glassmorphism Theme (Purple + Emerald Green AI SaaS Theme)

MODERN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Global Style */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: #05070D !important;
    color: #F8FAFC !important;
    background-image: 
        radial-gradient(at 15% 15%, rgba(139, 92, 246, 0.14) 0px, transparent 55%),
        radial-gradient(at 85% 20%, rgba(16, 185, 129, 0.10) 0px, transparent 50%),
        radial-gradient(at 50% 85%, rgba(109, 40, 217, 0.10) 0px, transparent 60%) !important;
    background-attachment: fixed !important;
}

/* Glassmorphism Card Container */
.glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.025) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 22px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
}
.glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(139, 92, 246, 0.30) !important;
    box-shadow: 0 12px 40px 0 rgba(139, 92, 246, 0.15) !important;
}

/* Header Title Gradient */
.gradient-title {
    background: linear-gradient(90deg, #A78BFA 0%, #8B5CF6 50%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.8rem;
    text-align: center;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    filter: drop-shadow(0px 4px 12px rgba(139, 92, 246, 0.3));
}

.gradient-subtitle {
    font-weight: 300;
    color: #94A3B8;
    text-align: center;
    font-size: 1.05rem;
    margin-bottom: 24px;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background: rgba(5, 7, 13, 0.92) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
}

/* Sidebar Navigation Buttons / Options */
div[data-testid="stSidebarNav"] {
    padding-top: 10px;
}

/* Primary Action Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.35) !important;
    transition: all 0.25s ease !important;
    width: 100%;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #6D28D9, #9333EA) !important;
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
    border-color: rgba(167, 139, 250, 0.4) !important;
}
div.stButton > button:active {
    transform: scale(0.98) !important;
}

/* Download / Success Emerald Buttons */
div.stDownloadButton > button {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.30) !important;
    transition: all 0.25s ease !important;
    width: 100%;
}
div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #059669, #047857) !important;
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
}

/* Streamlit Tabs Custom styling */
button[data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    background: transparent !important;
    padding: 10px 18px !important;
    border: none !important;
    transition: all 0.25s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: #A78BFA !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #34D399 !important;
    border-bottom: 2px solid #10B981 !important;
    text-shadow: 0 0 12px rgba(16, 185, 129, 0.4) !important;
}

/* Metrics Cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.025) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    text-align: center !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
}
[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #A78BFA, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
    font-size: 0.85rem !important;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.025) !important;
    border: 1px solid rgba(139, 92, 246, 0.20) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
}

/* User Messages - Emerald Tint */
[data-testid="stChatMessage"][data-testid="stChatMessageUser"] {
    background-color: rgba(16, 185, 129, 0.06) !important;
    border-color: rgba(16, 185, 129, 0.22) !important;
}

/* Highlight Skill Badges */
.badge-have {
    background-color: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.28);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
}
.badge-need {
    background-color: rgba(139, 92, 246, 0.12);
    color: #A78BFA;
    border: 1px solid rgba(139, 92, 246, 0.30);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
}

/* Input Fields styling */
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    background: rgba(255, 255, 255, 0.025) !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}
div[data-baseweb="input"] input:focus, div[data-baseweb="textarea"] textarea:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.3) !important;
}

/* Progress bar customization */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%) !important;
    border-radius: 999px !important;
}
.stProgress > div > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border-radius: 999px !important;
}

/* Mock Interview Score badge */
.score-circle {
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: conic-gradient(#8B5CF6 var(--percentage), #10B981 var(--percentage), rgba(255, 255, 255, 0.08) 0);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: bold;
    color: #F8FAFC;
    margin: auto;
    position: relative;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.25);
}
.score-circle::after {
    content: "";
    position: absolute;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: #05070D;
}
.score-circle span {
    position: relative;
    z-index: 10;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: rgba(5, 7, 13, 0.6) !important;
}
::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.25) !important;
    border-radius: 6px !important;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(139, 92, 246, 0.50) !important;
}

</style>
"""

