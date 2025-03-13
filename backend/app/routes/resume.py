from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from app.models.resume import ResumeInput, ResumeOutput
from app.services.llm_service import generate_resume_content
from app.utils.logger import app_logger

router = APIRouter()

@router.post("/generate", response_model=ResumeOutput)
def generate_resume(input_data: ResumeInput = Body(...)):
    try:
        # Generate resume using LLM
        result = generate_resume_content(
            name=input_data.name,
            position=input_data.position,
            additional_info=input_data.additional_info or {}
        )
        return result
    except Exception as e:
        app_logger.error(f"Error generating resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")

@router.post("/update", response_model=ResumeOutput)
def update_resume(
    markdown_content: str = Body(...),
    name: str = Body("Xiao Han"),
    position: str = Body("Algorithm Engineer"),
    additional_info: Optional[Dict[str, Any]] = Body(None)
):
    try:
        # Update existing resume content
        result = generate_resume_content(
            name=name,
            position=position,
            additional_info=additional_info or {},
            existing_content=markdown_content
        )
        return result
    except Exception as e:
        app_logger.error(f"Error updating resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating resume: {str(e)}")
    
# 当运行此脚本是，测试一下这个接口的功能函数generate_resume，update_resume
if __name__ == "__main__":
    from app.models.resume import ResumeInput

    # Test generate_resume
    def test_generate_resume():
        # Create a test ResumeInput object
        test_request = ResumeInput(
            name="Xiao Han",
            position="Algorithm Engineer",
            additional_info={}
        )

        # Run the test
        result = generate_resume(test_request)
        print(result)

    # Test update_resume
    def test_update_resume():
        # Create a test markdown content
        test_markdown = "**Test**"

        # Run the test
        result = update_resume(test_markdown)
        print(result)

    test_generate_resume()
    test_update_resume()