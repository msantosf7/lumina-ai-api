import json
import os
import uuid
import time
import requests

COMFY_URL = "http://localhost:8188"

import base64
import io

def upload_image(image_base64):
    """Uploads a base64 image to ComfyUI and returns the filename."""
    try:
        # Decode base64
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,")[1]
        
        image_data = base64.b64decode(image_base64)
        
        files = {"image": ("reference.png", image_data)}
        response = requests.post(f"{COMFY_URL}/upload/image", files=files, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("name")
        return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def generate_image(prompt, reference, preset):
    # Use workflow_advanced if reference exists, else workflow_basic
    is_advanced = reference is not None and len(reference.strip()) > 0
    workflow_file = "workflow_advanced.json" if is_advanced else "workflow_basic.json"
    
    workflow_path = os.path.join(os.path.dirname(__file__), workflow_file)
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)

    # Load professional styles
    styles_path = os.path.join(os.path.dirname(__file__), "professional_styles.json")
    try:
        with open(styles_path, 'r') as f:
            styles = json.load(f)
    except Exception:
        styles = {}

    # Get style fragments
    style = styles.get(preset, styles.get("photorealistic"))
    pos_style = style.get("positive", "")
    neg_style = style.get("negative", "")

    # Inject dynamic prompts
    workflow["6"]["inputs"]["text"] = f"{pos_style}, {prompt}"
    workflow["7"]["inputs"]["text"] = neg_style

    # Handle Reference Image (IP-Adapter)
    if is_advanced:
        uploaded_filename = upload_image(reference)
        if uploaded_filename:
            workflow["12"]["inputs"]["image"] = uploaded_filename
        else:
            # Fallback to basic if upload fails (optional)
            print("Failed to upload reference image, falling back to text-only.")

    payload = {
        "prompt": workflow,
        "client_id": str(uuid.uuid4())
    }

    try:
        # 1. Send Prompt
        response = requests.post(f"{COMFY_URL}/prompt", json=payload, timeout=10)
        if response.status_code != 200:
            return {"status": "error", "message": f"ComfyUI Error {response.status_code}: {response.text}"}
        
        prompt_id = response.json().get('prompt_id')
        if not prompt_id:
            return {"status": "error", "message": "Failed to get prompt_id from ComfyUI"}

        # 2. Poll for Completion
        retries = 300 # Increase wait for complex generations on slow hardware (5 mins)
        while retries > 0:
            history_response = requests.get(f"{COMFY_URL}/history/{prompt_id}")
            if history_response.status_code == 200:
                history = history_response.json()
                if prompt_id in history:
                    outputs = history[prompt_id].get('outputs', {})
                    for node_id in outputs:
                        if 'images' in outputs[node_id]:
                            image_data = outputs[node_id]['images'][0]
                            filename = image_data['filename']
                            subfolder = image_data.get('subfolder', '')
                            return f"{COMFY_URL}/view?filename={filename}&subfolder={subfolder}&type=output"
            
            time.sleep(1)
            retries -= 1

        return {"status": "error", "message": "Timeout waiting for image generation"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
