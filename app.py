# app.py - Flask REST API & Web Server Controller (Emoji-Free & Comparator Integrated)

import os
import time
from flask import Flask, render_template, request, jsonify, session

# Function to manually load .env file if it exists
def load_dotenv(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, val = line.split("=", 1)
                        # Remove whitespace and surrounding quotes
                        val = val.strip().strip("'\"")
                        os.environ[key.strip()] = val

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Generate a cryptographically secure random session secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex())

# Import components
from db_handler import register_user, authenticate_user
from llm_handler import analyze_symptoms_groq, chat_with_empathy_groq
from simulation_engine import (
    get_clinical_analysis,
    generate_health_history,
    get_simulated_chat_response
)

# ==================== WEB ROUTES ====================

@app.route("/")
def index():
    """
    Serves the Single Page Application HTML5 master structure.
    """
    return render_template("index.html")

# ==================== AUTHENTICATION API ENDPOINTS ====================

@app.route("/api/signup", methods=["POST"])
def signup():
    """
    Registers a new patient profile securely in the local database.
    """
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400
        
    success, msg = register_user(email, name, password)
    if success:
        # Establish session variables
        session["logged_in"] = True
        session["user_name"] = name
        session["email"] = email
        return jsonify({"success": True, "message": msg, "user_name": name})
    else:
        return jsonify({"success": False, "message": msg}), 400

@app.route("/api/login", methods=["POST"])
def login():
    """
    Authenticates patient credentials against our secure SQLite salted SHA-256 store.
    """
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400
        
    success, msg, name = authenticate_user(email, password)
    if success:
        # Establish session variables
        session["logged_in"] = True
        session["user_name"] = name
        session["email"] = email
        return jsonify({"success": True, "message": msg, "user_name": name})
    else:
        return jsonify({"success": False, "message": msg}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    """
    Clears active user session contexts.
    """
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})

# ==================== DYNAMIC VITALS LOGGER ENDPOINTS ====================

@app.route("/api/vitals", methods=["GET", "POST"])
def manage_vitals():
    """
    Manages active daily patient vitals and timeline chart histories.
    """
    if not session.get("logged_in"):
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
        
    # Initialize default vitals in session if not present
    if "vitals" not in session:
        session["vitals"] = {
            "heart_rate": 78,
            "active_minutes": 45,
            "water_intake": 6,
            "health_score": 92
        }
        
    if request.method == "POST":
        data = request.get_json() or {}
        # Safely parse slider updates
        for key in ["heart_rate", "active_minutes", "water_intake", "health_score"]:
            if key in data:
                session["vitals"][key] = int(data[key])
        session.modified = True
        return jsonify({"success": True, "vitals_current": session["vitals"]})
        
    # GET: Retrieve vitals context and generated 7-day health tracking timeline
    history = generate_health_history()
    # Inject current interactive slider vitals into the latest index in the history timeline
    if history and len(history) > 0:
        history[-1]["Avg Heart Rate (BPM)"] = session["vitals"]["heart_rate"]
        history[-1]["Water Intake (Glasses)"] = session["vitals"]["water_intake"]
        history[-1]["Active Minutes"] = session["vitals"]["active_minutes"]
        
    return jsonify({
        "success": True, 
        "vitals_current": session["vitals"],
        "history": history
    })

