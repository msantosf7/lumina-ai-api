from fastapi import APIRouter
from app.schemas.generation import GenerationRequest
from app.services.comfy import generate_image

router = APIRouter()

@router.post("/generate")
def generate(req: GenerationRequest):
    if req.provider == "gemini":
        from app.services.gemini import generate_image_gemini
        result = generate_image_gemini(
            prompt=req.prompt,
            reference_image=req.reference_image,
            preset=req.preset
        )
    else:
        # Default to ComfyUI
        result = generate_image(
            prompt=req.prompt,
            reference=req.reference_image,
            preset=req.preset
        )

    if isinstance(result, dict) and result.get("status") == "error":
        return result

    return {
        "status": "success",
        "image_url": result
    }
