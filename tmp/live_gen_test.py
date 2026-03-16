import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.gemini import generate_image_gemini

def test_live_generation():
    print("--- Nano Banana 2 (Gemini 3.1 Flash) Live Generation ---")
    
    # Load .env
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY is missing!")
        return

    # A creative prompt for the first image
    prompt = "A majestic glowing phoenix rising from digital ashes, synthwave aesthetic, vibrant purple and orange colors, 4k ultra detailed"
    preset = "cinematic"
    
    print(f"Prompt: {prompt}")
    print(f"Preset: {preset}")
    print("Generating... (This may take a moment)")
    
    result = generate_image_gemini(prompt=prompt, preset=preset)
    
    print("\n--- RESULT ---")
    if result.get("status") == "success":
        print("SUCCESS! Nano Banana 2 worked.")
        print(f"Message: {result.get('message')}")
        
        # If the response contains text/reasoning
        if "response_text" in result:
            print("\nModel Response:")
            print(result["response_text"])
            
        # If it's a multimodal response, the SDK might have saved the image or 
        # it might be in the raw response. 
        # In a real environment, we'd handle the image extraction here.
    else:
        print("FAILED!")
        print(f"Error: {result.get('message')}")
        if "raw_response" in result:
             print("Raw Details:", result["raw_response"])

if __name__ == "__main__":
    test_live_generation()
