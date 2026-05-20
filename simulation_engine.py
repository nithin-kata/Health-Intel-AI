# simulation_engine.py - Clinical Knowledge Database & Patient Simulator

import pandas as pd
import random
import datetime

# Clinical Knowledge Database mapping standard symptoms to potential conditions
CLINICAL_DATABASE = {
    "chest_pain": {
        "symptoms_matched": ["chest pain", "tightness", "pressure", "angina", "shortness of breath", "chest hurts", "heart hurting"],
        "conditions": [
            {"name": "Angina Pectoris", "likelihood": 45, "risk": "HIGH", "nlp_reason": "Based on reported pressure and chest tightness, transient reduction of myocardial blood flow (Angina) is a major diagnostic consideration."},
            {"name": "Gastroesophageal Reflux Disease (GERD)", "likelihood": 35, "risk": "LOW", "nlp_reason": "Acid reflux frequently mimics angina-like pain, presenting as retrosternal burning or pressure."},
            {"name": "Costochondritis", "likelihood": 20, "risk": "LOW", "nlp_reason": "Inflammation of the cartilage linking ribs to the breastbone causes localized chest pain, aggravated by pressure or breathing."}
        ],
        "treatment_plan": {
            "immediate_actions": [
                "Sit down immediately and rest. Avoid physical strain.",
                "Ensure loose-fitting clothing around your neck and chest.",
                "If you have prescribed nitroglycerin, administer as directed by your physician."
            ],
            "lifestyle": [
                "Implement a low-fat, heart-healthy Mediterranean diet.",
                "Incorporate stress-reduction techniques like mindful meditation and diaphragmatic breathing.",
                "Maintain a journal detailing pain triggers, duration, and associated activities."
            ],
            "dietary": [
                "Reduce caffeine and high-sodium food intake.",
                "Avoid heavy meals, especially within 3 hours before going to bed.",
                "Increase dietary fiber with whole grains, legumes, and fresh greens."
            ],
            "red_flags": [
                "Pain radiating to the left arm, shoulder, neck, jaw, or back.",
                "Crushing or squeezing chest sensation coupled with heavy sweating (diaphoresis).",
                "Shortness of breath (dyspnea) at rest, dizziness, lightheadedness, or sudden fainting."
            ]
        }
    },
    "headache": {
        "symptoms_matched": ["headache", "throbbing", "head hurts", "migraine", "temple pain", "forehead pressure", "head pain"],
        "conditions": [
            {"name": "Migraine", "likelihood": 50, "risk": "MEDIUM", "nlp_reason": "Unilateral, throbbing headache presentation is strongly associated with migraine, especially when exacerbated by light or sound."},
            {"name": "Tension Headache", "likelihood": 35, "risk": "LOW", "nlp_reason": "Bilateral, non-pulsating tightness surrounding the forehead suggests tension-induced myofascial strain."},
            {"name": "Dehydration Headache", "likelihood": 15, "risk": "LOW", "nlp_reason": "Decreased fluid levels lead to temporary narrowing of blood vessels in the brain, presenting as a generalized headache."}
        ],
        "treatment_plan": {
            "immediate_actions": [
                "Rest in a quiet, dark, and cool room.",
                "Apply a cold compress to your forehead or the back of your neck.",
                "Hydrate immediately by drinking 250-500ml of water or electrolyte solution."
            ],
            "lifestyle": [
                "Establish a consistent sleep schedule, aiming for 7-8 hours nightly.",
                "Reduce daily screen time and perform regular neck and shoulder stretches.",
                "Practice progressive muscle relaxation to relieve stress buildup."
            ],
            "dietary": [
                "Avoid potential triggers like aged cheeses, artificial sweeteners, and cured meats.",
                "Limit alcohol intake, particularly red wine.",
                "Maintain stable blood sugar levels by eating smaller, balanced meals regularly."
            ],
            "red_flags": [
                "Sudden, extremely severe headache peaking within seconds ('thunderclap' headache).",
                "Headache accompanied by high fever, stiff neck, confusion, double vision, or speech issues.",
                "A new headache after a recent head injury, or worsening when coughing or bending over."
            ]
        }
    },
    "flu_cough": {
        "symptoms_matched": ["cough", "fever", "flu", "sore throat", "chills", "congestion", "cold", "body ache", "shivering"],
        "conditions": [
            {"name": "Influenza (Flu)", "likelihood": 55, "risk": "MEDIUM", "nlp_reason": "Abrupt onset of high fever, body aches, shivering chills, and persistent cough is characteristic of influenza virus infection."},
            {"name": "Acute Bronchitis", "likelihood": 30, "risk": "LOW", "nlp_reason": "Persistent dry or productive cough following an upper respiratory infection indicates bronchial tube irritation."},
            {"name": "Common Cold (Rhinovirus)", "likelihood": 15, "risk": "LOW", "nlp_reason": "Mild sore throat combined with nasal congestion and low-grade fever points toward a viral rhinovirus infection."}
        ],
        "treatment_plan": {
            "immediate_actions": [
                "Prioritize bed rest to allow your immune system to fight the viral load.",
                "Stay warm and use a cool-mist humidifier near your bed to ease respiration.",
                "Gargle with warm salt water (1/2 teaspoon salt in a glass of warm water) for sore throat relief."
            ],
            "lifestyle": [
                "Avoid physical exertion until your body temperature returns to normal for 24+ hours.",
                "Wash hands frequently and isolate to prevent transmission to family members.",
                "Practice deep breathing exercises to clear respiratory passages."
            ],
            "dietary": [
                "Drink significant fluids: warm herbal teas, broths, and water to thin mucus secretions.",
                "Consume foods rich in Vitamin C and Zinc (citrus fruits, berries, nuts, pumpkin seeds).",
                "Avoid dairy if it appears to thicken phlegm, and limit sugary beverages."
            ],
            "red_flags": [
                "Difficulty breathing, chest pain, or a persistent high fever above 103°F (39.4°C) unresponsive to antipyretics.",
                "Inability to keep fluids down, leading to severe dehydration (dry mouth, extreme lethargy).",
                "Blueish lips or face (cyanosis), confusion, or severe chest rattling during respiration."
            ]
        }
    },
    "knee_pain": {
        "symptoms_matched": ["knee pain", "joint pain", "knee hurts", "stiff knee", "swollen knee", "knee click", "knee pop"],
        "conditions": [
            {"name": "Knee Osteoarthritis", "likelihood": 40, "risk": "LOW", "nlp_reason": "Stiffness, localized aching, and clicking sound during movement points to mechanical wear and tear of joint cartilage."},
            {"name": "Ligament/Meniscus Strain", "likelihood": 35, "risk": "MEDIUM", "nlp_reason": "Pain following mechanical twisting or minor impact points to micro-tears in ligament fibers or shock-absorbing meniscus."},
            {"name": "Patellofemoral Pain Syndrome", "likelihood": 25, "risk": "LOW", "nlp_reason": "Generalized ache behind or around the kneecap, worsened by stair climbing or sitting for long periods."}
        ],
        "treatment_plan": {
            "immediate_actions": [
                "Apply the R.I.C.E protocol: Rest the joint, Ice for 15 mins, Compress with elastic wrap, Elevate the leg.",
                "Avoid placing full body weight on the affected knee if pain is acute.",
                "Wear supportive footwear with cushioned soles."
            ],
            "lifestyle": [
                "Integrate low-impact exercises: swimming, cycling, or elliptical training rather than running.",
                "Strengthen quadriceps and hamstring muscles to offload stress from the knee joint.",
                "Maintain a healthy weight to reduce chronic load on weight-bearing joints."
            ],
            "dietary": [
                "Incorporate anti-inflammatory foods (fatty fish rich in Omega-3, walnuts, olive oil, turmeric).",
                "Minimize ultra-processed foods and refined sugars that aggravate systemic joint inflammation.",
                "Ensure sufficient intake of Vitamin D and Calcium for bone health."
            ],
            "red_flags": [
                "Inability to bear any weight on the leg, or the knee completely buckling or locking up.",
                "Extreme swelling, redness, heat, and severe pain accompanied by a fever (indicates potential septic joint).",
                "Visible joint deformity or severe pain following a high-impact fall or traumatic injury."
            ]
        }
    },
    "skin_rash": {
        "symptoms_matched": ["rash", "itchy skin", "red spots", "hives", "eczema", "skin irritation", "dry skin patch"],
        "conditions": [
            {"name": "Contact Dermatitis", "likelihood": 45, "risk": "LOW", "nlp_reason": "Localized red, itchy rash indicates an allergic or irritant reaction to a chemical, soap, or material exposure."},
            {"name": "Atopic Dermatitis (Eczema)", "likelihood": 35, "risk": "LOW", "nlp_reason": "Chronic, itchy, dry, and scaly red patches point toward atopic eczema, especially on flexor surfaces (creases)."},
            {"name": "Urticaria (Hives)", "likelihood": 20, "risk": "MEDIUM", "nlp_reason": "Sudden onset of raised, highly itchy, red or skin-colored welts (wheals) suggests an acute histamine release."}
        ],
        "treatment_plan": {
            "immediate_actions": [
                "Wash the area gently with cool water and a mild, fragrance-free cleanser to remove triggers.",
                "Apply an over-the-counter hydrocortisone cream (0.5% or 1%) or calamine lotion to relieve itching.",
                "Take a cool oatmeal bath to soothe widespread inflammation."
            ],
            "lifestyle": [
                "Avoid scratching the area (keep fingernails short) to prevent secondary bacterial infection.",
                "Wear loose, breathable cotton clothing. Avoid tight synthetic fabrics.",
                "Identify and keep a log of chemical exposures, new cosmetics, laundry detergents, or fabric types."
            ],
            "dietary": [
                "Hydrate generously to support skin barrier repair.",
                "Limit high-histamine foods (fermented foods, alcohol, aged cheese) if hives are active.",
                "Consume foods high in skin-supporting vitamins like Vitamin E (avocados, seeds) and Vitamin A."
            ],
            "red_flags": [
                "Rash that spreads extremely rapidly across the body, or is accompanied by a high fever.",
                "Rash associated with difficulty breathing, throat swelling, tongue numbness, or dizziness (anaphylaxis).",
                "Rash that begins to blister, is intensely painful, or shows signs of infection (pus, red streaks)."
            ]
        }
    }
}

# Fallback profile for general/unknown symptoms
DEFAULT_ANALYSIS = {
    "conditions": [
        {"name": "General Viral/Bacterial Syndrome", "likelihood": 40, "risk": "LOW", "nlp_reason": "The entered symptoms do not point to a specific major organ system issue, suggesting a mild systemic reaction or viral response."},
        {"name": "Mild Stress-Related Somatization", "likelihood": 35, "risk": "LOW", "nlp_reason": "Anxiety, tension, and mild sleep disturbance often manifest as minor physical discomforts across various bodily areas."},
        {"name": "Undetermined Clinical Presentation", "likelihood": 25, "risk": "MEDIUM", "nlp_reason": "A definite pre-screening match cannot be established from the inputted description. Requires professional inspection."}
    ],
    "treatment_plan": {
        "immediate_actions": [
            "Rest, limit strenuous tasks, and monitor your body temperature.",
            "Stay well hydrated by consuming water, light broths, or decaffeinated teas."
        ],
        "lifestyle": [
            "Incorporate a regular sleep pattern and gentle breathing exercises.",
            "Keep a meticulous daily log of symptom occurrence, severity, and potential triggers."
        ],
        "dietary": [
            "Eat nutrient-dense, easily digestible foods like soups, grains, and boiled vegetables.",
            "Avoid heavy, greasy, or spicy foods that can strain digestion."
        ],
        "red_flags": [
            "Pain that becomes severe, sharp, or localized to a specific quadrant of the body.",
            "Fever exceeding 103°F (39.4°C) or lasting longer than 72 hours.",
            "Shortness of breath, chest pain, confusion, or difficulty speaking."
        ]
    }
}

