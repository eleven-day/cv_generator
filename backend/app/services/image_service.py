from fastapi import UploadFile
from typing import Dict, List, Any
import base64
import io
from PIL import Image
import os
import aiohttp
import asyncio
from urllib.parse import quote_plus
from google import genai
from google.genai import types
import uuid
from app.utils.logger import app_logger
from app.utils.image_helpers import create_placeholder_image, resize_image

# Initialize Google Gemini API client
API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")  # Replace with your API key in production

def process_uploaded_image(file: UploadFile, placeholder_id: str) -> Dict[str, Any]:
    """
    Process an uploaded image file
    
    Args:
        file: The uploaded image file
        placeholder_id: The ID of the placeholder to replace
        
    Returns:
        Dictionary with base64 encoded image and placeholder ID
    """
    # Read and process the image
    content = file.read()
    
    # Resize if necessary
    content = resize_image(content, max_width=500, max_height=500)
    
    # Convert to base64
    img_str = base64.b64encode(content).decode()
    
    app_logger.info(f"Processed uploaded image for placeholder {placeholder_id}")
    
    return {
        "image_data": f"data:image/png;base64,{img_str}",
        "placeholder_id": placeholder_id
    }

async def search_image(
    query: str, 
    placeholder_id: str, 
    timeout: float = 10.0
) -> Dict[str, str]:
    """
    Search for an image based on a text query using Unsplash API
    
    Args:
        query: The search query
        placeholder_id: The ID of the placeholder to replace
        timeout: Timeout in seconds for the API request (default: 10.0)
        
    Returns:
        Dictionary with format: {"image_data": str, "placeholder_id": str}
        
    Raises:
        TimeoutError: If the API request exceeds the timeout
        ValueError: If invalid parameters are provided or no images found
    """
    # Input validation
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    
    # Get API key from environment variable
    api_key = os.environ.get("UNSPLASH_API_KEY", None)
    if not api_key:
        app_logger.error("Unsplash API key not found in environment variables")
        # Fallback to a placeholder image
        img_data = create_placeholder_image(
            width=400, 
            height=400,
            text=f"No API Key\n(Placeholder)",
            bg_color=(200, 100, 100)
        )
        return {
            "image_data": img_data,
            "placeholder_id": placeholder_id
        }
    
    # Log the search operation
    app_logger.info(f"Searching Unsplash for '{query}' with placeholder ID: {placeholder_id}")
    
    try:
        # Perform the API request to Unsplash
        encoded_query = quote_plus(query)
        url = f"https://api.unsplash.com/search/photos?query={encoded_query}&per_page=1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, 
                headers={"Authorization": f"Client-ID {api_key}"},
                timeout=timeout
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    app_logger.error(f"Unsplash API error: {response.status} - {error_text}")
                    raise ValueError(f"API returned status code {response.status}")
                
                data = await response.json()
                
                # Get the first result
                results = data.get("results", [])
                if not results:
                    app_logger.warning(f"No image results found for query: {query}")
                    raise ValueError(f"No images found for query: {query}")
                
                img_data = results[0]
                img_url = img_data.get("urls", {}).get("small")
                if not img_url:
                    raise ValueError("Invalid image data received from API")
                
                # Download the image
                async with session.get(img_url, timeout=timeout) as img_response:
                    if img_response.status != 200:
                        app_logger.warning(f"Failed to download image")
                        raise ValueError("Failed to download image")
                    
                    img_bytes = await img_response.read()
                    
                    # Open and encode the image
                    img = Image.open(io.BytesIO(img_bytes))
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    
                    # Log attribution info (since we're not returning it)
                    photographer = img_data.get("user", {}).get("name", "Unknown")
                    unsplash_link = img_data.get("links", {}).get("html", "")
                    app_logger.info(f"Image by {photographer} from Unsplash: {unsplash_link}")
                    
                    # Return a single dictionary
                    return {
                        "image_data": f"data:image/jpeg;base64,{img_base64}",
                        "placeholder_id": placeholder_id
                    }
                
    except asyncio.TimeoutError:
        app_logger.error(f"Unsplash API request timed out for query: {query}")
    except Exception as e:
        app_logger.error(f"Error during Unsplash image search: {str(e)}")
    
    # Fallback to a placeholder image if search fails
    img_data = create_placeholder_image(
        width=400, 
        height=400,
        text=f"Image Search\n(Failed)",
        bg_color=(200, 150, 100)
    )
    
    return {
        "image_data": img_data,
        "placeholder_id": placeholder_id
    }

def generate_image(prompt: str, placeholder_id: str) -> Dict[str, Any]:
    """
    Generate an image from a text prompt using Gemini API
    
    Args:
        prompt: The text prompt for image generation
        placeholder_id: The ID of the placeholder to replace
        
    Returns:
        Dictionary with base64 encoded image and placeholder ID
    """
    app_logger.info(f"Generating image with prompt '{prompt}' for placeholder {placeholder_id}")
    
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # Get the generated image and convert to base64
        generated_image = response.generated_images[0]
        img_bytes = generated_image.image.image_bytes
        img_str = base64.b64encode(img_bytes).decode()
        
        return {
            "image_data": f"data:image/png;base64,{img_str}",
            "placeholder_id": placeholder_id
        }
    except Exception as e:
        app_logger.error(f"Error generating image: {str(e)}")
        # Fallback to a placeholder image if generation fails
        img_data = create_placeholder_image(
            width=400, 
            height=400,
            text=f"Generated Image\n(Placeholder)",
            bg_color=(100, 150, 200)
        )
        
        return {
            "image_data": img_data,
            "placeholder_id": placeholder_id
        }
    
# Test the image service functions
if __name__ == "__main__":
    # Test process_uploaded_image
    def test_process_uploaded_image():
        # Create a test UploadFile object
        test_file = UploadFile(
            filename="test.jpg",
            content_type="image/jpeg"
        )
        test_file.file = open("test.jpg", "rb")
        
        # Run the test
        result = process_uploaded_image(test_file, "test")
        print(result)
    
    # Test search_image
    async def test_search_image():
        # Run the test
        result = await search_image("cat", "cat")
        print(result)
    
    # Test generate_image
    def test_generate_image():
        # Run the test
        result = generate_image("A beautiful sunset over the ocean", "sunset")
        print(result)
    
    # Run the tests
    test_process_uploaded_image()
    asyncio.run(test_search_image())
    test_generate_image()