from pydantic import BaseModel, Field
from enum import Enum


class ExportFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    MD = "md"
    HTML = "html"


class ExportRequest(BaseModel):
    html_content: str = Field(..., description="Resume content in HTML format")
    format: ExportFormat = Field(..., description="Desired export format")
    filename: str = Field("resume", description="Name for the exported file (without extension)")