from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from app.models.resume import ResumeInput, ResumeOutput
from app.services.llm_service import generate_resume_content
from app.utils.logger import app_logger

router = APIRouter()

@router.post("/generate", response_model=ResumeOutput)
async def generate_resume(input_data: ResumeInput = Body(...)):
    try:
        # Generate resume using LLM
        result = await generate_resume_content(
            name=input_data.name,
            position=input_data.position,
            additional_info=input_data.additional_info or {}
        )
        return result
    except Exception as e:
        app_logger.error(f"Error generating resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")

@router.post("/update", response_model=ResumeOutput)
async def update_resume(
    markdown_content: str = Body(...),
    name: str = Body("Xiao Han"),
    position: str = Body("Algorithm Engineer"),
    additional_info: Optional[Dict[str, Any]] = Body(None)
):
    try:
        # Update existing resume content
        result = await generate_resume_content(
            name=name,
            position=position,
            additional_info=additional_info or {},
            existing_content=markdown_content
        )
        return result
    except Exception as e:
        app_logger.error(f"Error updating resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating resume: {str(e)}")