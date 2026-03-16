import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.services.gemini import generate_image_gemini
from app.schemas.generation import GenerationRequest

def test_gemini_integration():
    print("Testing Gemini (Nano Banana 2) Integration...")
    
    # Mocking a prompt
    prompt = "A futuristic city with neon lights and flying cars"
    preset = "photorealistic"
    
    print(f"Prompt: {prompt}")
    print(f"Preset: {preset}")
    
    # We call the service. We expect an error if API_KEY is missing, 
    # but we want to see if the imports and logic flow work.
    result = generate_image_gemini(prompt=prompt, preset=preset)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    test_gemini_integration()
