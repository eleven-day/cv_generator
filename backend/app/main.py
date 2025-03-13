from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routes import resume, image, export
from app.utils.logger import app_logger

app = FastAPI(
    title="Resume Generator API",
    description="API for generating and formatting resumes using LLM"
)

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(image.router, prefix="/api/image", tags=["Image"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])

# Serve static files if running in production mode (not in development)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app_logger.info(f"Serving static files from {static_dir}")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/api")
async def root():
    return {"message": "Resume Generator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)