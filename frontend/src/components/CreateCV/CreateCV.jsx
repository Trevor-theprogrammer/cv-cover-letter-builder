import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import PersonalInfoForm from './forms/PersonalInfoForm';
import ExperienceForm from './forms/ExperienceForm';
import EducationForm from './forms/EducationForm';
import ProjectsForm from './forms/ProjectsForm';
import TemplateSelector from './TemplateSelector';
import CVPreview from './CVPreview';
import ProgressIndicator from './ProgressIndicator';
import './CreateCV.css';

const CreateCV = () => {
  const [cvData, setCvData] = useState({
    full_name: '',
    email: '',
    phone: '',
    location: '',
    summary: '',
    template: null,
    sections: {
      experience: [],
      education: [],
      projects: [],
    },
  });

  const [templates, setTemplates] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  const [cvId, setCvId] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    fetchTemplates();
    createDraftCV();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('/api/enhanced-templates/');
      setTemplates(response.data);
    } catch (error) {
      toast.error('Failed to load templates');
    }
  };

  const createDraftCV = async () => {
    try {
      const response = await axios.post('/api/enhanced-cvs/create_draft/', {
        title: 'Untitled CV',
        is_draft: true,
      });
      setCvId(response.data.id);
    } catch (error) {
      toast.error('Failed to create CV draft');
    }
  };

  const autoSave = async (data) => {
    if (!cvId) return;

    setIsSaving(true);
    try {
      await axios.patch(`/api/enhanced-cvs/${cvId}/auto_save/`, data);
    } catch (error) {
      console.error('Auto-save failed:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handlePersonalInfoChange = (data) => {
    const newData = { ...cvData, ...data };
    setCvData(newData);
    autoSave(newData);
  };

  const handleSectionChange = (sectionType, data) => {
    const newData = {
      ...cvData,
      sections: {
        ...cvData.sections,
        [sectionType]: data,
      },
    };
    setCvData(newData);
    autoSave(newData);
  };

  const handleTemplateSelect = (template) => {
    const newData = { ...cvData, template };
    setCvData(newData);
    autoSave(newData);
  };

  const validateStep = async () => {
    if (!cvId) return false;

    try {
      const response = await axios.post(
        `/api/enhanced-cvs/${cvId}/validate_data/`
      );
      setValidationErrors(response.data.errors || {});
      return response.data.is_valid;
    } catch (error) {
      toast.error('Validation failed');
      return false;
    }
  };

  const nextStep = async () => {
    const isValid = await validateStep();
    if (isValid && currentStep < 5) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const generateCV = async () => {
    const isValid = await validateStep();
    if (!isValid) {
      toast.error('Please fix validation errors before generating CV');
      return;
    }

    try {
      const response = await axios.get(`/api/enhanced-cvs/${cvId}/export_pdf/`);
      // Handle PDF download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${cvData.full_name}_CV.pdf`;
      a.click();
      toast.success('CV generated successfully!');
    } catch (error) {
      toast.error('Failed to generate CV');
    }
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <PersonalInfoForm
            data={cvData}
            onChange={handlePersonalInfoChange}
            errors={validationErrors}
          />
        );
      case 2:
        return (
          <ExperienceForm
            data={cvData.sections.experience}
            onChange={(data) => handleSectionChange('experience', data)}
            errors={validationErrors}
          />
        );
      case 3:
        return (
          <EducationForm
            data={cvData.sections.education}
            onChange={(data) => handleSectionChange('education', data)}
            errors={validationErrors}
          />
        );
      case 4:
        return (
          <ProjectsForm
            data={cvData.sections.projects}
            onChange={(data) => handleSectionChange('projects', data)}
            errors={validationErrors}
          />
        );
      case 5:
        return (
          <TemplateSelector
            templates={templates}
            selectedTemplate={cvData.template}
            onSelect={handleTemplateSelect}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="create-cv-container">
      <div className="create-cv-header">
        <h1>Create Your CV</h1>
        <ProgressIndicator currentStep={currentStep} totalSteps={5} />
        {isSaving && <div className="auto-save-indicator">Saving...</div>}
      </div>

      <div className="create-cv-content">
        <div className="form-section">
          {renderCurrentStep()}

          <div className="navigation-buttons">
            {currentStep > 1 && (
              <button className="btn btn-secondary" onClick={prevStep}>
                Previous
              </button>
            )}

            {currentStep < 5 ? (
              <button className="btn btn-primary" onClick={nextStep}>
                Next
              </button>
            ) : (
              <button className="btn btn-success" onClick={generateCV}>
                Generate CV
              </button>
            )}
          </div>
        </div>

        <div className="preview-section">
          <CVPreview cvId={cvId} cvData={cvData} />
        </div>
      </div>
    </div>
  );
};

export default CreateCV;
