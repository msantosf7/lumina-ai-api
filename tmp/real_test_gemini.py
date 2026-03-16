import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.gemini import generate_image_gemini

def run_real_test():
    print("--- Nano Banana 2 (Gemini 3.1 Flash) Real Test ---")
    
    # Load .env to ensure we have the key
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key or "your_api_key_here" in api_key:
        print("ERROR: GOOGLE_API_KEY not found or invalid in .env")
        return

    print("API Key found. Attempting generation...")
    
    prompt = "A cute robot holding a sign that says 'Lumina AI', digital art style"
    preset = "artistic"
    
    result = generate_image_gemini(prompt=prompt, preset=preset)
    
    print("\n--- TEST RESULT ---")
    if result.get("status") == "success":
        print("SUCCESS!")
        print(f"Message: {result.get('message')}")
        if "response_text" in result:
            print("Response Snippet:", result["response_text"][:200])
    else:
        print("FAILED!")
        print(f"Error Message: {result.get('message')}")

if __name__ == "__main__":
    run_real_test()
