import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 60000, // 60 seconds timeout for long operations like image generation
});

// Resume API endpoints
export const resumeApi = {
  generateResume: (data) => api.post('/resume/generate', data),
  updateResume: (data) => api.post('/resume/update', data),
};

// Image API endpoints
export const imageApi = {
  uploadImage: (file, placeholderId) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('placeholder_id', placeholderId);
    
    return api.post('/image/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  searchImages: (query, placeholderId) => 
    api.post('/image/search', { query, placeholder_id: placeholderId }),
  generateImage: (prompt, placeholderId) => 
    api.post('/image/generate', { prompt, placeholder_id: placeholderId }),
};

// Export API endpoints
export const exportApi = {
  exportResume: (html, format, filename = 'resume') => 
    api.post('/export/convert', 
      { html_content: html, format, filename },
      { responseType: 'blob' }
    ),
};

const apiService = {
  resume: resumeApi,
  image: imageApi,
  export: exportApi,
};

export default apiService;