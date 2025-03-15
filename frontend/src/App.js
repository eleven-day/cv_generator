import React, { useState } from 'react';
import './styles/App.css';
import ResumeForm from './components/ResumeForm';
import ResumeEditor from './components/ResumeEditor';
import ResumePreview from './components/ResumePreview';
import ImagePlaceholderManager from './components/ImagePlaceholderManager';
import ExportOptions from './components/ExportOptions';

function App() {
  const [resumeData, setResumeData] = useState(null);
  const [htmlContent, setHtmlContent] = useState('');
  const [imagePlaceholders, setImagePlaceholders] = useState({});
  const [imageData, setImageData] = useState({});
  const [selectedPlaceholder, setSelectedPlaceholder] = useState(null);
  const [viewMode, setViewMode] = useState('preview'); // 'code' or 'preview'

  const handleGenerateResume = (data) => {
    setResumeData(data);
    setHtmlContent(data.html_content);
    setImagePlaceholders(data.image_placeholders);
  };

  const handleUpdateHtml = (newContent) => {
    setHtmlContent(newContent);
  };

  const handleImageUpdate = (placeholderId, imageDataUrl) => {
    setImageData({
      ...imageData,
      [placeholderId]: imageDataUrl
    });
  };

  const handleSelectPlaceholder = (placeholderId) => {
    setSelectedPlaceholder(placeholderId);
  };

  const toggleViewMode = () => {
    setViewMode(viewMode === 'preview' ? 'code' : 'preview');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Resume Generator</h1>
      </header>
      
      <main className="single-page-layout">
        <div className="left-panel">
          <ResumeForm onGenerateResume={handleGenerateResume} />
        </div>
        
        <div className="right-panel">
          <div className="view-controls">
            <button 
              className={`view-button ${viewMode === 'code' ? 'active' : ''}`} 
              onClick={toggleViewMode}
            >
              HTML Code
            </button>
            <button 
              className={`view-button ${viewMode === 'preview' ? 'active' : ''}`} 
              onClick={toggleViewMode}
            >
              Preview
            </button>
          </div>
          
          <div className="resume-display">
            {viewMode === 'code' ? (
              <ResumeEditor 
                htmlContent={htmlContent} 
                onUpdateContent={handleUpdateHtml} 
              />
            ) : (
              <ResumePreview 
                htmlContent={htmlContent} 
                imagePlaceholders={imagePlaceholders}
                imageData={imageData}
              />
            )}
          </div>
          
          <div className="bottom-controls">
            <div className="placeholders-section">
              <h3>Image Placeholders</h3>
              <div className="placeholders-list">
                {Object.entries(imagePlaceholders).map(([id, description]) => (
                  <div 
                    key={id} 
                    className={`placeholder-item ${selectedPlaceholder === id ? 'selected' : ''}`} 
                    onClick={() => handleSelectPlaceholder(id)}
                  >
                    <div className="placeholder-preview">
                      {imageData[id] ? (
                        <img src={imageData[id]} alt={description} />
                      ) : (
                        <div className="placeholder-text">{description}</div>
                      )}
                    </div>
                    <div className="placeholder-description">{description}</div>
                  </div>
                ))}
              </div>
              
              {selectedPlaceholder && (
                <ImagePlaceholderManager 
                  placeholderId={selectedPlaceholder}
                  description={imagePlaceholders[selectedPlaceholder]}
                  onUpdateImage={handleImageUpdate}
                />
              )}
            </div>
            
            <div className="export-section">
              <ExportOptions htmlContent={htmlContent} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;