import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const ExperienceList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const ExperienceCard = styled.div`
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

const Experience = ({ data, updateData }) => {
  const [experiences, setExperiences] = useState(data.experience || []);

  const addExperience = () => {
    const newExperience = {
      id: Date.now(),
      company: '',
      position: '',
      startDate: '',
      endDate: '',
      current: false,
      description: '',
      achievements: '',
    };

    const updated = [...experiences, newExperience];
    setExperiences(updated);
    updateData({ ...data, experience: updated });
  };

  const updateExperience = (id, field, value) => {
    const updated = experiences.map((exp) =>
      exp.id === id ? { ...exp, [field]: value } : exp
    );
    setExperiences(updated);
    updateData({ ...data, experience: updated });
  };

  const removeExperience = (id) => {
    const updated = experiences.filter((exp) => exp.id !== id);
    setExperiences(updated);
    updateData({ ...data, experience: updated });
  };

  return (
    <Container>
      <h2>Work Experience</h2>
      <p>Add your professional experience to showcase your career journey</p>

      <ExperienceList>
        {experiences.map((exp, index) => (
          <ExperienceCard key={exp.id}>
            <h3>Experience {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Company Name *</Label>
                <Input
                  type="text"
                  value={exp.company}
                  onChange={(e) =>
                    updateExperience(exp.id, 'company', e.target.value)
                  }
                  placeholder="Tech Corp Inc."
                />
              </FormGroup>

              <FormGroup>
                <Label>Position *</Label>
                <Input
                  type="text"
                  value={exp.position}
                  onChange={(e) =>
                    updateExperience(exp.id, 'position', e.target.value)
                  }
                  placeholder="Senior Software Engineer"
                />
              </FormGroup>

              <FormGroup>
                <Label>Start Date *</Label>
                <Input
                  type="month"
                  value={exp.startDate}
                  onChange={(e) =>
                    updateExperience(exp.id, 'startDate', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>End Date</Label>
                <Input
                  type="month"
                  value={exp.endDate}
                  onChange={(e) =>
                    updateExperience(exp.id, 'endDate', e.target.value)
                  }
                  disabled={exp.current}
                />
              </FormGroup>
            </Grid>

            <FormGroup>
              <Label>
                <input
                  type="checkbox"
                  checked={exp.current}
                  onChange={(e) =>
                    updateExperience(exp.id, 'current', e.target.checked)
                  }
                />
                I currently work here
              </Label>
            </FormGroup>

            <FormGroup>
              <Label>Job Description</Label>
              <TextArea
                value={exp.description}
                onChange={(e) =>
                  updateExperience(exp.id, 'description', e.target.value)
                }
                placeholder="Describe your role and responsibilities..."
              />
            </FormGroup>

            <FormGroup>
              <Label>Key Achievements</Label>
              <TextArea
                value={exp.achievements}
                onChange={(e) =>
                  updateExperience(exp.id, 'achievements', e.target.value)
                }
                placeholder="List your key achievements and accomplishments..."
              />
            </FormGroup>

            <ButtonGroup>
              <Button
                className="danger"
                onClick={() => removeExperience(exp.id)}
              >
                Remove
              </Button>
            </ButtonGroup>
          </ExperienceCard>
        ))}
      </ExperienceList>

      <AddButton className="primary" onClick={addExperience}>
        + Add Experience
      </AddButton>

      {experiences.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>
            No work experience added yet. Click "Add Experience" to get started.
          </p>
        </div>
      )}
    </Container>
  );
};

export default Experience;
