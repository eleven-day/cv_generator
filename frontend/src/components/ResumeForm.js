import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ResumeForm.css';

const ResumeForm = ({ onGenerateResume }) => {
  const [formData, setFormData] = useState({
    name: '',
    position: '',
    experience: '',
    education: '',
    skills: '',
    contact: '',
    additionalInfo: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // Prepare data for API
      const apiData = {
        name: formData.name || 'Xiao Han',
        position: formData.position || 'Algorithm Engineer',
        additional_info: {}
      };

      // Add additional fields if they exist
      if (formData.experience) apiData.additional_info.experience = formData.experience;
      if (formData.education) apiData.additional_info.education = formData.education;
      if (formData.skills) apiData.additional_info.skills = formData.skills;
      if (formData.contact) apiData.additional_info.contact = formData.contact;
      if (formData.additionalInfo) apiData.additional_info.additional = formData.additionalInfo;

      const response = await axios.post('/api/resume/generate', apiData);
      onGenerateResume(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate resume');
      console.error('Error generating resume:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="resume-form-container">
      <h2>Enter Your Resume Information</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="resume-form">
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Xiao Han"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="position">Position:</label>
          <input
            type="text"
            id="position"
            name="position"
            value={formData.position}
            onChange={handleChange}
            placeholder="Algorithm Engineer"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="experience">Work Experience:</label>
          <textarea
            id="experience"
            name="experience"
            value={formData.experience}
            onChange={handleChange}
            placeholder="Enter your work experience"
            rows={4}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="education">Education:</label>
          <textarea
            id="education"
            name="education"
            value={formData.education}
            onChange={handleChange}
            placeholder="Enter your education background"
            rows={3}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="skills">Skills:</label>
          <textarea
            id="skills"
            name="skills"
            value={formData.skills}
            onChange={handleChange}
            placeholder="List your skills"
            rows={3}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="contact">Contact Information:</label>
          <textarea
            id="contact"
            name="contact"
            value={formData.contact}
            onChange={handleChange}
            placeholder="Email, phone, LinkedIn, etc."
            rows={2}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="additionalInfo">Additional Information:</label>
          <textarea
            id="additionalInfo"
            name="additionalInfo"
            value={formData.additionalInfo}
            onChange={handleChange}
            placeholder="Any other information you'd like to include"
            rows={3}
          />
        </div>
        
        <button type="submit" className="button primary" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Resume'}
        </button>
      </form>
    </div>
  );
};

export default ResumeForm;