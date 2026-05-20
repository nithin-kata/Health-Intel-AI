# app.py - Main Streamlit Application UI

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# Import components
from styles import CUSTOM_CSS
from simulation_engine import (
    get_clinical_analysis,
    generate_health_history,
    get_simulated_chat_response,
    CLINICAL_DATABASE
)
from llm_handler import analyze_symptoms_groq, chat_with_empathy_groq

# Set page config with high-tech theme defaults
st.set_page_config(
    page_title="Healthcare Intelligence AI",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject premium custom CSS stylesheet
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- CONFIGURATION -----------------
# Pre-populated with your Groq API Key
GROQ_API_KEY = "YOUR_API_KEY_HERE"

# ----------------- SESSION STATE INITIALIZATION -----------------
if "demographics" not in st.session_state:
    st.session_state.demographics = {
        "age": 32,
        "gender": "Male",
        "pre_existing": "None",
        "medications": "None"
    }

# Determine default mode based on API key availability
default_key = GROQ_API_KEY if GROQ_API_KEY != "YOUR_API_KEY_HERE" and GROQ_API_KEY.strip() != "" else os.environ.get("GROQ_API_KEY", "")

if "api_mode" not in st.session_state:
    st.session_state.api_mode = "Groq Live API Mode" if default_key else "Simulation Mode"

if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = default_key

if "groq_model" not in st.session_state:
    st.session_state.groq_model = "llama-3.3-70b-versatile"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Hello! I am your 24/7 AI Medical Assistant. How are you feeling today? You can describe any symptoms you are experiencing, and I will offer clinical facts and empathetic guidance."
        }
    ]

if "symptom_input" not in st.session_state:
    st.session_state.symptom_input = ""

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "active_symptom_key" not in st.session_state:
    st.session_state.active_symptom_key = "general"

