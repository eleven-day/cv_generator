from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
import tempfile
import os
from app.models.export import ExportRequest
from app.services.export_service import export_resume
from app.utils.logger import app_logger

router = APIRouter()

@router.post("/convert")
async def convert_resume(input_data: ExportRequest = Body(...)):
    try:
        # Create a temporary file for the exported resume
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{input_data.format.value}") as temp_file:
            temp_filename = temp_file.name
        
        # Export the resume to the specified format
        await export_resume(
            markdown_content=input_data.markdown_content,
            output_format=input_data.format.value,
            output_path=temp_filename
        )
        
        # Return the file for download
        return FileResponse(
            path=temp_filename,
            filename=f"{input_data.filename}.{input_data.format.value}",
            media_type=f"application/{input_data.format.value}",
            background=lambda: os.unlink(temp_filename)  # Delete after download
        )
    except Exception as e:
        app_logger.error(f"Error exporting resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting resume: {str(e)}")
    
# 当运行此脚本是，测试一下这个接口的功能函数convert_resume
if __name__ == "__main__":
    from app.models.export import ExportFormat
    from app.models.export import ExportRequest
    import asyncio

    # Create a test ExportRequest object
    test_request = ExportRequest(
        markdown_content="**Test**",
        format=ExportFormat.PDF,
        filename="test"
    )

    # Run the test
    asyncio.run(convert_resume(test_request))