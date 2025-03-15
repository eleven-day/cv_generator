import React from 'react';
import '../styles/ResumeEditor.css';

const ResumeEditor = ({ htmlContent, onUpdateContent }) => {
  const handleChange = (e) => {
    onUpdateContent(e.target.value);
  };

  return (
    <div className="html-editor">
      <div className="editor-info">
        <p>Edit your resume HTML content directly. Be careful not to break the structure.</p>
      </div>
      <textarea
        value={htmlContent}
        onChange={handleChange}
        className="html-textarea"
        spellCheck="false"
        placeholder="Your HTML content will appear here..."
      />
    </div>
  );
};

export default ResumeEditor;