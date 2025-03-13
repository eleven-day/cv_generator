import re
from typing import Dict, List, Tuple

def extract_image_placeholders(markdown_content: str) -> Dict[str, str]:
    """
    Extract image placeholders from markdown content
    
    Args:
        markdown_content: Markdown text content
        
    Returns:
        Dictionary mapping placeholder IDs to descriptions
    """
    placeholders = {}
    placeholder_pattern = r'!\[(.*?)\]\(image:(.*?)\)'
    
    for match in re.finditer(placeholder_pattern, markdown_content):
        description = match.group(1)
        placeholder_id = match.group(2)
        placeholders[placeholder_id] = description
    
    return placeholders


def replace_placeholders_with_images(
    markdown_content: str, 
    image_data: Dict[str, str]
) -> str:
    """
    Replace image placeholders in markdown with actual image data URLs
    
    Args:
        markdown_content: Original markdown content with placeholders
        image_data: Dictionary mapping placeholder IDs to image data URLs
        
    Returns:
        Updated markdown with placeholders replaced by actual images
    """
    updated_content = markdown_content
    
    for placeholder_id, image_url in image_data.items():
        placeholder_pattern = f'!\\[(.*?)\\]\\(image:{placeholder_id}\\)'
        placeholder_regex = re.compile(placeholder_pattern)
        
        # Find all matches to preserve descriptions
        matches = list(placeholder_regex.finditer(updated_content))
        for match in matches:
            description = match.group(1)
            placeholder = match.group(0)
            replacement = f'![{description}]({image_url})'
            updated_content = updated_content.replace(placeholder, replacement)
    
    return updated_content