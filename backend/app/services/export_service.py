import os
import markdown
import tempfile
from weasyprint import HTML, CSS
from app.utils.logger import app_logger

# Add support for other formats
import pypandoc

def export_resume(html_content: str, output_format: str, output_path: str) -> str:
    """
    Export resume HTML to various formats
    
    Args:
        html_content: The HTML content to export
        output_format: The desired output format (pdf, docx, pptx, md, html)
        output_path: Path where the exported file should be saved
        
    Returns:
        Path to the exported file
    """
    app_logger.info(f"Exporting resume to {output_format} format")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    if output_format == "html":
        # Simply save the HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        app_logger.info(f"Exported HTML to {output_path}")
        return output_path
    
    elif output_format == "md":
        # Convert HTML to markdown using pypandoc
        try:
            md_content = pypandoc.convert_text(html_content, 'md', format='html')
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            app_logger.info(f"Exported markdown to {output_path}")
            return output_path
        except Exception as e:
            app_logger.error(f"Error converting HTML to markdown: {str(e)}")
            raise
    
    elif output_format == "pdf":
        # Save HTML to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
            temp_html_path = temp.name
            temp.write(html_content.encode('utf-8'))
        
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
        # Save HTML to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
            temp_html_path = temp.name
            temp.write(html_content.encode('utf-8'))
        
        try:
            # Run pandoc to convert HTML to the desired format
            app_logger.info(f"Converting to {output_format} using pandoc")
            pypandoc.convert_file(
                temp_html_path,
                output_format,
                outputfile=output_path,
                extra_args=['--standalone']
            )
            app_logger.info(f"Exported {output_format.upper()} to {output_path}")
            return output_path
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
    
    else:
        error_msg = f"Unsupported output format: {output_format}"
        app_logger.error(error_msg)
        raise ValueError(error_msg)
    
# 当运行此脚本是，测试一下这个接口的功能函数convert_resume
if __name__ == "__main__":
    from app.models.export import ExportFormat
    from app.models.export import ExportRequest

    # Create a test ExportRequest object
    test_request = ExportRequest(
        html_content="<div>Test HTML content</div>",
        format=ExportFormat.PDF,
        filename="test"
    )

    # Run the test
    export_resume(test_request.html_content, test_request.format.value, f"test.{test_request.format.value}")