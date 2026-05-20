# test_groq.py - Diagnostics
import sys
import traceback

def run_test():
    print("Testing Groq API...")
    try:
        from openai import OpenAI
        print("openai version:", sys.modules.get('openai').__version__ if 'openai' in sys.modules else 'unknown')
        
        # Initialize client with user's key
        api_key = "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"
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
