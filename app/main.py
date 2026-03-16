from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.generate import router as generate_router
import os

app = FastAPI(
    title="Lumina AI API",
    description="API de geração de imagens do Lumina",
    version="1.0"
)

app.include_router(generate_router)

# Serve the test interface at /ui
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="ui")
