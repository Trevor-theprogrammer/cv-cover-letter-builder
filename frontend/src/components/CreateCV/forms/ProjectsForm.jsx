import React, { useState } from 'react';

const ProjectsForm = ({ data, onChange, errors }) => {
  const [projects, setProjects] = useState(data || []);

  const addProject = () => {
    const newProject = {
      name: '',
      description: '',
      technologies: [],
      url: '',
      start_date: '',
      end_date: '',
      is_current: false,
    };
    const updatedProjects = [...projects, newProject];
    setProjects(updatedProjects);
    onChange(updatedProjects);
  };

  const updateProject = (index, field, value) => {
    const updatedProjects = projects.map((project, i) =>
      i === index ? { ...project, [field]: value } : project
    );
    setProjects(updatedProjects);
    onChange(updatedProjects);
  };

  const updateTechnologies = (index, techString) => {
    const technologies = techString
      .split(',')
      .map((tech) => tech.trim())
      .filter((tech) => tech);
    updateProject(index, 'technologies', technologies);
  };

  const removeProject = (index) => {
    const updatedProjects = projects.filter((_, i) => i !== index);
    setProjects(updatedProjects);
    onChange(updatedProjects);
  };

  return (
    <div className="projects-form">
      <h2>Projects</h2>

      {projects.map((project, index) => (
        <div key={index} className="project-entry">
          <div className="entry-header">
            <h3>Project #{index + 1}</h3>
            <button
              type="button"
              className="btn btn-danger btn-sm"
              onClick={() => removeProject(index)}
            >
              Remove
            </button>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Project Name *</label>
              <input
                type="text"
                value={project.name}
                onChange={(e) => updateProject(index, 'name', e.target.value)}
                placeholder="E-commerce Website"
              />
            </div>
            <div className="form-group">
              <label>Project URL</label>
              <input
                type="url"
                value={project.url}
                onChange={(e) => updateProject(index, 'url', e.target.value)}
                placeholder="https://github.com/username/project"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Technologies Used</label>
            <input
              type="text"
              value={project.technologies.join(', ')}
              onChange={(e) => updateTechnologies(index, e.target.value)}
              placeholder="React, Node.js, MongoDB, Express"
            />
            <small className="form-text">
              Separate technologies with commas
            </small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={project.start_date}
                onChange={(e) =>
                  updateProject(index, 'start_date', e.target.value)
                }
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={project.end_date}
                onChange={(e) =>
                  updateProject(index, 'end_date', e.target.value)
                }
                disabled={project.is_current}
              />
            </div>
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={project.is_current}
                onChange={(e) =>
                  updateProject(index, 'is_current', e.target.checked)
                }
              />
              Currently working on this project
            </label>
          </div>

          <div className="form-group">
            <label>Project Description *</label>
            <textarea
              value={project.description}
              onChange={(e) =>
                updateProject(index, 'description', e.target.value)
              }
              placeholder="Describe the project, your role, and key achievements..."
              rows="4"
            />
          </div>
        </div>
      ))}

      <button type="button" className="btn btn-secondary" onClick={addProject}>
        Add Project
      </button>

      {errors.projects && (
        <div className="error-message">{errors.projects}</div>
      )}
    </div>
  );
};

export default ProjectsForm;