# ==================== CLINICAL SYMPTOM ANALYSIS ENDPOINTS ====================

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Runs multi-model symptom analyses using the Groq LPU API or local Clinical Simulation fallbacks.
    """
    data = request.get_json() or {}
    symptom_text = data.get("symptom_text", "")
    demographics = data.get("demographics", {})
    severity = data.get("severity", 5)
    duration = data.get("duration", "1-3 Days")
    force_fallback = data.get("force_fallback", False)
    
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    # Check if Groq API key is present and active
    if api_key.startswith("gsk_") and not force_fallback:
        try:
            # Call Groq API Llama-3.3-70B model
            results = analyze_symptoms_groq(
                api_key=api_key,
                symptom_text=symptom_text,
                demographics=demographics,
                severity=severity,
                duration=duration
            )
            # Fetch corresponding local key matching to map guidelines layout
            symptom_key, _, _ = get_clinical_analysis(symptom_text)
            return jsonify({
                "success": True,
                "symptom_key": symptom_key,
                "results": results,
                "engine": "Groq LPU API"
            })
        except Exception as e:
            # Resilient fallback to local clinical simulation parser
            err_msg = str(e)
            symptom_key, conditions, treatment_plan = get_clinical_analysis(symptom_text)
            results = {
                "conditions": conditions,
                "treatment_plan": treatment_plan
            }
            return jsonify({
                "success": True,
                "symptom_key": symptom_key,
                "results": results,
                "engine": "Local Clinical Simulation (Groq Connection Offline)",
                "api_error": err_msg
            })
    else:
        # Run local Clinical NLP Simulation parser
        symptom_key, conditions, treatment_plan = get_clinical_analysis(symptom_text)
        results = {
            "conditions": conditions,
            "treatment_plan": treatment_plan
        }
        return jsonify({
            "success": True,
            "symptom_key": symptom_key,
            "results": results,
            "engine": "Local Clinical Simulation Engine"
        })

# ==================== GROQ MODEL COMPARATOR ENDPOINT ====================

@app.route("/api/compare", methods=["POST"])
def compare():
    """
    Benchmarks multiple Groq models concurrently against the same symptom prompt.
    Returns latency, word counts, token speeds, and analysis outputs side-by-side.
    """
    if not session.get("logged_in"):
        return jsonify({"success": False, "message": "Unauthorized access."}), 401
        
    data = request.get_json() or {}
    symptom_text = data.get("symptom_text", "")
    demographics = data.get("demographics", {})
    severity = data.get("severity", 5)
    duration = data.get("duration", "1-3 Days")
    models = data.get("models", [])
    
    if not symptom_text:
        return jsonify({"success": False, "message": "Symptom prompt query is required."}), 400
        
    if not models:
        return jsonify({"success": False, "message": "Select at least one Groq model to benchmark."}), 400
        
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key.startswith("gsk_"):
        return jsonify({
            "success": False, 
            "message": "Live API Mode is disabled. To run benchmarks, please configure a valid Groq API Key starting with 'gsk_' in the .env file."
        }), 400
        
    benchmarks = []
    
    for model in models:
        try:
            start_time = time.time()
            results = analyze_symptoms_groq(
                api_key=api_key,
                symptom_text=symptom_text,
                demographics=demographics,
                severity=severity,
                duration=duration,
                model=model
            )
            latency = round(time.time() - start_time, 2)
            
            # Compute output statistics
            response_str = str(results)
            word_count = len(response_str.split())
            # Estimate tokens (~1.35 tokens per word for structured json completions)
            tokens_estimated = int(word_count * 1.35)
            tokens_per_sec = round(tokens_estimated / (latency if latency > 0 else 0.1), 1)
            
            benchmarks.append({
                "model": model,
                "latency": latency,
                "word_count": word_count,
                "tokens_per_sec": tokens_per_sec,
                "results": results,
                "success": True
            })
        except Exception as e:
            benchmarks.append({
                "model": model,
                "success": False,
                "error": str(e)
            })
            
    return jsonify({"success": True, "benchmarks": benchmarks})

# ==================== EMPATHETIC CHATBOT API ENDPOINTS ====================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Orchestrates the 24/7 empathetic patient chat using Groq or local response routers.
    """
    data = request.get_json() or {}
    message = data.get("message", "")
    history = data.get("history", [])
    demographics = data.get("demographics", {})
    
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    if api_key.startswith("gsk_"):
        try:
            # Call Groq Chat API Llama-3.3-70B model
            response = chat_with_empathy_groq(
                api_key=api_key,
                conversation_history=history,
                user_message=message,
                demographics=demographics
            )
            return jsonify({"success": True, "response": response})
        except Exception as e:
            # Resilient fallback on exception
            fallback_resp = get_simulated_chat_response(message)
            combined = f"[API connection offline: {str(e)} (Falling back to Clinical Guide)]\n\n{fallback_resp}"
            return jsonify({"success": True, "response": combined})
    else:
        # Call local simulated chatbot response router
        response = get_simulated_chat_response(message)
        return jsonify({"success": True, "response": response})

# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    # Start the Flask web application
    app.run(debug=True)
