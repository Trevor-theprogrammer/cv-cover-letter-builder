import React, { useState } from 'react';

const EducationForm = ({ data, onChange, errors }) => {
  const [educations, setEducations] = useState(data || []);

  const addEducation = () => {
    const newEducation = {
      degree: '',
      institution: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      gpa: '',
      description: '',
    };
    const updatedEducations = [...educations, newEducation];
    setEducations(updatedEducations);
    onChange(updatedEducations);
  };

  const updateEducation = (index, field, value) => {
    const updatedEducations = educations.map((edu, i) =>
      i === index ? { ...edu, [field]: value } : edu
    );
    setEducations(updatedEducations);
    onChange(updatedEducations);
  };

  const removeEducation = (index) => {
    const updatedEducations = educations.filter((_, i) => i !== index);
    setEducations(updatedEducations);
    onChange(updatedEducations);
  };

  return (
    <div className="education-form">
      <h2>Education</h2>

      {educations.map((education, index) => (
        <div key={index} className="education-entry">
          <div className="entry-header">
            <h3>Education #{index + 1}</h3>
            <button
              type="button"
              className="btn btn-danger btn-sm"
              onClick={() => removeEducation(index)}
            >
              Remove
            </button>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Degree *</label>
              <input
                type="text"
                value={education.degree}
                onChange={(e) =>
                  updateEducation(index, 'degree', e.target.value)
                }
                placeholder="Bachelor of Science in Computer Science"
              />
            </div>
            <div className="form-group">
              <label>Institution *</label>
              <input
                type="text"
                value={education.institution}
                onChange={(e) =>
                  updateEducation(index, 'institution', e.target.value)
                }
                placeholder="University Name"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={education.location}
                onChange={(e) =>
                  updateEducation(index, 'location', e.target.value)
                }
                placeholder="City, Country"
              />
            </div>
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={education.start_date}
                onChange={(e) =>
                  updateEducation(index, 'start_date', e.target.value)
                }
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={education.end_date}
                onChange={(e) =>
                  updateEducation(index, 'end_date', e.target.value)
                }
                disabled={education.is_current}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={education.is_current}
                  onChange={(e) =>
                    updateEducation(index, 'is_current', e.target.checked)
                  }
                />
                Currently studying
              </label>
            </div>
            <div className="form-group">
              <label>GPA (Optional)</label>
              <input
                type="text"
                value={education.gpa}
                onChange={(e) => updateEducation(index, 'gpa', e.target.value)}
                placeholder="3.8/4.0"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Description (Optional)</label>
            <textarea
              value={education.description}
              onChange={(e) =>
                updateEducation(index, 'description', e.target.value)
              }
              placeholder="Relevant coursework, honors, activities..."
              rows="3"
            />
          </div>
        </div>
      ))}

      <button
        type="button"
        className="btn btn-secondary"
        onClick={addEducation}
      >
        Add Education
      </button>

      {errors.education && (
        <div className="error-message">{errors.education}</div>
      )}
    </div>
  );
};

export default EducationForm;
