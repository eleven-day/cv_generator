import React from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/ResumePreview.css';

const ResumePreview = ({ markdownContent, imagePlaceholders, imageData }) => {
  // Function to process markdown content and replace image placeholders with actual images
  const processMarkdown = (content) => {
    let processedContent = content;
    
    // Replace placeholders with actual images if available
    Object.entries(imagePlaceholders).forEach(([id, description]) => {
      const placeholderRegex = new RegExp(`!\\[${description}\\]\\(image:${id}\\)`, 'g');
      
      if (imageData[id]) {
        processedContent = processedContent.replace(
          placeholderRegex,
          `![${description}](${imageData[id]})`
        );
      } else {
        // Leave the placeholder as is, it will be rendered as text
        processedContent = processedContent.replace(
          placeholderRegex,
          `[Image Placeholder: ${description}]`
        );
      }
    });
    
    return processedContent;
  };

  return (
    <div className="resume-preview">
      <h2>Resume Preview</h2>
      <div className="preview-container">
        <div className="preview-page">
          <ReactMarkdown>
            {processMarkdown(markdownContent)}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResumePreview;