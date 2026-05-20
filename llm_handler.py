# llm_handler.py - Groq API Integration Client

import json
from openai import OpenAI

def get_groq_client(api_key):
    """
    Returns an OpenAI-compatible client pointed at the Groq LPU API.
    """
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def analyze_symptoms_groq(api_key, symptom_text, demographics, severity, duration, model="llama-3.3-70b-versatile"):
    """
    Calls the Groq API to perform a structured clinical symptom analysis.
    Demographics: dict with age, gender, medical history, medications.
    """
    client = get_groq_client(api_key)
    
    system_prompt = """You are a world-class clinical pre-screening AI designed to analyze user symptoms and provide educational guidance.
Your goal is to parse the user's symptoms, weigh clinical factors including patient demographics, and provide a highly structured, accurate analysis.

RULES:
1. Be medically rigorous yet easy to understand for patients.
2. Provide an honest clinical likelihood assessment based on demographics.
3. Categorize risk strictly as LOW, MEDIUM, or HIGH.
4. Supply actionable, science-based lifestyle and dietary suggestions.
5. Highlight critical "Red Flag" warning symptoms that warrant immediate emergency room care.
6. YOU MUST ONLY RESPOND IN VALID JSON FORMAT. Do not wrap in markdown blocks, except standard JSON.

Expected Output Format:
{
  "conditions": [
    {
      "name": "Condition name",
      "likelihood": 65,
      "risk": "HIGH",
      "nlp_reason": "Medical reasoning including how patient age/gender/history influenced this prediction."
    }
  ],
  "treatment_plan": {
    "immediate_actions": [
      "Action step 1",
      "Action step 2"
    ],
    "lifestyle": [
      "Lifestyle modification 1",
      "Lifestyle modification 2"
    ],
    "dietary": [
      "Dietary recommendation 1",
      "Dietary recommendation 2"
    ],
    "red_flags": [
      "Critical warning symptom 1",
      "Critical warning symptom 2"
    ]
  }
}
"""

    user_content = f"""
Patient Demographics:
- Age: {demographics.get('age')}
- Gender: {demographics.get('gender')}
- Pre-existing Conditions: {demographics.get('pre_existing')}
- Active Medications: {demographics.get('medications')}

Symptom Presentation:
- Symptom Description: "{symptom_text}"
- Severity Level: {severity}/10
- Duration of Symptoms: {duration}

Please analyze these symptoms and provide a comprehensive structured medical assessment strictly adhering to the JSON schema.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result_json = json.loads(response.choices[0].message.content.strip())
        return result_json
        
    except Exception as e:
        # Reraise or handle gracefully in front-end
        raise RuntimeError(f"Groq API call failed: {str(e)}")

def chat_with_empathy_groq(api_key, conversation_history, user_message, demographics, model="llama-3.3-70b-versatile"):
    """
    Enables a 24/7 patient conversational stream using Groq's high-speed API.
    Empathizes with the patient's state and uses demographics as context.
    """
    client = get_groq_client(api_key)
    
    system_prompt = f"""You are a 24/7 empathetic, highly intelligent AI Medical Assistant. Your role is to answer patient questions, clarify medical queries, and ease anxiety while maintaining professional clinical standards.

Patient Context:
- Age: {demographics.get('age')}, Gender: {demographics.get('gender')}
- Pre-existing Conditions: {demographics.get('pre_existing')}

GUIDELINES:
1. Speak with a warm, caring tone. Match the patient's emotional state.
2. Ground all answers in established clinical guidelines and medical facts.
3. Be transparent about uncertainties.
4. Keep your explanations clear, simple, and free of unnecessary medical jargon.
5. Emphasize that you are an informational pre-screening assistant and cannot replace in-person diagnosis.
6. If the patient describes life-threatening signs (e.g. crushing chest pain, paralysis, sudden extreme breathlessness), instantly instruct them to call 911/emergency services immediately.
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    # Append conversation history
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Append the new user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq Chat API call failed: {str(e)}")
