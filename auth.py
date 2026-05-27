# auth.py - Login / Signup authentication page

import streamlit as st
from db_handler import register_user, authenticate_user

AUTH_CSS = """
<style>
.auth-container {
    max-width: 450px;
    margin: 40px auto;
    background: rgba(23, 28, 41, 0.45) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 24px !important;
    padding: 35px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

.auth-header {
    text-align: center;
    margin-bottom: 25px;
}

.auth-title {
    font-family: 'Outfit', sans-serif;
    color: #FFF;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.auth-subtitle {
    color: #94A3B8;
    font-size: 0.9rem;
}
</style>
"""

def show_auth_page():
    # Inject auth styling
    st.markdown(AUTH_CSS, unsafe_allow_html=True)
    
    # Back Button
    if st.button("⬅️ Back to Home"):
        st.session_state.current_page = "landing"
        st.rerun()
        
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown(
        '<div class="auth-header">'
        '  <span style="font-size: 2.2rem;">🔐</span>'
        '  <div class="auth-title">Secure Portal Access</div>'
        '  <div class="auth-subtitle">Sign in or create a profile to launch analytics</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Tabs for login and signup
    tab_login, tab_signup = st.tabs(["🔒 Sign In", "➕ Create Account"])
    
    with tab_login:
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        login_email = st.text_input("Email Address", value="patient@healthintel.ai", key="login_email_input")
        login_pass = st.text_input("Password", value="health123", type="password", key="login_pass_input")
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        login_btn = st.button("🔓 AUTHORIZE & ENTER", use_container_width=True, type="primary")
        if login_btn:
            if not login_email or not login_pass:
                st.error("⚠️ Please fill in all fields.")
            else:
                with st.spinner("⏳ Establishing secure session..."):
                    success, msg, name = authenticate_user(login_email, login_pass)
                    if success:
                        st.session_state.user_name = name
                        st.session_state.logged_in = True
                        st.success("✅ Secure session established!")
                        st.rerun()
                    else:
                        st.error(msg)
                    
    with tab_signup:
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        signup_name = st.text_input("Full Name", placeholder="e.g. John Doe", key="signup_name_input")
        signup_email = st.text_input("Email Address", placeholder="e.g. john@example.com", key="signup_email_input")
        signup_pass = st.text_input("Password", placeholder="Choose a secure password", type="password", key="signup_pass_input")
        
        # Interactive password guidelines
        st.markdown(
            '<p style="font-size:0.75rem; color:#94A3B8; margin-top: 5px;">'
            '🔒 Password should be 8+ characters, with at least 1 number and 1 special symbol.'
            '</p>',
            unsafe_allow_html=True
        )
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        signup_btn = st.button("🚀 REGISTER ACCOUNT", use_container_width=True, type="primary")
        if signup_btn:
            if not signup_name or not signup_email or not signup_pass:
                st.error("⚠️ Please fill in all fields.")
            elif len(signup_pass) < 8:
                st.error("❌ Password must be at least 8 characters long.")
            else:
                with st.spinner("⏳ Creating medical profile..."):
                    success, msg = register_user(signup_email, signup_name, signup_pass)
                    if success:
                        st.session_state.user_name = signup_name
                        st.session_state.logged_in = True
                        st.success("✅ Account created successfully!")
                        st.rerun()
                    else:
                        st.error(msg)
                    
    st.markdown('</div>', unsafe_allow_html=True)
