import React, { useState } from 'react';
import { exportApi } from '../services/api';
import '../styles/ExportOptions.css';

const ExportOptions = ({ htmlContent }) => {
  const [filename, setFilename] = useState('resume');
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState(null);

  const handleExport = async () => {
    if (!htmlContent) {
      setError('No resume content to export. Please generate a resume first.');
      return;
    }
    
    setIsExporting(true);
    setError(null);
    
    try {
      const response = await exportApi.exportResume(
        htmlContent,
        'pdf',
        filename
      );
      
      // Create a download link for the file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${filename}.pdf`);
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
      <h3>Export Your Resume</h3>
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
        
        <button 
          className="button primary export-button" 
          onClick={handleExport}
          disabled={isExporting}
        >
          {isExporting ? 'Exporting...' : 'Export as PDF'}
        </button>
      </div>
    </div>
  );
};

export default ExportOptions;