import React from 'react';
import SimpleMDE from 'react-simplemde-editor';
import 'easymde/dist/easymde.min.css';
import '../styles/ResumeEditor.css';

const ResumeEditor = ({ markdownContent, onUpdateContent }) => {
  const handleChange = (value) => {
    onUpdateContent(value);
  };

  const editorOptions = {
    autofocus: true,
    spellChecker: true,
    lineWrapping: true,
    placeholder: 'Edit your resume content here...',
    status: ['lines', 'words'],
    toolbar: [
      'bold', 'italic', 'heading', '|', 
      'unordered-list', 'ordered-list', '|',
      'link', 'image', '|',
      'preview', 'side-by-side', 'fullscreen', '|',
      'guide'
    ]
  };

  return (
    <div className="resume-editor">
      <h2>Edit Resume Content</h2>
      <p className="editor-info">
        Edit your resume content in markdown format. Use the toolbar for formatting options.
      </p>
      <SimpleMDE
        value={markdownContent}
        onChange={handleChange}
        options={editorOptions}
      />
    </div>
  );
};

export default ResumeEditor;