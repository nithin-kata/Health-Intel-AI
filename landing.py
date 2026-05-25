# landing.py - Premium Landing Page with 3D Flip Card

import streamlit as st

LANDING_CSS = """
<style>
/* 3D Scene and Perspective */
.scene3d {
    width: 340px;
    height: 380px;
    perspective: 1200px;
    margin: 30px auto;
}

.card3d {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer;
}

.scene3d:hover .card3d {
    transform: rotateY(180deg) rotateX(5deg);
}

.card3d-front, .card3d-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 24px;
    padding: 35px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.card3d-front {
    background: linear-gradient(135deg, rgba(23, 28, 41, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 
                inset 0 0 30px rgba(6, 182, 212, 0.15);
}

.card3d-back {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 
                inset 0 0 30px rgba(139, 92, 246, 0.2);
    transform: rotateY(180deg);
    color: #E2E8F0;
}

.floating-icon {
    font-size: 4.5rem;
    filter: drop-shadow(0 0 20px rgba(6, 182, 212, 0.5));
    animation: float 4s ease-in-out infinite;
    margin-bottom: 25px;
}

@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-12px) rotate(3deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

.pulse-badge {
    background: rgba(6, 182, 212, 0.1);
    border: 1px solid rgba(6, 182, 212, 0.3);
    color: #06B6D4;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
    display: inline-block;
}

/* Feature grid items */
.landing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 40px;
    width: 100%;
}

.landing-grid-item {
    background: rgba(23, 28, 41, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    text-align: left;
    transition: all 0.3s ease;
}

.landing-grid-item:hover {
    border-color: rgba(6, 182, 212, 0.2);
    background: rgba(23, 28, 41, 0.6);
    transform: translateY(-3px);
}

.landing-grid-icon {
    font-size: 1.8rem;
    margin-bottom: 12px;
}

/* Mock Nav Bar style */
.mock-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 40px;
}
</style>
"""

