import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import requests

load_dotenv()

# Configure the API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def generate_image_gemini(prompt, reference_image=None, preset="photorealistic"):
    """
    Generates an image using Gemini 3.1 Flash Image (Nano Banana 2).
    """
    try:
        # Load professional styles
        styles_path = os.path.join(os.path.dirname(__file__), "professional_styles.json")
        try:
            with open(styles_path, 'r', encoding='utf-8') as f:
                styles = json.load(f)
        except Exception:
            styles = {}

        # Get style fragments
        style = styles.get(preset, styles.get("photorealistic", {}))
        pos_style = style.get("positive", "")
        neg_style = style.get("negative", "")

        # Construct the final prompt
        final_prompt = f"{pos_style}, {prompt}"
        if neg_style:
            final_prompt += f" NOT {neg_style}"

        # Initialize the model
        # Model name for Gemini 3.1 Flash Image is usually 'gemini-exp-1206' or similar 
        # but the request mentioned "Nano Banana 2" which maps to Gemini 3.1 Flash.
        # As of now, the most recent image generation model in Gemini is accessed via the Imagen 3 API 
        # usually within the 'gemini-1.5-flash' or 'gemini-2.0-flash' but for specialized image generation
        # it might require using the specifically named model if available in the SDK.
        # For this implementation, we'll use 'gemini-1.5-flash' as a placeholder or 
        # 'imagen-3' if the user's API key supports it directly.
        
        # PROMPT: "Nano Banana 2 is also known as Gemini 3.1 Flash Image"
        # Use the correct identifier for Gemini 3.1 Flash Image (Nano Banana 2)
        model_name = "gemini-3.1-flash-image-preview" 
        
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as e:
            return {"status": "error", "message": f"Model initialization failed: {str(e)}"}
        
        # Handle reference image if provided (Multimodal)
        inputs = [final_prompt]
        if reference_image:
            if "base64," in reference_image:
                reference_image = reference_image.split("base64,")[1]
            image_data = base64.b64decode(reference_image)
            
            image_part = {
                "mime_type": "image/png",
                "data": image_data
            }
            inputs.append(image_part)

        # Generate content
        response = model.generate_content(inputs)
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content.parts:
                    for part in candidate.content.parts:
                        # Check if the part contains image data
                        # The SDK sometimes has different property names for image bytes
                        image_bytes = None
                        if hasattr(part, 'inline_data') and part.inline_data:
                            image_bytes = part.inline_data.data
                        elif hasattr(part, 'image') and part.image:
                             image_bytes = part.image.data
                        
                        if image_bytes:
                            # Save image to static folder
                            static_outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "outputs")
                            if not os.path.exists(static_outputs_dir):
                                os.makedirs(static_outputs_dir)
                            
                            filename = f"gemini_{int(time.time())}.png"
                            filepath = os.path.join(static_outputs_dir, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(image_bytes)
                            
                            return f"/ui/outputs/{filename}"

        # Fallback if no image bytes found but text exists
        if hasattr(response, 'text') and response.text:
            return {
                "status": "success",
                "message": "Nano Banana 2 responded with text (possible reasoning), but no image data was found.",
                "response_text": response.text[:500]
            }
        
        return {"status": "error", "message": "No image data returned from Nano Banana 2."}

    except Exception as e:
        return {"status": "error", "message": f"Gemini Error: {str(e)}"}
