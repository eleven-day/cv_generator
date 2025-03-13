import os
import markdown
import tempfile
from typing import Dict, Any
import asyncio
import subprocess
from pathlib import Path
from weasyprint import HTML, CSS
from app.utils.logger import app_logger

# Add support for other formats
import pypandoc

async def export_resume(markdown_content: str, output_format: str, output_path: str) -> str:
    """
    Export resume markdown to various formats
    
    Args:
        markdown_content: The markdown content to export
        output_format: The desired output format (pdf, docx, pptx, md, html)
        output_path: Path where the exported file should be saved
        
    Returns:
        Path to the exported file
    """
    app_logger.info(f"Exporting resume to {output_format} format")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    if output_format == "md":
        # Simply save the markdown
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        app_logger.info(f"Exported markdown to {output_path}")
        return output_path
    
    elif output_format == "html":
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Add styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    max-width: 8.5in;
                    margin: 0 auto;
                    padding: 1in;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    text-align: center;
                    margin-bottom: 0.5em;
                }}
                h2 {{
                    border-bottom: 1px solid #eee;
                    padding-bottom: 0.3em;
                }}
                img {{
                    max-width: 100%;
                }}
                .profile-img {{
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin: 0 auto;
                    display: block;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(styled_html)
        app_logger.info(f"Exported HTML to {output_path}")
        return output_path
    
    elif output_format == "pdf":
        # First convert to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Create styled HTML
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Resume</title>
            <style>
                @page {{
                    size: A4;
                    margin: 1cm;
                }}
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    text-align: center;
                    margin-bottom: 0.5em;
                }}
                h2 {{
                    border-bottom: 1px solid #eee;
                    padding-bottom: 0.3em;
                }}
                img {{
                    max-width: 100%;
                }}
                .profile-img {{
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin: 0 auto;
                    display: block;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Save to a temporary HTML file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
            temp_html_path = temp.name
            temp.write(styled_html.encode('utf-8'))
        
        try:
            # Convert HTML to PDF using WeasyPrint
            HTML(temp_html_path).write_pdf(output_path)
            app_logger.info(f"Exported PDF to {output_path}")
            return output_path
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
    
    elif output_format == "docx" or output_format == "pptx":
        # Use pandoc for conversion to docx/pptx
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp:
            temp_md_path = temp.name
            temp.write(markdown_content.encode('utf-8'))
        
        try:
            # Run pandoc to convert markdown to the desired format
            app_logger.info(f"Converting to {output_format} using pandoc")
            pypandoc.convert_file(
                temp_md_path,
                output_format,
                outputfile=output_path,
                extra_args=['--standalone']
            )
            app_logger.info(f"Exported {output_format.upper()} to {output_path}")
            return output_path
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_md_path):
                os.unlink(temp_md_path)
    
    else:
        error_msg = f"Unsupported output format: {output_format}"
        app_logger.error(error_msg)
        raise ValueError(error_msg)
    
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
    asyncio.run(export_resume(test_request.markdown_content, test_request.format.value, f"test.{test_request.format.value}"))