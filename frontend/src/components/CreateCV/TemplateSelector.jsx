import React, { useState } from 'react';

const TemplateSelector = ({ templates, selectedTemplate, onSelect }) => {
  const [previewTemplate, setPreviewTemplate] = useState(null);

  const handleTemplateClick = (template) => {
    onSelect(template);
  };

  const handlePreview = (template) => {
    setPreviewTemplate(template);
  };

  return (
    <div className="template-selector">
      <h2>Choose a Template</h2>
      <p>Select a template that best fits your style and industry</p>

      <div className="templates-grid">
        {templates.map((template) => (
          <div
            key={template.id}
            className={`template-card ${
              selectedTemplate?.id === template.id ? 'selected' : ''
            }`}
            onClick={() => handleTemplateClick(template)}
          >
            <div className="template-preview">
              {template.preview_image ? (
                <img
                  src={template.preview_image}
                  alt={template.name}
                  className="template-image"
                />
              ) : (
                <div className="template-placeholder">
                  <span>{template.name}</span>
                </div>
              )}
            </div>

            <div className="template-info">
              <h3>{template.name}</h3>
              <p>{template.description}</p>
              <div className="template-tags">
                <span className={`tag ${template.style}`}>
                  {template.style}
                </span>
                <span className="tag">{template.type}</span>
              </div>
            </div>

            <div className="template-actions">
              <button
                className="btn btn-outline"
                onClick={(e) => {
                  e.stopPropagation();
                  handlePreview(template);
                }}
              >
                Preview
              </button>
              <button
                className={`btn ${
                  selectedTemplate?.id === template.id
                    ? 'btn-success'
                    : 'btn-primary'
                }`}
                onClick={() => handleTemplateClick(template)}
              >
                {selectedTemplate?.id === template.id ? 'Selected' : 'Select'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {templates.length === 0 && (
        <div className="no-templates">
          <p>No templates available. Please contact support.</p>
        </div>
      )}

      {previewTemplate && (
        <div className="template-preview-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{previewTemplate.name} Preview</h3>
              <button
                className="close-btn"
                onClick={() => setPreviewTemplate(null)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <img
                src={previewTemplate.preview_image}
                alt={previewTemplate.name}
                className="preview-image"
              />
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-secondary"
                onClick={() => setPreviewTemplate(null)}
              >
                Close
              </button>
              <button
                className="btn btn-primary"
                onClick={() => {
                  handleTemplateClick(previewTemplate);
                  setPreviewTemplate(null);
                }}
              >
                Select This Template
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TemplateSelector;
