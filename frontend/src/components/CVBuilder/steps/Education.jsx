import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const EducationList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const EducationCard = styled.div`
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

const Select = styled.select`
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
  min-height: 80px;
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

const Education = ({ data, updateData }) => {
  const [education, setEducation] = useState(data.education || []);

  const addEducation = () => {
    const newEducation = {
      id: Date.now(),
      institution: '',
      degree: '',
      fieldOfStudy: '',
      startDate: '',
      endDate: '',
      current: false,
      gpa: '',
      description: '',
    };

    const updated = [...education, newEducation];
    setEducation(updated);
    updateData({ ...data, education: updated });
  };

  const updateEducation = (id, field, value) => {
    const updated = education.map((edu) =>
      edu.id === id ? { ...edu, [field]: value } : edu
    );
    setEducation(updated);
    updateData({ ...data, education: updated });
  };

  const removeEducation = (id) => {
    const updated = education.filter((edu) => edu.id !== id);
    setEducation(updated);
    updateData({ ...data, education: updated });
  };

  const degreeOptions = [
    'High School',
    'Associate',
    'Bachelor',
    'Master',
    'Doctorate',
    'Professional Certificate',
    'Other',
  ];

  return (
    <Container>
      <h2>Education</h2>
      <p>Add your educational background to showcase your qualifications</p>

      <EducationList>
        {education.map((edu, index) => (
          <EducationCard key={edu.id}>
            <h3>Education {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Institution Name *</Label>
                <Input
                  type="text"
                  value={edu.institution}
                  onChange={(e) =>
                    updateEducation(edu.id, 'institution', e.target.value)
                  }
                  placeholder="Stanford University"
                />
              </FormGroup>

              <FormGroup>
                <Label>Degree Type *</Label>
                <Select
                  value={edu.degree}
                  onChange={(e) =>
                    updateEducation(edu.id, 'degree', e.target.value)
                  }
                >
                  <option value="">Select degree</option>
                  {degreeOptions.map((degree) => (
                    <option key={degree} value={degree}>
                      {degree}
                    </option>
                  ))}
                </Select>
              </FormGroup>

              <FormGroup>
                <Label>Field of Study *</Label>
                <Input
                  type="text"
                  value={edu.fieldOfStudy}
                  onChange={(e) =>
                    updateEducation(edu.id, 'fieldOfStudy', e.target.value)
                  }
                  placeholder="Computer Science"
                />
              </FormGroup>

              <FormGroup>
                <Label>GPA (Optional)</Label>
                <Input
                  type="text"
                  value={edu.gpa}
                  onChange={(e) =>
                    updateEducation(edu.id, 'gpa', e.target.value)
                  }
                  placeholder="3.8/4.0"
                />
              </FormGroup>

              <FormGroup>
                <Label>Start Date *</Label>
                <Input
                  type="month"
                  value={edu.startDate}
                  onChange={(e) =>
                    updateEducation(edu.id, 'startDate', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>End Date</Label>
                <Input
                  type="month"
                  value={edu.endDate}
                  onChange={(e) =>
                    updateEducation(edu.id, 'endDate', e.target.value)
                  }
                  disabled={edu.current}
                />
              </FormGroup>
            </Grid>

            <FormGroup>
              <Label>
                <input
                  type="checkbox"
                  checked={edu.current}
                  onChange={(e) =>
                    updateEducation(edu.id, 'current', e.target.checked)
                  }
                />
                I currently attend this institution
              </Label>
            </FormGroup>

            <FormGroup>
              <Label>Description</Label>
              <TextArea
                value={edu.description}
                onChange={(e) =>
                  updateEducation(edu.id, 'description', e.target.value)
                }
                placeholder="Relevant coursework, achievements, activities, or honors..."
              />
            </FormGroup>

            <ButtonGroup>
              <Button
                className="danger"
                onClick={() => removeEducation(edu.id)}
              >
                Remove
              </Button>
            </ButtonGroup>
          </EducationCard>
        ))}
      </EducationList>

      <AddButton className="primary" onClick={addEducation}>
        + Add Education
      </AddButton>

      {education.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>No education added yet. Click "Add Education" to get started.</p>
        </div>
      )}
    </Container>
  );
};

export default Education;
