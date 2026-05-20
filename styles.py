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
    background: rgba(23, 28, 41, 0.55) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 20px !important;
    transition: transform 0.2s ease, border-color 0.2s ease !important;
}

.glass-card:hover {
    border-color: rgba(6, 182, 212, 0.3) !important;
    transform: translateY(-2px) !important;
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
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    align-self: flex-end !important;
    border-bottom-right-radius: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.chat-bubble.assistant {
    background: rgba(30, 41, 59, 0.7) !important;
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
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    text-align: center !important;
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

/* Premium form customization */
div[data-baseweb="input"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
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
</style>
"""
