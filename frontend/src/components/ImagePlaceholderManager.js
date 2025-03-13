import React, { useState } from 'react';
import { imageApi } from '../services/api';
import '../styles/ImagePlaceholderManager.css';

const ImagePlaceholderManager = ({ placeholderId, description, onUpdateImage }) => {
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState(description || '');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [generatePrompt, setGeneratePrompt] = useState(description || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setUploadedFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!uploadedFile) return;
    
    setIsUploading(true);
    setError(null);
    
    try {
      const response = await imageApi.uploadImage(uploadedFile, placeholderId);
      onUpdateImage(placeholderId, response.data.image_data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload image');
      console.error('Error uploading image:', err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    setError(null);
    
    try {
      const response = await imageApi.searchImages(searchQuery, placeholderId);
      setSearchResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to search for images');
      console.error('Error searching for images:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectSearchResult = (imageData) => {
    onUpdateImage(placeholderId, imageData);
  };

  const handleGenerate = async () => {
    if (!generatePrompt.trim()) return;
    
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await imageApi.generateImage(generatePrompt, placeholderId);
      onUpdateImage(placeholderId, response.data.image_data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate image');
      console.error('Error generating image:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="image-placeholder-manager">
      <h3>Manage Image: {description}</h3>
      {error && <div className="error-message">{error}</div>}
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          Upload
        </button>
        <button 
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          Search
        </button>
        <button 
          className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => setActiveTab('generate')}
        >
          Generate
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'upload' && (
          <div className="upload-tab">
            <div className="file-input">
              <input 
                type="file" 
                id="image-upload" 
                accept="image/*" 
                onChange={handleFileChange}
              />
              <label htmlFor="image-upload" className="file-label">
                Choose Image
              </label>
              {uploadedFile && <span className="file-name">{uploadedFile.name}</span>}
            </div>
            
            <button 
              className="button" 
              onClick={handleFileUpload}
              disabled={!uploadedFile || isUploading}
            >
              {isUploading ? 'Uploading...' : 'Upload Image'}
            </button>
          </div>
        )}
        
        {activeTab === 'search' && (
          <div className="search-tab">
            <div className="search-input">
              <input 
                type="text" 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for images"
              />
              <button 
                onClick={handleSearch}
                disabled={isSearching}
              >
                {isSearching ? 'Searching...' : 'Search'}
              </button>
            </div>
            
            <div className="search-results">
              {searchResults.map((result, index) => (
                <div 
                  key={index} 
                  className="search-result"
                  onClick={() => handleSelectSearchResult(result.image_data)}
                >
                  <img src={result.image_data} alt={`Search result ${index + 1}`} />
                </div>
              ))}
              
              {searchResults.length === 0 && !isSearching && (
                <p className="no-results">No images found. Try a different search term.</p>
              )}
              
              {isSearching && (
                <p className="loading">Searching for images...</p>
              )}
            </div>
          </div>
        )}
        
        {activeTab === 'generate' && (
          <div className="generate-tab">
            <div className="generate-input">
              <textarea 
                value={generatePrompt} 
                onChange={(e) => setGeneratePrompt(e.target.value)}
                placeholder="Describe the image you want to generate"
                rows={4}
              />
              <button 
                onClick={handleGenerate}
                disabled={isGenerating}
              >
                {isGenerating ? 'Generating...' : 'Generate Image'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImagePlaceholderManager;