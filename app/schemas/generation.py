from typing import Optional, List

class GenerationRequest(BaseModel):
    prompt: str
    reference_image: Optional[str] = None # Legacy support
    images: Optional[List[str]] = None      # Multi-image support
    preset: str = "raw"
    provider: str = "gemini"

class GenerationResponse(BaseModel):
    id: str
    status: str
    image_url: Optional[str] = None