def show_landing_page():
    # Inject CSS specific to the landing page
    st.markdown(LANDING_CSS, unsafe_allow_html=True)
    
    # Mock Header Navigation
    st.markdown(
        '<div class="mock-nav">'
        '<div style="display:flex; align-items:center; gap:8px;">'
        '<span style="font-size:1.6rem;">⚕️</span>'
        '<span style="font-family:\'Outfit\'; font-weight:800; font-size:1.35rem; color:#FFF;">Health Intel AI</span>'
        '</div>'
        '<div style="color:#94A3B8; font-size:0.85rem; font-family:\'Outfit\'; font-weight:500;">PREMIUM PRE-SCREENING</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Grid columns layout: Left is text, Right is 3D Card
    col_text, col_card = st.columns([6, 4], gap="large")
    
    with col_text:
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        st.markdown('<span class="badge badge-low" style="font-size: 0.85rem; padding: 6px 14px; margin-bottom: 15px;">🛡️ Clinical Intelligence System</span>', unsafe_allow_html=True)
        
        st.markdown(
            '<h1 style="font-size: 3.2rem; font-family:\'Outfit\'; font-weight:900; line-height:1.1; margin-bottom:20px;">'
            'The Future of <span style="background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Healthcare Intelligence</span>'
            '</h1>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            '<p style="font-size: 1.15rem; color: #94A3B8; line-height: 1.6; margin-bottom: 30px; font-family:\'Inter\';">'
            'Empowering individuals with clinical-grade symptom assessments, visual health analytics, and empathetic conversational guidance. '
            'Equipped with ultra-fast LLM capabilities to deliver predictive wellness pre-screenings in seconds.'
            '</p>',
            unsafe_allow_html=True
        )
        
        # Action CTA
        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("🚀 ENTER PLATFORM", use_container_width=True, type="primary"):
                st.session_state.current_page = "auth"
                st.rerun()
        with c_btn2:
            st.markdown(
                '<div style="text-align: center; padding-top: 8px;">'
                '<span style="color:#94A3B8; font-size:0.9rem;">🔐 100% Client-Side Safe</span>'
                '</div>',
                unsafe_allow_html=True
            )
            
    with col_card:
        # Render the interactive 3D Card
        st.markdown(
            '<div class="scene3d">'
            '  <div class="card3d">'
            '    <div class="card3d-front">'
            '      <div class="pulse-badge">Hover to Flip</div>'
            '      <div class="floating-icon">⚕️</div>'
            '      <h3 style="color:#FFF; font-family:\'Outfit\'; font-size:1.6rem; font-weight:700; margin:0 0 10px 0;">Health Intel AI</h3>'
            '      <p style="color:#94A3B8; font-size:0.9rem; line-height:1.4; margin:0;">Generative Pre-screening & High-Fidelity Vitals Dashboarding</p>'
            '    </div>'
            '    <div class="card3d-back">'
            '      <span class="badge badge-high" style="margin-bottom:15px;">Advanced Analytics</span>'
            '      <h3 style="color:#FFF; font-family:\'Outfit\'; font-size:1.6rem; font-weight:700; margin:0 0 10px 0;">LPU Accelerated</h3>'
            '      <p style="color:#CBD5E1; font-size:0.9rem; line-height:1.4; margin:0 0 15px 0;">Powered by Llama-3.3-70B on high-speed inference engines.</p>'
            '      <div style="font-size:0.75rem; color:#8B5CF6; font-weight:600; text-transform:uppercase;">Click Enter Platform to Start</div>'
            '    </div>'
            '  </div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('<hr style="border-top: 1px solid rgba(255, 255, 255, 0.05); margin: 40px 0 30px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:\'Outfit\'; color:#FFF; text-align:center; font-size:1.6rem; margin-bottom:20px;">Explore Our Core Modules</h3>', unsafe_allow_html=True)
    
    # 4 Product Feature Cards Grid
    st.markdown(
        '<div class="landing-grid">'
        '  <div class="landing-grid-item">'
        '    <div class="landing-grid-icon" style="color:#06B6D4;">📊</div>'
        '    <h4 style="color:#FFF; font-family:\'Outfit\'; margin:0 0 8px 0; font-size:1.1rem;">Vitals & Analytics</h4>'
        '    <p style="color:#94A3B8; font-size:0.85rem; line-height:1.4; margin:0;">Interactive patient timeline chart graphs mapping sleep, hydration, and symptom intensity histories.</p>'
        '  </div>'
        '  <div class="landing-grid-item">'
        '    <div class="landing-grid-icon" style="color:#3B82F6;">🩺</div>'
        '    <h4 style="color:#FFF; font-family:\'Outfit\'; margin:0 0 8px 0; font-size:1.1rem;">Predictive Analyzer</h4>'
        '    <p style="color:#94A3B8; font-size:0.85rem; line-height:1.4; margin:0;">AI-driven pre-screening assessment that weighs demographics and returns risk factors immediately.</p>'
        '  </div>'
        '  <div class="landing-grid-item">'
        '    <div class="landing-grid-icon" style="color:#8B5CF6;">📋</div>'
        '    <h4 style="color:#FFF; font-family:\'Outfit\'; margin:0 0 8px 0; font-size:1.1rem;">Treatment Plans</h4>'
        '    <p style="color:#94A3B8; font-size:0.85rem; line-height:1.4; margin:0;">Actionable dietary guidelines, healthy lifestyle alterations, and critical Red Flag warning systems.</p>'
        '  </div>'
        '  <div class="landing-grid-item">'
        '    <div class="landing-grid-icon" style="color:#EC4899;">💬</div>'
        '    <h4 style="color:#FFF; font-family:\'Outfit\'; margin:0 0 8px 0; font-size:1.1rem;">Empathetic Chat</h4>'
        '    <p style="color:#94A3B8; font-size:0.85rem; line-height:1.4; margin:0;">A supportive, 24/7 conversational medical virtual assistant built on high-fidelity clinical principles.</p>'
        '  </div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Spacer
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
