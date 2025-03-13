import base64
from io import BytesIO
from PIL import Image, ImageDraw
import random
from typing import Tuple

def create_placeholder_image(
    width: int = 200, 
    height: int = 200, 
    text: str = "Placeholder", 
    bg_color: Tuple[int, int, int] = None
) -> str:
    """
    Create a simple placeholder image with text
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        text: Text to display on the placeholder
        bg_color: Background color as RGB tuple (random if None)
        
    Returns:
        Base64 encoded data URL for the image
    """
    # Use random color if none specified
    if bg_color is None:
        bg_color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(100, 200)
        )
    
    # Create image and drawing context
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add a border
    border_width = 4
    draw.rectangle(
        [(border_width, border_width), (width-border_width, height-border_width)],
        outline=(255, 255, 255),
        width=border_width
    )
    
    # Add text
    text_color = (255, 255, 255)
    text_position = (width//2, height//2)
    
    # Draw centered text (simplified, no font loading)
    draw.text(
        text_position, 
        text, 
        fill=text_color, 
        anchor="mm"  # Center alignment
    )
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def resize_image(image_data: bytes, max_width: int = 800, max_height: int = 800) -> bytes:
    """
    Resize an image to fit within the specified dimensions while maintaining aspect ratio
    
    Args:
        image_data: Raw image bytes
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Resized image bytes
    """
    img = Image.open(BytesIO(image_data))
    
    # Calculate new dimensions while preserving aspect ratio
    width, height = img.size
    
    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Convert back to bytes
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

if __name__ == "__main__":
    # Test the image helpers
    placeholder_image = create_placeholder_image(
        width=400, 
        height=200, 
        text="Hello, World!", 
        bg_color=(100, 150, 200)
    )
    print(placeholder_image)
    
    # Load an example image
    with open("example.jpg", "rb") as f:
        image_data = f.read()
    
    # Resize the image
    resized_image = resize_image(image_data, max_width=800, max_height=600)
    print(f"Original size: {len(image_data)} bytes, Resized size: {len(resized_image)} bytes")