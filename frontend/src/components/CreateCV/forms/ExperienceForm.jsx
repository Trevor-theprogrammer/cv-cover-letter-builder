import React, { useState } from 'react';

const ExperienceForm = ({ data, onChange, errors }) => {
  const [experiences, setExperiences] = useState(data || []);

  const addExperience = () => {
    const newExperience = {
      job_title: '',
      company: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      achievements: [],
    };
    const updatedExperiences = [...experiences, newExperience];
    setExperiences(updatedExperiences);
    onChange(updatedExperiences);
  };

  const updateExperience = (index, field, value) => {
    const updatedExperiences = experiences.map((exp, i) =>
      i === index ? { ...exp, [field]: value } : exp
    );
    setExperiences(updatedExperiences);
    onChange(updatedExperiences);
  };

  const removeExperience = (index) => {
    const updatedExperiences = experiences.filter((_, i) => i !== index);
    setExperiences(updatedExperiences);
    onChange(updatedExperiences);
  };

  return (
    <div className="experience-form">
      <h2>Work Experience</h2>

      {experiences.map((experience, index) => (
        <div key={index} className="experience-entry">
          <div className="entry-header">
            <h3>Experience #{index + 1}</h3>
            <button
              type="button"
              className="btn btn-danger btn-sm"
              onClick={() => removeExperience(index)}
            >
              Remove
            </button>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Job Title *</label>
              <input
                type="text"
                value={experience.job_title}
                onChange={(e) =>
                  updateExperience(index, 'job_title', e.target.value)
                }
                placeholder="Software Engineer"
              />
            </div>
            <div className="form-group">
              <label>Company *</label>
              <input
                type="text"
                value={experience.company}
                onChange={(e) =>
                  updateExperience(index, 'company', e.target.value)
                }
                placeholder="Company Name"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={experience.location}
                onChange={(e) =>
                  updateExperience(index, 'location', e.target.value)
                }
                placeholder="City, Country"
              />
            </div>
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={experience.start_date}
                onChange={(e) =>
                  updateExperience(index, 'start_date', e.target.value)
                }
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={experience.end_date}
                onChange={(e) =>
                  updateExperience(index, 'end_date', e.target.value)
                }
                disabled={experience.is_current}
              />
            </div>
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={experience.is_current}
                onChange={(e) =>
                  updateExperience(index, 'is_current', e.target.checked)
                }
              />
              Currently working here
            </label>
          </div>

          <div className="form-group">
            <label>Job Description</label>
            <textarea
              value={experience.description}
              onChange={(e) =>
                updateExperience(index, 'description', e.target.value)
              }
              placeholder="Describe your responsibilities and achievements..."
              rows="4"
            />
          </div>
        </div>
      ))}

      <button
        type="button"
        className="btn btn-secondary"
        onClick={addExperience}
      >
        Add Experience
      </button>

      {errors.experience && (
        <div className="error-message">{errors.experience}</div>
      )}
    </div>
  );
};

export default ExperienceForm;
