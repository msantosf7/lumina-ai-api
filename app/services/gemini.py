import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import requests
import json
import base64
import io

def generate_image_gemini(prompt, reference_image=None, images=None, preset="raw"):
    """
    Generates an image using Gemini 3.1 Flash Image (Nano Banana 2).
    """
    try:
        # Load environment variables (to capture recent changes)
        load_dotenv()
        
        # Configure the API key dynamically
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {"status": "error", "message": "GOOGLE_API_KEY NOT FOUND in environment or .env file."}
        
        genai.configure(api_key=api_key)
        # Load professional styles
        styles_path = os.path.join(os.path.dirname(__file__), "professional_styles.json")
        try:
            with open(styles_path, 'r', encoding='utf-8') as f:
                styles = json.load(f)
        except Exception:
            styles = {}

        # Get style fragments only if preset is provided and not "raw"
        pos_style = ""
        neg_style = ""
        
        if preset and preset != "raw":
            style = styles.get(preset, {})
            pos_style = style.get("positive", "")
            neg_style = style.get("negative", "")

        # Construct the final prompt
        if pos_style:
            final_prompt = f"{pos_style}, {prompt}"
        else:
            final_prompt = prompt
            
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
        
        # Handle reference images (Multimodal)
        inputs = [final_prompt]
        
        # Combine single reference_image and multiple images list
        image_sources = []
        if images:
            image_sources.extend(images)
        if reference_image:
            image_sources.append(reference_image)

        for img_src in image_sources:
            if not img_src:
                continue
                
            # Clean base64 header if present
            if isinstance(img_src, str) and "base64," in img_src:
                actual_data = img_src.split("base64,")[1]
            else:
                actual_data = img_src
            
            try:
                # Decode base64 to bytes
                image_data = base64.b64decode(actual_data)
                inputs.append({
                    "mime_type": "image/png",
                    "data": image_data
                })
            except Exception as e:
                print(f"Error decoding image part: {e}")

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
