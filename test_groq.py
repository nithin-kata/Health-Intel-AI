# test_groq.py - Diagnostics
import os
import sys
import traceback

def load_dotenv(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, val = line.split("=", 1)
                        val = val.strip().strip("'\"")
                        os.environ[key.strip()] = val

def run_test():
    print("Testing Groq API...")
    try:
        load_dotenv()
        from openai import OpenAI
        print("openai version:", sys.modules.get('openai').__version__ if 'openai' in sys.modules else 'unknown')
        
        # Initialize client with user's key from environment
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env or environment")
            
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Respond with 'Success' if you can read this."}
            ],
            temperature=0.2
        )
        print("Success! Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("\n--- ERROR DETECTED ---")
        print("Exception class:", e.__class__.__name__)
        print("Exception message:", str(e))
        print("\nTraceback:")
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
