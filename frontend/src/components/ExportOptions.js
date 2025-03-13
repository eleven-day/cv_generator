import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ExportOptions.css';

const ExportOptions = ({ markdownContent }) => {
  const [exportFormat, setExportFormat] = useState('pdf');
  const [filename, setFilename] = useState('resume');
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState(null);

  const handleExport = async () => {
    setIsExporting(true);
    setError(null);
    
    try {
      const response = await axios.post(
        '/api/export/convert',
        {
          markdown_content: markdownContent,
          format: exportFormat,
          filename: filename
        },
        {
          responseType: 'blob'
        }
      );
      
      // Create a download link for the file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${filename}.${exportFormat}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to export resume. Please try again.');
      console.error('Error exporting resume:', err);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="export-options">
      <h2>Export Your Resume</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="export-form">
        <div className="form-group">
          <label htmlFor="filename">Filename:</label>
          <input
            type="text"
            id="filename"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            placeholder="resume"
          />
        </div>
        
        <div className="form-group">
          <label>Export Format:</label>
          <div className="format-options">
            <label className="format-option">
              <input
                type="radio"
                name="format"
                value="pdf"
                checked={exportFormat === 'pdf'}
                onChange={() => setExportFormat('pdf')}
              />
              <span className="format-label">PDF</span>
            </label>
            
            <label className="format-option">
              <input
                type="radio"
                name="format"
                value="docx"
                checked={exportFormat === 'docx'}
                onChange={() => setExportFormat('docx')}
              />
              <span className="format-label">DOCX</span>
            </label>
            
            <label className="format-option">
              <input
                type="radio"
                name="format"
                value="pptx"
                checked={exportFormat === 'pptx'}
                onChange={() => setExportFormat('pptx')}
              />
              <span className="format-label">PPTX</span>
            </label>
            
            <label className="format-option">
              <input
                type="radio"
                name="format"
                value="md"
                checked={exportFormat === 'md'}
                onChange={() => setExportFormat('md')}
              />
              <span className="format-label">Markdown</span>
            </label>
            
            <label className="format-option">
              <input
                type="radio"
                name="format"
                value="html"
                checked={exportFormat === 'html'}
                onChange={() => setExportFormat('html')}
              />
              <span className="format-label">HTML</span>
            </label>
          </div>
        </div>
        
        <button 
          className="button primary" 
          onClick={handleExport}
          disabled={isExporting}
        >
          {isExporting ? 'Exporting...' : `Export as ${exportFormat.toUpperCase()}`}
        </button>
      </div>
    </div>
  );
};

export default ExportOptions;