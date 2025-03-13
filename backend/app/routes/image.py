from fastapi import APIRouter, HTTPException, UploadFile, File, Body, Form
from typing import List
from app.models.resume import ImageResponse, ImageGenerationInput, ImageSearchInput
from app.services.image_service import (
    process_uploaded_image,
    search_image,
    generate_image
)
from app.utils.logger import app_logger

router = APIRouter()

@router.post("/upload", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    placeholder_id: str = Form(...)
):
    try:
        result = await process_uploaded_image(file, placeholder_id)
        return result
    except Exception as e:
        app_logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/search", response_model=List[ImageResponse])
async def search_for_image(input_data: ImageSearchInput):
    try:
        results = await search_image(input_data.query, input_data.placeholder_id)
        return results
    except Exception as e:
        app_logger.error(f"Error searching for image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching for image: {str(e)}")

@router.post("/generate", response_model=ImageResponse)
async def generate_image_from_prompt(input_data: ImageGenerationInput):
    try:
        result = await generate_image(input_data.prompt, input_data.placeholder_id)
        return result
    except Exception as e:
        app_logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")