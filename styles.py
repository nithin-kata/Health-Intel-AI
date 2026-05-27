# styles.py - Premium dark-theme CSS injection for Healthcare Intelligence AI

CUSTOM_CSS = """
<style>
/* Import modern typography */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

/* Apply primary typography */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0B0E14 !important;
    color: #E2E8F0 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* Glassmorphism containers */
.glass-card {
    background: rgba(23, 28, 41, 0.45) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    margin-bottom: 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.glass-card:hover {
    border-color: rgba(6, 182, 212, 0.25) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 20px rgba(6, 182, 212, 0.1) !important;
}

/* Linear gradient typography headers */
.gradient-header {
    background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    margin-bottom: 5px !important;
}

.gradient-subheader {
    background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

/* Micro-animations */
@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* Custom styled warning alert */
.red-flag-box {
    background: rgba(239, 68, 68, 0.08) !important;
    border-left: 5px solid #EF4444 !important;
    border-radius: 8px !important;
    padding: 18px !important;
    margin: 20px 0 !important;
    animation: pulse 3s infinite !important;
}

.red-flag-title {
    color: #F87171 !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 8px !important;
}

/* Chat bubble styling */
.chat-container {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    margin: 15px 0 !important;
    width: 100% !important;
}

.chat-bubble {
    padding: 14px 18px !important;
    border-radius: 20px !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    max-width: 75% !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
}

.chat-bubble.user {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.65) 0%, rgba(99, 102, 241, 0.65) 100%) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    color: #FFFFFF !important;
    align-self: flex-end !important;
    border-bottom-right-radius: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.chat-bubble.assistant {
    background: rgba(30, 41, 59, 0.45) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    color: #E2E8F0 !important;
    align-self: flex-start !important;
    border-bottom-left-radius: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.chat-avatar {
    font-size: 1.3rem !important;
    margin-bottom: 4px !important;
}

/* Custom indicator pills */
.badge {
    display: inline-block !important;
    padding: 4px 10px !important;
    border-radius: 9999px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

.badge-high {
    background-color: rgba(239, 68, 68, 0.15) !important;
    color: #F87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
}

.badge-med {
    background-color: rgba(245, 158, 11, 0.15) !important;
    color: #FBBF24 !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
}

.badge-low {
    background-color: rgba(16, 185, 129, 0.15) !important;
    color: #34D399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
}

/* Sleek metrics widgets */
.metric-box {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    text-align: center !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.metric-box:hover {
    border-color: rgba(6, 182, 212, 0.25) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2), 0 0 10px rgba(6, 182, 212, 0.05) !important;
}

.metric-value {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    font-family: 'Outfit', sans-serif !important;
}

.metric-label {
    font-size: 0.8rem !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-top: 4px !important;
}

/* Premium glass sidebar customization */
section[data-testid="stSidebar"] {
    background: rgba(13, 17, 23, 0.45) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}

/* Premium glass button overrides */
div.stButton > button {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #E2E8F0 !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}
div.stButton > button:hover {
    background: rgba(6, 182, 212, 0.08) !important;
    border-color: rgba(6, 182, 212, 0.3) !important;
    color: #06B6D4 !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.15) !important;
    transform: translateY(-2px) !important;
}
div.stButton > button:active {
    transform: translateY(0) !important;
}

/* Primary buttons specific glow */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%) !important;
    border: 1px solid rgba(6, 182, 212, 0.4) !important;
    color: #FFF !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(59, 130, 246, 0.25) 100%) !important;
    border-color: rgba(6, 182, 212, 0.6) !important;
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.25) !important;
}

/* Premium glass Tab controls */
div[data-testid="stTabBar"] {
    background: rgba(23, 28, 41, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 6px !important;
    gap: 8px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
}
div[data-testid="stTabBar"] button {
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    transition: all 0.3s ease !important;
    color: #94A3B8 !important;
    background: transparent !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
}
div[data-testid="stTabBar"] button[aria-selected="true"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #FFF !important;
    font-weight: 600 !important;
    box-shadow: inset 0 0 10px rgba(6, 182, 212, 0.05) !important;
}
div[data-testid="stTabBar"] button:hover {
    color: #FFF !important;
    background: rgba(255, 255, 255, 0.02) !important;
}
div[data-testid="stTabBar"]::after {
    display: none !important;
}

/* Premium form and input customization */
div[data-baseweb="input"], 
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background-color: rgba(15, 23, 42, 0.45) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
    transition: all 0.3s ease !important;
}
div[data-baseweb="input"]:focus-within, 
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    border-color: rgba(6, 182, 212, 0.4) !important;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.1) !important;
    background-color: rgba(15, 23, 42, 0.6) !important;
}

/* Premium glass sliders */
div[data-testid="stSlider"] [role="slider"] {
    background-color: #06B6D4 !important;
    border: 2px solid #FFF !important;
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.5) !important;
}
div[data-testid="stSlider"] div[role="presentation"] {
    background-color: rgba(255, 255, 255, 0.08) !important;
}
div[data-testid="stSlider"] div[data-testid="stSliderTickBar"] {
    color: #94A3B8 !important;
}

/* Sleek scrollbar override */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.3);
}
::-webkit-scrollbar-thumb {
    background: rgba(6, 182, 212, 0.3);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(6, 182, 212, 0.5);
}

/* Remove default Streamlit top header glow and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}

/* Chat input bottom container glass styling and alignment */
div[data-testid="stBottom"],
div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottom"] > div,
div[class*="stBottomBlockContainer"],
div[class*="stBottom"] {
    background-color: #0B0E14 !important;
    background: #0B0E14 !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stBottomBlockContainer"] {
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* ChatGPT-themed premium glassy input box (removes multiple nested boxes) */
div[data-testid="stChatInput"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-bottom: 20px !important;
}

/* Style the actual inner text area wrapper as a single clean glassy bar matching the navy blue theme cards above */
div[data-testid="stChatInput"] > div {
    background-color: #171C29 !important; /* Navy Blue matching color */
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 26px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    padding: 6px 14px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: rgba(6, 182, 212, 0.4) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), 0 0 15px rgba(6, 182, 212, 0.15) !important;
    background-color: #1D2333 !important; /* Slightly lighter navy blue on focus */
}

/* Inner input field styling */
div[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
}

/* Send arrow button styling */
div[data-testid="stChatInput"] button {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #E2E8F0 !important;
    border-radius: 50% !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stChatInput"] button:hover {
    background-color: rgba(6, 182, 212, 0.15) !important;
    border-color: rgba(6, 182, 212, 0.3) !important;
    color: #06B6D4 !important;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.25) !important;
}
</style>
"""
