import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const ProjectsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const ProjectCard = styled.div`
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;

  &.primary {
    background: #667eea;
    color: white;

    &:hover {
      background: #5a6fd8;
    }
  }

  &.secondary {
    background: #e9ecef;
    color: #495057;

    &:hover {
      background: #dee2e6;
    }
  }

  &.danger {
    background: #dc3545;
    color: white;

    &:hover {
      background: #c82333;
    }
  }
`;

const AddButton = styled(Button)`
  margin: 1rem 0;
  padding: 0.75rem 1.5rem;
`;

const TechStack = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
`;

const TechTag = styled.div`
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
`;

const Projects = ({ data, updateData }) => {
  const [projects, setProjects] = useState(data.projects || []);

  const addProject = () => {
    const newProject = {
      id: Date.now(),
      name: '',
      description: '',
      technologies: [],
      url: '',
      github: '',
      startDate: '',
      endDate: '',
      current: false,
      role: '',
      achievements: '',
    };

    const updated = [...projects, newProject];
    setProjects(updated);
    updateData({ ...data, projects: updated });
  };

  const updateProject = (id, field, value) => {
    const updated = projects.map((project) =>
      project.id === id ? { ...project, [field]: value } : project
    );
    setProjects(updated);
    updateData({ ...data, projects: updated });
  };

  const removeProject = (id) => {
    const updated = projects.filter((project) => project.id !== id);
    setProjects(updated);
    updateData({ ...data, projects: updated });
  };

  const handleTechChange = (id, techString) => {
    const technologies = techString
      .split(',')
      .map((tech) => tech.trim())
      .filter((tech) => tech);
    updateProject(id, 'technologies', technologies);
  };

  return (
    <Container>
      <h2>Projects</h2>
      <p>Showcase your best projects to demonstrate your technical abilities</p>

      <ProjectsList>
        {projects.map((project, index) => (
          <ProjectCard key={project.id}>
            <h3>Project {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Project Name *</Label>
                <Input
                  type="text"
                  value={project.name}
                  onChange={(e) =>
                    updateProject(project.id, 'name', e.target.value)
                  }
                  placeholder="E-commerce Platform"
                />
              </FormGroup>

              <FormGroup>
                <Label>Your Role *</Label>
                <Input
                  type="text"
                  value={project.role}
                  onChange={(e) =>
                    updateProject(project.id, 'role', e.target.value)
                  }
                  placeholder="Full Stack Developer"
                />
              </FormGroup>

              <FormGroup>
                <Label>Project URL</Label>
                <Input
                  type="url"
                  value={project.url}
                  onChange={(e) =>
                    updateProject(project.id, 'url', e.target.value)
                  }
                  placeholder="https://myproject.com"
                />
              </FormGroup>

              <FormGroup>
                <Label>GitHub Repository</Label>
                <Input
                  type="url"
                  value={project.github}
                  onChange={(e) =>
                    updateProject(project.id, 'github', e.target.value)
                  }
                  placeholder="https://github.com/username/project"
                />
              </FormGroup>

              <FormGroup>
                <Label>Start Date *</Label>
                <Input
                  type="month"
                  value={project.startDate}
                  onChange={(e) =>
                    updateProject(project.id, 'startDate', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>End Date</Label>
                <Input
                  type="month"
                  value={project.endDate}
                  onChange={(e) =>
                    updateProject(project.id, 'endDate', e.target.value)
                  }
                  disabled={project.current}
                />
              </FormGroup>
            </Grid>

            <FormGroup>
              <Label>
                <input
                  type="checkbox"
                  checked={project.current}
                  onChange={(e) =>
                    updateProject(project.id, 'current', e.target.checked)
                  }
                />
                This project is ongoing
              </Label>
            </FormGroup>

            <FormGroup>
              <Label>Technologies Used (comma-separated)</Label>
              <Input
                type="text"
                value={project.technologies.join(', ')}
                onChange={(e) => handleTechChange(project.id, e.target.value)}
                placeholder="React, Node.js, MongoDB, Express"
              />
              <TechStack>
                {project.technologies.map((tech) => (
                  <TechTag key={tech}>{tech}</TechTag>
                ))}
              </TechStack>
            </FormGroup>

            <FormGroup>
              <Label>Project Description *</Label>
              <TextArea
                value={project.description}
                onChange={(e) =>
                  updateProject(project.id, 'description', e.target.value)
                }
                placeholder="Brief overview of the project, its purpose, and key features..."
              />
            </FormGroup>

            <FormGroup>
              <Label>Key Achievements</Label>
              <TextArea
                value={project.achievements}
                onChange={(e) =>
                  updateProject(project.id, 'achievements', e.target.value)
                }
                placeholder="Quantifiable achievements, metrics, or notable accomplishments..."
              />
            </FormGroup>

            <ButtonGroup>
              <Button
                className="danger"
                onClick={() => removeProject(project.id)}
              >
                Remove Project
              </Button>
            </ButtonGroup>
          </ProjectCard>
        ))}
      </ProjectsList>

      <AddButton className="primary" onClick={addProject}>
        + Add Project
      </AddButton>

      {projects.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>
            No projects added yet. Click "Add Project" to showcase your work.
          </p>
        </div>
      )}
    </Container>
  );
};

export default Projects;
