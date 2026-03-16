from pydantic import BaseModel
from typing import Optional

class GenerationRequest(BaseModel):
    prompt: str
    reference_image: Optional[str] = None
    preset: str = "photorealistic"
    provider: str = "comfyui"

class GenerationResponse(BaseModel):
    id: str
    status: str
    image_url: Optional[str] = None
