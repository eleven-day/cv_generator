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
      {
        name: 'bold',
        action: SimpleMDE.toggleBold,
        className: 'fa fa-bold',
        title: 'Bold',
      },
      {
        name: 'italic',
        action: SimpleMDE.toggleItalic,
        className: 'fa fa-italic',
        title: 'Italic',
      },
      {
        name: 'heading',
        action: SimpleMDE.toggleHeadingSmaller,
        className: 'fa fa-header',
        title: 'Heading',
      },
      '|',
      {
        name: 'unordered-list',
        action: SimpleMDE.toggleUnorderedList,
        className: 'fa fa-list-ul',
        title: 'Unordered List',
      },
      {
        name: 'ordered-list',
        action: SimpleMDE.toggleOrderedList,
        className: 'fa fa-list-ol',
        title: 'Ordered List',
      },
      '|',
      {
        name: 'link',
        action: SimpleMDE.drawLink,
        className: 'fa fa-link',
        title: 'Link',
      },
      {
        name: 'image',
        action: SimpleMDE.drawImage,
        className: 'fa fa-picture-o',
        title: 'Image',
      },
      '|',
      {
        name: 'preview',
        action: SimpleMDE.togglePreview,
        className: 'fa fa-eye',
        title: 'Preview',
      },
      {
        name: 'side-by-side',
        action: SimpleMDE.toggleSideBySide,
        className: 'fa fa-columns',
        title: 'Side by Side',
      },
      {
        name: 'fullscreen',
        action: SimpleMDE.toggleFullScreen,
        className: 'fa fa-arrows-alt',
        title: 'Fullscreen',
      },
      '|',
      {
        name: 'guide',
        action: 'https://www.markdownguide.org/basic-syntax/',
        className: 'fa fa-question-circle',
        title: 'Markdown Guide',
      }
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