# EMPATHETIC CHATBOT PRE-PROGRAMMED DIALOGUES
CHAT_DIALOGUES = {
    "emergency": "If you or someone near you is experiencing severe symptoms like sudden chest crushing pain, difficulty breathing, numbness on one side of the body, or loss of consciousness, please immediately dial **911** or visit the nearest emergency room. Your safety is of paramount importance.",
    "migraine": "Dealing with migraines can be incredibly draining. The intense throbbing and sensitivity to light/sound can make daily life difficult. Make sure to rest in a completely dark, quiet room. Placing a cool damp towel on your temples and staying hydrated can help ease the intensity.",
    "flu": "Fever, body aches, and persistent coughing are your body's signals to slow down. Please rest in bed, keep warm, and hydrate continuously. Warm water, clear broths, and herbal teas with honey will help soothe throat irritation and clear congestion.",
    "joint_stiffness": "For morning joint stiffness or osteoarthritis, a gentle warm bath or heating pad can help relax muscles and ease movement. Avoid sudden high-impact motions, and consider mild low-impact stretching to promote flexibility.",
    "anxiety": "It's completely understandable to feel anxious when dealing with unexplained physical symptoms. However, stress can sometimes amplify the pain sensations. Take a slow, deep breath in... hold it... and release. Focus on resting. We are here to guide you, but seeing a friendly professional can provide peace of mind.",
    "hello": "Hello! I am your 24/7 AI Medical Assistant. I'm here to provide empathetic, health-related insights, clinical facts, and support. Please remember I am an informational tool, not a doctor. How are you feeling today?",
    "default": "I understand you are seeking guidance on your health. While I can offer clinical facts and tips, it is crucial to monitor your symptoms closely. If they persist or worsen, please consult a primary care doctor. What specific symptoms are you most concerned about right now?"
}

