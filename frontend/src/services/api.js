import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
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
  exportResume: (markdown, format, filename = 'resume') => 
    api.post('/export/convert', 
      { markdown_content: markdown, format, filename },
      { responseType: 'blob' }
    ),
};

export default {
  resume: resumeApi,
  image: imageApi,
  export: exportApi,
};