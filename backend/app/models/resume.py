from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ResumeBase(BaseModel):
    name: str = Field(..., description="Full name of the person")
    position: str = Field(..., description="Job position or title")


class ResumeInput(ResumeBase):
    experience: Optional[str] = Field(None, description="Work experience details")
    education: Optional[str] = Field(None, description="Education background")
    skills: Optional[str] = Field(None, description="Professional skills")
    contact: Optional[str] = Field(None, description="Contact information")
    additional_info: Optional[Dict[str, Any]] = Field(None, description="Any additional information")
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to format expected by the API"""
        additional_info = {}
        
        if self.experience:
            additional_info["experience"] = self.experience
        if self.education:
            additional_info["education"] = self.education
        if self.skills:
            additional_info["skills"] = self.skills
        if self.contact:
            additional_info["contact"] = self.contact
        if self.additional_info:
            additional_info.update(self.additional_info)
            
        return {
            "name": self.name,
            "position": self.position,
            "additional_info": additional_info
        }


class ResumeOutput(BaseModel):
    html_content: str = Field(..., description="Generated resume content in HTML format")
    image_placeholders: Dict[str, str] = Field(..., description="Image placeholders found in the content")


class ImageResponse(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    placeholder_id: str = Field(..., description="Identifier for the image placeholder")

class ImageGenerationInput(BaseModel):
    prompt: str
    placeholder_id: str

class ImageSearchInput(BaseModel):
    query: str
    placeholder_id: str


class SearchResult(ImageResponse):
    description: Optional[str] = Field(None, description="Description of the image")