def parse_symptoms(symptom_text):
    """
    NLP Symptom Parser
    Matches user input string with conditions in the clinical database.
    """
    text_lower = symptom_text.lower()
    
    # Check for keyword matches
    for key, data in CLINICAL_DATABASE.items():
        for keyword in data["symptoms_matched"]:
            if keyword in text_lower:
                return key, data
                
    return "general", None

def get_clinical_analysis(symptom_text):
    """
    Returns condition lists and treatment plans based on symptom text parser
    """
    key, data = parse_symptoms(symptom_text)
    if data:
        return key, data["conditions"], data["treatment_plan"]
    else:
        return "general", DEFAULT_ANALYSIS["conditions"], DEFAULT_ANALYSIS["treatment_plan"]

def generate_health_history(days=7):
    """
    Generates realistic historical patient vitals and health analytics tracking data.
    """
    base_date = datetime.date.today() - datetime.timedelta(days=days-1)
    dates = [base_date + datetime.timedelta(days=i) for i in range(days)]
    
    # Generate shifting trends
    symptom_severity = [random.randint(4, 7) for _ in range(days-2)]
    symptom_severity.append(3) # Gradual improvement
    symptom_severity.append(2)
    
    heart_rate = [random.randint(72, 88) for _ in range(days)]
    water_intake = [random.randint(4, 6) for _ in range(days-2)] + [7, 8] # Improving hydration
    sleep_hours = [random.randint(5, 6) for _ in range(days-3)] + [7, 8, 8] # Improving sleep
    active_minutes = [random.randint(10, 20) for _ in range(days-2)] + [30, 35] # Regaining energy
    
    df = pd.DataFrame({
        "Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Symptom Severity (1-10)": symptom_severity,
        "Avg Heart Rate (BPM)": heart_rate,
        "Water Intake (Glasses)": water_intake,
        "Sleep Duration (Hours)": sleep_hours,
        "Active Minutes": active_minutes
    })
    
    return df

def get_simulated_chat_response(query_text):
    """
    Empathetic chatbot query router
    """
    q = query_text.lower()
    if "emergency" in q or "die" in q or "heart attack" in q or "severe pain" in q or "911" in q:
        return CHAT_DIALOGUES["emergency"]
    elif "migraine" in q or "headache" in q or "head hurt" in q:
        return CHAT_DIALOGUES["migraine"]
    elif "flu" in q or "fever" in q or "cough" in q or "cold" in q:
        return CHAT_DIALOGUES["flu"]
    elif "joint" in q or "knee" in q or "stiff" in q or "arthritis" in q:
        return CHAT_DIALOGUES["joint_stiffness"]
    elif "anxious" in q or "anxiety" in q or "scared" in q or "worry" in q:
        return CHAT_DIALOGUES["anxiety"]
    elif "hello" in q or "hi" in q or "hey" in q:
        return CHAT_DIALOGUES["hello"]
    else:
        return CHAT_DIALOGUES["default"]
