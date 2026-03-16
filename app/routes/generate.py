from fastapi import APIRouter
from app.schemas.generation import GenerationRequest
from app.services.gemini import generate_image_gemini

router = APIRouter()

@router.post("/generate")
def generate(req: GenerationRequest):
    # Nano Banana 2 (Gemini) is now the primary provider
    result = generate_image_gemini(
        prompt=req.prompt,
        reference_image=req.reference_image,
        images=req.images,
        preset=req.preset
    )

    if isinstance(result, dict) and result.get("status") == "error":
        return result

    return {
        "status": "success",
        "image_url": result
    }