# ----------------- SIDEBAR INTERFACE -----------------
st.sidebar.markdown(
    '<div style="text-align: center; margin-bottom: 20px;">'
    '<h1 style="color: #06B6D4; font-size: 1.8rem; font-family: \'Outfit\'; font-weight: 800;">'
    '⚕️ Health Intel AI</h1>'
    '<span style="color: #94A3B8; font-size: 0.85rem;">Medical Symptom Analyzer</span>'
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<hr style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 10px 0;">', unsafe_allow_html=True)

# Navigation
st.sidebar.markdown('<p class="gradient-subheader" style="font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase;">Navigation</p>', unsafe_allow_html=True)
navigation = st.sidebar.radio(
    "Go To Page",
    [
        "📊 Vitals & Analytics Dashboard",
        "🩺 Predictive Symptom Analyzer",
        "📋 Personalized Treatment Plans",
        "💬 24/7 Conversational Chat"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown('<hr style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 15px 0;">', unsafe_allow_html=True)

# Patient Demographics Profile
st.sidebar.markdown('<p class="gradient-subheader" style="font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase;">Patient Profile</p>', unsafe_allow_html=True)
with st.sidebar.expander("👤 Edit Demographics", expanded=True):
    age = st.slider("Age", 1, 100, st.session_state.demographics["age"])
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.demographics["gender"]))
    pre_existing = st.text_input("Pre-existing Conditions", st.session_state.demographics["pre_existing"], placeholder="e.g. Hypertension, None")
    medications = st.text_input("Active Medications", st.session_state.demographics["medications"], placeholder="e.g. Aspirin, None")
    
    st.session_state.demographics = {
        "age": age,
        "gender": gender,
        "pre_existing": pre_existing if pre_existing.strip() != "" else "None",
        "medications": medications if medications.strip() != "" else "None"
    }

# API Credentials Config
st.sidebar.markdown('<hr style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 15px 0;">', unsafe_allow_html=True)
st.sidebar.markdown('<p class="gradient-subheader" style="font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase;">AI Engine Settings</p>', unsafe_allow_html=True)
with st.sidebar.expander("⚙️ Groq LPU Config", expanded=False):
    api_mode = st.radio("Operating Mode", ["Simulation Mode", "Groq Live API Mode"], index=1 if st.session_state.api_mode == "Groq Live API Mode" else 0)
    groq_key = st.text_input("Groq API Key", st.session_state.groq_api_key, type="password", placeholder="gsk-...")
    groq_model = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"], index=0)
    
    st.session_state.api_mode = api_mode
    st.session_state.groq_api_key = groq_key
    st.session_state.groq_model = groq_model
    
    if api_mode == "Groq Live API Mode" and not groq_key.startswith("gsk_"):
        st.warning("⚠️ Enter a valid Groq API Key (starts with gsk_)")

# Safety Disclaimer
st.sidebar.markdown('<hr style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 20px 0;">', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div style="background-color: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 12px; font-size: 0.75rem; color: #EF4444; line-height: 1.4;">'
    '⚠️ <strong>MEDICAL DISCLAIMER:</strong> This AI system provides informational and educational pre-screening guidance only. '
    'It does NOT substitute for professional medical advice, physical examination, diagnosis, or clinical treatment. '
    '<strong>If you have a medical emergency, call 911 or visit the nearest ER immediately.</strong>'
    '</div>',
    unsafe_allow_html=True
)

# ----------------- HEADER & BANNER -----------------
# Define banner image paths
banner_path = r"C:\Users\NITHIN KATA\.gemini\antigravity\brain\219379dd-943a-4779-a1a3-0616aee34382\medical_ai_banner_1779253229884.png"

try:
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        st.markdown(
            '<div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 50%, rgba(139, 92, 246, 0.15) 100%); '
            'border-bottom: 2px solid rgba(6, 182, 212, 0.3); border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 30px;">'
            '<h1 class="gradient-header">Healthcare Intelligence AI</h1>'
            '<p style="color: #94A3B8; font-size: 1.2rem; max-width: 800px; margin: 0 auto; font-family: \'Outfit\';">'
            'Empowering patients with reliable, clinical-grade pre-screening analytics, personalized care insights, and empathetic conversational guidance.</p>'
            '</div>',
            unsafe_allow_html=True
        )
except Exception:
    st.markdown(
        '<div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 50%, rgba(139, 92, 246, 0.15) 100%); '
        'border-bottom: 2px solid rgba(6, 182, 212, 0.3); border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 30px;">'
        '<h1 class="gradient-header">Healthcare Intelligence AI</h1>'
        '<p style="color: #94A3B8; font-size: 1.2rem; max-width: 800px; margin: 0 auto; font-family: \'Outfit\';">'
        'Empowering patients with reliable, clinical-grade pre-screening analytics, personalized care insights, and empathetic conversational guidance.</p>'
        '</div>',
        unsafe_allow_html=True
    )

# ----------------- PAGE 1: HEALTH DASHBOARD -----------------
if navigation == "📊 Vitals & Analytics Dashboard":
    st.markdown('<h2 style="font-family: \'Outfit\'; font-size: 2.2rem; color: #FFF; margin-bottom: 20px;">📊 Patient Vitals & Health Analytics</h2>', unsafe_allow_html=True)
    
    # 4 Quick Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div class="metric-box">'
            '<div class="metric-value" style="color: #06B6D4;">78 <span style="font-size: 0.9rem; color: #94A3B8;">BPM</span></div>'
            '<div class="metric-label">Avg Heart Rate</div>'
            '<div style="font-size: 0.75rem; color: #34D399; margin-top: 4px;">🟢 Normal Range</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="metric-box">'
            '<div class="metric-value" style="color: #3B82F6;">45 <span style="font-size: 0.9rem; color: #94A3B8;">MIN</span></div>'
            '<div class="metric-label">Active Minutes</div>'
            '<div style="font-size: 0.75rem; color: #34D399; margin-top: 4px;">📈 +15% vs Last Week</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div class="metric-box">'
            '<div class="metric-value" style="color: #6366F1;">6 / 8 <span style="font-size: 0.9rem; color: #94A3B8;">CUPS</span></div>'
            '<div class="metric-label">Water Intake</div>'
            '<div style="font-size: 0.75rem; color: #FBBF24; margin-top: 4px;">🟡 75% of Daily Target</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            '<div class="metric-box">'
            '<div class="metric-value" style="color: #A855F7;">92%</div>'
            '<div class="metric-label">Health Score</div>'
            '<div style="font-size: 0.75rem; color: #34D399; margin-top: 4px;">🟢 Excellent Health Index</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # 2 Column Chart Area
    c1, c2 = st.columns(2)
    
    # Generate static 7-day health history
    history_df = generate_health_history()
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #06B6D4; font-family: \'Outfit\'; margin-top:0;">%s Daily Symptom Severity Trend</h3>' % "🩺", unsafe_allow_html=True)
        
        # Plotly chart for symptom severity (neon line)
        fig1 = px.line(
            history_df,
            x="Date",
            y="Symptom Severity (1-10)",
            markers=True,
            color_discrete_sequence=["#06B6D4"]
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94A3B8',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title=""),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 10], title="Severity Scale (1-10)"),
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #8B5CF6; font-family: \'Outfit\'; margin-top:0;">💤 Vitals: Sleep & Activity Tracking</h3>', unsafe_allow_html=True)
        
        # Plotly chart for sleep vs activity
        fig2 = px.bar(
            history_df,
            x="Date",
            y=["Sleep Duration (Hours)", "Water Intake (Glasses)"],
            barmode="group",
            color_discrete_map={
                "Sleep Duration (Hours)": "#8B5CF6",
                "Water Intake (Glasses)": "#3B82F6"
            }
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94A3B8',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title=""),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Metric Value"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""),
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Weekly AI Insight card
    st.markdown(
        '<div class="glass-card" style="border-left: 5px solid #06B6D4;">'
        '<h4 style="color: #06B6D4; font-family: \'Outfit\'; margin-top:0; font-size:1.15rem; display: flex; align-items: center; gap: 8px;">'
        '🧠 AI Health Intelligence Insights</h4>'
        '<p style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;">'
        '🔍 <strong>Trend Observation:</strong> Over the past 7 days, your active minutes and sleep schedule show strong stabilization. '
        'Your daily symptom severity shows a <strong>decrease of 62%</strong> (improving from 7 to 2 out of 10) starting around May 18, which correlates '
        'closely with your hydration levels increasing from 4 glasses to 8 glasses of water daily.'
        '</p>'
        '<p style="color: #94A3B8; font-size: 0.85rem; margin-top: 10px;">'
        '💡 <strong>Recommendations:</strong> Maintain a stable hydration regimen (target: 8 glasses/day). '
        'Continue prioritizing sleep hygiene, aiming for 7-8 hours. If symptoms reappear or aggravate during physical active cycles, '
        'scale back exercise intensity and log the trigger event in the Symptom Analyzer.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

# ----------------- PAGE 2: SYMPTOM ANALYZER -----------------
elif navigation == "🩺 Predictive Symptom Analyzer":
    st.markdown('<h2 style="font-family: \'Outfit\'; font-size: 2.2rem; color: #FFF; margin-bottom: 20px;">🩺 Proactive Disease & Symptom Analyzer</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #06B6D4; font-family: \'Outfit\'; margin-top:0;">1. Enter Patient Presentation</h3>', unsafe_allow_html=True)
    
    # Clickable suggestion chips
    st.write("💡 **Quick Symptom Presets (Click to test):**")
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1:
        if st.button("🫁 Tight Chest Pain", use_container_width=True):
            st.session_state.symptom_input = "severe pressure and tightness in chest, difficulty breathing"
    with col_s2:
        if st.button("🧠 Throbbing Migraine", use_container_width=True):
            st.session_state.symptom_input = "throbbing headache on left side of head, sensitive to light and noise"
    with col_s3:
        if st.button("🤒 High Fever & Cough", use_container_width=True):
            st.session_state.symptom_input = "dry persistent cough, body chills, mild sore throat, shivering fever"
    with col_s4:
        if st.button("🦵 Clicking Knee Pain", use_container_width=True):
            st.session_state.symptom_input = "stiff and aching knee joint, clicking pops during walking up stairs"
    with col_s5:
        if st.button("🧴 Itchy Red Skin Rash", use_container_width=True):
            st.session_state.symptom_input = "localized red itchy rash on skin after using new laundry detergent"
            
    # Text input
    symptom_desc = st.text_area(
        "Describe what physical symptoms you are currently experiencing in detail:",
        value=st.session_state.symptom_input,
        placeholder="Provide symptoms, timing, locations, and onset details...",
        height=120
    )
    # Sync manual edit back to session state
    st.session_state.symptom_input = symptom_desc

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    
    c_form1, c_form2 = st.columns(2)
    with c_form1:
        severity = st.slider("Rate Current Symptom Severity (1 = Barely noticeable, 10 = Severe/Intolerable)", 1, 10, 5)
    with c_form2:
        duration = st.selectbox(
            "Onset Duration:",
            ["Less than 24 hours", "1-3 Days", "4-7 Days", "1-2 Weeks", "More than 2 Weeks"]
        )
        
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Active mode summary badge
    if st.session_state.api_mode == "Groq Live API Mode":
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 15px; color: #A855F7;">'
            f'🌐 Engine: <strong>Groq LPU API ({st.session_state.groq_model})</strong> active</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="text-align: center; margin-bottom: 15px; color: #06B6D4;">'
            '💻 Engine: <strong>Local Clinical Simulation Parser</strong> active</div>', 
            unsafe_allow_html=True
        )

    # Submit button
    submit_btn = st.button("🚀 RUN PROACTIVE CLINICAL ASSESSMENT", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_btn:
        if not symptom_desc.strip():
            st.error("⚠️ Please describe your symptoms or select one of the quick presets above before running the assessment.")
        else:
            with st.spinner("⏳ Analyzing medical knowledge base & patient demographics..."):
                # Simulation vs Groq api logic
                if st.session_state.api_mode == "Groq Live API Mode":
                    if not st.session_state.groq_api_key.strip():
                        st.error("❌ Groq API Key is missing. Please expand the 'Groq LPU Config' in the sidebar and enter your key, or toggle to 'Simulation Mode'.")
                    else:
                        try:
                            # Call Groq API
                            analysis = analyze_symptoms_groq(
                                api_key=st.session_state.groq_api_key,
                                symptom_text=symptom_desc,
                                demographics=st.session_state.demographics,
                                severity=severity,
                                duration=duration,
                                model=st.session_state.groq_model
                            )
                            st.session_state.analysis_results = analysis
                            # Try matching active symptom key for treatment plan mapping
                            symptom_key, _, _ = get_clinical_analysis(symptom_desc)
                            st.session_state.active_symptom_key = symptom_key
                            st.success("✅ Generative clinical analysis complete via Groq LPU API!")
                        except Exception as e:
                            err_msg = str(e)
                            if "401" in err_msg or "api_key" in err_msg.lower():
                                st.error("❌ **Groq Authentication Failed (401 - Invalid API Key)**:\n\nThe API key written in `app.py` has been rejected by Groq. Please generate a new key on your [Groq Console](https://console.groq.com/keys) and update it in the sidebar under **Groq LPU Config** or edit `app.py` directly.")
                            else:
                                st.error(f"❌ Groq API Error: {err_msg}")
                            st.info("💡 Falling back to Local Clinical Simulation Mode to maintain experience.")
                            symptom_key, conditions, treatment_plan = get_clinical_analysis(symptom_desc)
                            st.session_state.analysis_results = {
                                "conditions": conditions,
                                "treatment_plan": treatment_plan
                            }
                            st.session_state.active_symptom_key = symptom_key
                else:
                    # Run NLP Simulation Mode
                    time.sleep(1.2) # Simulate network lag
                    symptom_key, conditions, treatment_plan = get_clinical_analysis(symptom_desc)
                    st.session_state.analysis_results = {
                        "conditions": conditions,
                        "treatment_plan": treatment_plan
                    }
                    st.session_state.active_symptom_key = symptom_key
                    st.success("✅ Clinical pre-screening simulation complete!")

    # Display results
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #8B5CF6; font-family: \'Outfit\'; margin-top:0;">📊 Proactive Condition Likelihood Assessment</h3>', unsafe_allow_html=True)
        
        st.write("Below are potential non-critical clinical conditions that align with your symptom profile and demographics:")
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        for cond in results["conditions"]:
            risk_class = "badge-low"
            if cond["risk"] == "HIGH":
                risk_class = "badge-high"
            elif cond["risk"] == "MEDIUM":
                risk_class = "badge-med"
                
            col_left, col_right = st.columns([7, 3])
            with col_left:
                st.markdown(
                    f'<span style="font-size: 1.15rem; font-weight: 700; color: #FFF;">{cond["name"]}</span> '
                    f'<span class="badge {risk_class}" style="margin-left: 8px;">{cond["risk"]} RISK</span>',
                    unsafe_allow_html=True
                )
                st.write(cond["nlp_reason"])
            with col_right:
                st.markdown(f'<div style="text-align: right; margin-bottom: 5px; font-weight: 600; color: #06B6D4;">Likelihood: {cond["likelihood"]}%</div>', unsafe_allow_html=True)
                st.progress(cond["likelihood"] / 100.0)
                
            st.markdown('<hr style="border-top: 1px dashed rgba(255, 255, 255, 0.08); margin: 15px 0;">', unsafe_allow_html=True)
            
        st.markdown(
            '<div style="text-align: center; margin-top: 10px;">'
            '<p style="color: #94A3B8;">📋 Care plan generated. Navigate to the <strong>"Personalized Treatment Plans"</strong> tab in the sidebar to view care checklists and critical safety warnings.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- PAGE 3: TREATMENT PLANS -----------------
elif navigation == "📋 Personalized Treatment Plans":
    st.markdown('<h2 style="font-family: \'Outfit\'; font-size: 2.2rem; color: #FFF; margin-bottom: 20px;">📋 Personalized Clinical Care Guidelines</h2>', unsafe_allow_html=True)
    
    # Load fallback preset if no analysis exists
    if not st.session_state.analysis_results:
        st.markdown(
            '<div class="glass-card" style="text-align: center; padding: 40px 20px;">'
            '<h4>🔍 No Active Care Plan Found</h4>'
            '<p style="color: #94A3B8;">You have not run a symptom analysis yet in this session. '
            'Please select one of the following preset conditions to generate a mock clinical care guidelines plan for review:</p>'
            '</div>',
            unsafe_allow_html=True
        )
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            if st.button("📋 Load Chest Pain Care Plan", use_container_width=True):
                st.session_state.active_symptom_key = "chest_pain"
                st.session_state.analysis_results = {
                    "conditions": CLINICAL_DATABASE["chest_pain"]["conditions"],
                    "treatment_plan": CLINICAL_DATABASE["chest_pain"]["treatment_plan"]
                }
                st.rerun()
        with col_c2:
            if st.button("📋 Load Migraine Care Plan", use_container_width=True):
                st.session_state.active_symptom_key = "headache"
                st.session_state.analysis_results = {
                    "conditions": CLINICAL_DATABASE["headache"]["conditions"],
                    "treatment_plan": CLINICAL_DATABASE["headache"]["treatment_plan"]
                }
                st.rerun()
        with col_c3:
            if st.button("📋 Load Flu & Cough Care Plan", use_container_width=True):
                st.session_state.active_symptom_key = "flu_cough"
                st.session_state.analysis_results = {
                    "conditions": CLINICAL_DATABASE["flu_cough"]["conditions"],
                    "treatment_plan": CLINICAL_DATABASE["flu_cough"]["treatment_plan"]
                }
                st.rerun()
                
    else:
        results = st.session_state.analysis_results
        plan = results.get("treatment_plan", {})
        topic_name = st.session_state.active_symptom_key.replace("_", " ").upper()
        
        # RED FLAG SYSTEM WARNINGS - CRITICAL
        red_flags_html = "".join([f"<li>{item}</li>" for item in plan.get("red_flags", [])])
        st.markdown(
            f'<div class="red-flag-box">'
            f'<div class="red-flag-title">⚠️ CRITICAL SAFETY WARNING (RED FLAGS - SEEK EMERGENCY CARE)</div>'
            f'<p style="color: #F87171; font-size: 0.9rem; margin-bottom: 8px;">'
            f'If you experience any of the symptoms below, discontinue self-care immediately and call 911 or visit the nearest ER:</p>'
            f'<ul style="color: #FCA5A5; font-size: 0.9rem; margin-left: 20px; line-height: 1.5;">{red_flags_html}</ul>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(f'<h3 style="color: #06B6D4; font-family: \'Outfit\'; margin-bottom: 20px;">Tailored Guidelines: {topic_name} Support</h3>', unsafe_allow_html=True)
        
        # 3 Column Care Layout
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #3B82F6; font-family: \'Outfit\'; margin-top:0;">🛑 Immediate Actions</h4>', unsafe_allow_html=True)
            st.write("Initial steps to manage physical discomfort and prioritize stability:")
            for idx, act in enumerate(plan.get("immediate_actions", [])):
                st.markdown(f"**{idx+1}.** {act}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_t2:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #10B981; font-family: \'Outfit\'; margin-top:0;">🥗 Dietary Adjustments</h4>', unsafe_allow_html=True)
            st.write("Nutritional adjustments to assist immunological recovery or reduce inflammation:")
            for idx, diet in enumerate(plan.get("dietary", [])):
                st.markdown(f"**{idx+1}.** {diet}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_t3:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #8B5CF6; font-family: \'Outfit\'; margin-top:0;">🏃‍♂️ Lifestyle Modifications</h4>', unsafe_allow_html=True)
            st.write("Longer-term actions to build biological resilience and eliminate pain triggers:")
            for idx, life in enumerate(plan.get("lifestyle", [])):
                st.markdown(f"**{idx+1}.** {life}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        st.info("💡 Pro-Tip: You can export this care plan or write specific questions about these guidelines in the '24/7 Conversational Chat' tab to discuss with your doctor.")

# ----------------- PAGE 4: 24/7 PATIENT CHAT -----------------
elif navigation == "💬 24/7 Conversational Chat":
    st.markdown('<h2 style="font-family: \'Outfit\'; font-size: 2.2rem; color: #FFF; margin-bottom: 20px;">💬 24/7 Conversational Patient Chat Assistant</h2>', unsafe_allow_html=True)
    
    st.write("Discuss your symptoms, ask questions about care guidelines, or seek clarifications about clinical facts in real-time. Our assistant communicates with professional medical facts and empathy.")
    
    # Pre-programmed suggestion chips
    st.write("💡 **Quick Queries (Click to ask):**")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    preset_query = ""
    with col_q1:
        if st.button("🚨 What are chest pain emergency red flags?", use_container_width=True):
            preset_query = "What are the emergency red flags I should watch out for if I have chest pain?"
    with col_q2:
        if st.button("💆 How can I manage migraines at home?", use_container_width=True):
            preset_query = "What are the best home remedies and lifestyle modifications for dealing with migraine headaches?"
    with col_q3:
        if st.button("🤒 What dietary changes help when having a flu?", use_container_width=True):
            preset_query = "What are the best foods and hydration tips to recover quickly from influenza fever and dry cough?"
    with col_q4:
        if st.button("🤝 I feel anxious about my symptoms. Help.", use_container_width=True):
            preset_query = "I am feeling extremely anxious and worried about my physical symptoms. Can you give me some reassurance?"

    # Chat history display area
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        avatar = "👤" if msg["role"] == "user" else "⚕️"
        bubble_class = "user" if msg["role"] == "user" else "assistant"
        
        st.markdown(
            f'<div class="chat-bubble {bubble_class}">'
            f'<div class="chat-avatar">{avatar}</div>'
            f'<div>{msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input logic
    user_chat_msg = st.chat_input("Enter your health question here...")
    
    # Override with preset click if applicable
    if preset_query != "":
        user_chat_msg = preset_query

    if user_chat_msg:
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": user_chat_msg})
        st.rerun()

    # Trigger Assistant Response if last message is from user
    if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
        user_msg = st.session_state.chat_history[-1]["content"]
        
        with st.spinner("⏳ Assistant is typing..."):
            if st.session_state.api_mode == "Groq Live API Mode":
                if not st.session_state.groq_api_key.strip():
                    response_text = "❌ Groq API Key is missing. Please configure it in the sidebar settings or switch to 'Simulation Mode'."
                else:
                    try:
                        response_text = chat_with_empathy_groq(
                            api_key=st.session_state.groq_api_key,
                            conversation_history=st.session_state.chat_history[:-1],
                            user_message=user_msg,
                            demographics=st.session_state.demographics,
                            model=st.session_state.groq_model
                        )
                    except Exception as e:
                        err_msg = str(e)
                        if "401" in err_msg or "api_key" in err_msg.lower():
                            response_text = "❌ **Groq Authentication Failed (401 - Invalid API Key)**:\n\nThe API key in use was rejected by Groq. Please create a new key on your **[Groq Console](https://console.groq.com/keys)** and update it in the sidebar settings or edit the code."
                        else:
                            response_text = f"❌ API Error: {err_msg}\n\n*Falling back to local clinical guide responses.*"
                        
                        # Fallback response
                        fallback_resp = get_simulated_chat_response(user_msg)
                        response_text += f"\n\n⚕️ **Clinical Guide Response:** {fallback_resp}"
            else:
                time.sleep(1.0) # Simulate typing delay
                response_text = get_simulated_chat_response(user_msg)
                
            # Append Assistant Message
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            st.rerun()

    # Clear chat button
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I am your 24/7 AI Medical Assistant. How are you feeling today? You can describe any symptoms you are experiencing, and I will offer clinical facts and empathetic guidance."
            }
        ]
        st.rerun()
