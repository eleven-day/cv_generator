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
def upload_image(
    file: UploadFile = File(...),
    placeholder_id: str = Form(...)
):
    try:
        result = process_uploaded_image(file, placeholder_id)
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
        result = generate_image(input_data.prompt, input_data.placeholder_id)
        return result
    except Exception as e:
        app_logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")
    
# 当运行此脚本是，测试一下这个接口的功能函数upload_image，search_for_image，generate_image_from_prompt
if __name__ == "__main__":
    import asyncio
    from app.models.resume import ImageSearchInput, ImageGenerationInput

    # Test upload_image
    async def test_upload_image():
        from fastapi import UploadFile
        from fastapi.datastructures import UploadFile as UploadFileData
        from fastapi import Form

        # Create a test UploadFile object
        test_file = UploadFileData(
            filename="test.jpg",
            content_type="image/jpeg"
        )
        test_file.file = open("test.jpg", "rb")

        # Run the test
        upload_image(file=test_file, placeholder_id="test")

    # Test search_for_image
    async def test_search_for_image():
        # Create a test ImageSearchInput object
        test_input = ImageSearchInput(
            query="cat",
            placeholder_id="test"
        )

        # Run the test
        await search_for_image(test_input)

    # Test generate_image_from_prompt
    def test_generate_image_from_prompt():
        # Create a test ImageGenerationInput object
        test_input = ImageGenerationInput(
            prompt="A cat sitting on a table",
            placeholder_id="test"
        )

        # Run the test
        generate_image_from_prompt(test_input)

    # Run the tests
    asyncio.run(test_upload_image())
    asyncio.run(test_search_for_image())
    test_generate_image_from_prompt()