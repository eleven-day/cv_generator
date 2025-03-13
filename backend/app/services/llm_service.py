from typing import Dict, Any, Optional
import re
import os
from google import genai
from google.genai import types
from app.utils.logger import app_logger
from app.utils.markdown_helpers import extract_image_placeholders

# Initialize Google Gemini API client
API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")  # Replace with your API key in production
genai.configure(api_key=API_KEY)

PROMPT_TEMPLATE = """
<Background>
You are an AI resume writer skilled at creating professional, concise, and well-formatted resumes.
</Background>

<Role>
Resume Writer
</Role>

<Task>
Create a professional resume in markdown format for the user based on the provided information.
</Task>

<Style>
- Professional and concise
- Well-organized sections (Personal Info, Summary, Experience, Education, Skills, etc.)
- Clean formatting with appropriate headings, bullet points, and spacing
- Image placeholders marked with special syntax: ![description](image:placeholder_id)
</Style>

<Metrics>
- Length: Content should fit on a single A4 page
- Focus on relevant information only
- Use professional language and industry-appropriate terminology
</Metrics>

<User Input>
Name: {name}
Position: {position}
{additional_info}
</User Input>

<Output Format>
Provide a complete resume in markdown format. For any images (profile photo, icons, etc.), 
use the placeholder syntax: ![description](image:placeholder_id) where placeholder_id is a unique identifier.
</Output Format>
"""

async def generate_resume_content(
    name: str,
    position: str,
    additional_info: Dict[str, Any] = None,
    existing_content: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate resume content using Google Gemini API
    
    Args:
        name: User's name
        position: Job position
        additional_info: Additional resume information
        existing_content: Existing markdown content to update
        
    Returns:
        Dictionary with markdown content and image placeholders
    """
    app_logger.info(f"Generating resume for {name}, position: {position}")
    
    additional_info_str = ""
    if additional_info:
        for key, value in additional_info.items():
            additional_info_str += f"{key}: {value}\n"
    
    # Create the prompt
    if existing_content:
        # If updating existing content, use a different prompt
        app_logger.info("Updating existing resume content")
        prompt = f"""
        <Background>
        You are an AI resume writer skilled at updating professional resumes.
        </Background>

        <Role>
        Resume Writer
        </Role>

        <Task>
        Update the existing resume markdown with new information while maintaining the format.
        </Task>

        <User Input>
        Name: {name}
        Position: {position}
        {additional_info_str}
        </User Input>

        <Existing Resume>
        {existing_content}
        </Existing Resume>

        <Output Format>
        Provide the updated resume in markdown format. Maintain the existing image placeholders.
        </Output Format>
        """
    else:
        # Create a new resume
        app_logger.info("Creating new resume content")
        prompt = PROMPT_TEMPLATE.format(
            name=name,
            position=position,
            additional_info=additional_info_str
        )
    
    try:
        # Generate content using Gemini
        client = genai.Client()
        response = await client.models.generate_content_async(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=2000,
                temperature=0.2
            )
        )
        
        markdown_content = response.text
        
        # Extract image placeholders
        image_placeholders = extract_image_placeholders(markdown_content)
        
        app_logger.info(f"Resume generated successfully with {len(image_placeholders)} image placeholders")
        
        return {
            "markdown_content": markdown_content,
            "image_placeholders": image_placeholders
        }
    except Exception as e:
        app_logger.error(f"Error generating resume content: {str(e)}")
        raise