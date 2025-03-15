import React, { useMemo } from 'react';
import '../styles/ResumePreview.css';

const ResumePreview = ({ htmlContent, imagePlaceholders, imageData }) => {
  // Process HTML content to replace image placeholders with actual images
  const processedHtml = useMemo(() => {
    if (!htmlContent) return '';
    
    let processedContent = htmlContent;
    
    // Replace placeholders with actual images if available
    Object.entries(imagePlaceholders).forEach(([id, description]) => {
      if (imageData[id]) {
        const placeholderRegex = new RegExp(`src="image:${id}"`, 'g');
        processedContent = processedContent.replace(
          placeholderRegex,
          `src="${imageData[id]}"`
        );
      }
    });
    
    return processedContent;
  }, [htmlContent, imagePlaceholders, imageData]);

  return (
    <div className="resume-preview">
      <div className="preview-container">
        <iframe
          title="Resume Preview"
          srcDoc={processedHtml}
          className="preview-iframe"
          sandbox="allow-same-origin"
        />
      </div>
    </div>
  );
};

export default ResumePreview;