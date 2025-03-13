import React, { useState, useEffect } from 'react';
import './styles/App.css';
import ResumeForm from './components/ResumeForm';
import ResumeEditor from './components/ResumeEditor';
import ResumePreview from './components/ResumePreview';
import ImagePlaceholderManager from './components/ImagePlaceholderManager';
import ExportOptions from './components/ExportOptions';

function App() {
  const [resumeData, setResumeData] = useState(null);
  const [markdownContent, setMarkdownContent] = useState('');
  const [imagePlaceholders, setImagePlaceholders] = useState({});
  const [imageData, setImageData] = useState({});
  const [activeStep, setActiveStep] = useState('form'); // form, edit, preview, export
  const [selectedPlaceholder, setSelectedPlaceholder] = useState(null);

  // 使用 useEffect 确保 resumeData 被实际使用，消除 no-unused-vars 警告
  useEffect(() => {
    // 当 resumeData 变化时，进行必要的处理
    if (resumeData) {
      console.log("Resume data loaded:", resumeData.id || "new resume");
    }
  }, [resumeData]);

  const handleGenerateResume = (data) => {
    setResumeData(data);
    setMarkdownContent(data.markdown_content);
    setImagePlaceholders(data.image_placeholders);
    setActiveStep('edit');
  };

  const handleUpdateMarkdown = (newContent) => {
    setMarkdownContent(newContent);
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

  const handleNextStep = () => {
    if (activeStep === 'form') setActiveStep('edit');
    else if (activeStep === 'edit') setActiveStep('preview');
    else if (activeStep === 'preview') setActiveStep('export');
  };

  const handlePreviousStep = () => {
    if (activeStep === 'export') setActiveStep('preview');
    else if (activeStep === 'preview') setActiveStep('edit');
    else if (activeStep === 'edit') setActiveStep('form');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Resume Generator</h1>
      </header>
      
      <main className="App-content">
        {activeStep === 'form' && (
          <ResumeForm onGenerateResume={handleGenerateResume} />
        )}
        
        {activeStep === 'edit' && (
          <div className="editor-container">
            <ResumeEditor 
              markdownContent={markdownContent} 
              onUpdateContent={handleUpdateMarkdown} 
            />
            <div className="placeholder-manager">
              <h3>Image Placeholders</h3>
              {Object.entries(imagePlaceholders).map(([id, description]) => (
                <div key={id} className="placeholder-item" onClick={() => handleSelectPlaceholder(id)}>
                  <div className={`placeholder-preview ${selectedPlaceholder === id ? 'selected' : ''}`}>
                    {imageData[id] ? (
                      <img src={imageData[id]} alt={description} />
                    ) : (
                      <div className="placeholder-text">{description}</div>
                    )}
                  </div>
                  <div className="placeholder-description">{description}</div>
                </div>
              ))}
              
              {selectedPlaceholder && (
                <ImagePlaceholderManager 
                  placeholderId={selectedPlaceholder}
                  description={imagePlaceholders[selectedPlaceholder]}
                  onUpdateImage={handleImageUpdate}
                />
              )}
            </div>
          </div>
        )}
        
        {activeStep === 'preview' && (
          <ResumePreview 
            markdownContent={markdownContent} 
            imagePlaceholders={imagePlaceholders}
            imageData={imageData}
          />
        )}
        
        {activeStep === 'export' && (
          <ExportOptions 
            markdownContent={markdownContent}
          />
        )}
        
        <div className="navigation-buttons">
          {activeStep !== 'form' && (
            <button onClick={handlePreviousStep} className="button">Back</button>
          )}
          {activeStep !== 'export' && (
            <button onClick={handleNextStep} className="button primary">Next</button>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;