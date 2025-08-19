import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const AwardsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const AwardCard = styled.div`
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

const Awards = ({ data, updateData }) => {
  const [awards, setAwards] = useState(data.awards || []);

  const addAward = () => {
    const newAward = {
      id: Date.now(),
      title: '',
      issuer: '',
      date: '',
      type: 'academic',
      description: '',
      significance: '',
      url: '',
    };

    const updated = [...awards, newAward];
    setAwards(updated);
    updateData({ ...data, awards: updated });
  };

  const updateAward = (id, field, value) => {
    const updated = awards.map((award) =>
      award.id === id ? { ...award, [field]: value } : award
    );
    setAwards(updated);
    updateData({ ...data, awards: updated });
  };

  const removeAward = (id) => {
    const updated = awards.filter((award) => award.id !== id);
    setAwards(updated);
    updateData({ ...data, awards: updated });
  };

  const getAwardTypes = () => [
    { value: 'academic', label: 'Academic' },
    { value: 'professional', label: 'Professional' },
    { value: 'leadership', label: 'Leadership' },
    { value: 'innovation', label: 'Innovation' },
    { value: 'community', label: 'Community Service' },
    { value: 'sports', label: 'Sports' },
    { value: 'arts', label: 'Arts & Culture' },
    { value: 'other', label: 'Other' },
  ];

  return (
    <Container>
      <h2>Awards & Recognition</h2>
      <p>
        Showcase your achievements and recognition to demonstrate excellence and
        impact in your field
      </p>

      <AwardsList>
        {awards.map((award, index) => (
          <AwardCard key={award.id}>
            <h3>Award {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Award Title *</Label>
                <Input
                  type="text"
                  value={award.title}
                  onChange={(e) =>
                    updateAward(award.id, 'title', e.target.value)
                  }
                  placeholder="Dean's List Award"
                />
              </FormGroup>

              <FormGroup>
                <Label>Issuing Organization *</Label>
                <Input
                  type="text"
                  value={award.issuer}
                  onChange={(e) =>
                    updateAward(award.id, 'issuer', e.target.value)
                  }
                  placeholder="Stanford University"
                />
              </FormGroup>

              <FormGroup>
                <Label>Date Received *</Label>
                <Input
                  type="month"
                  value={award.date}
                  onChange={(e) =>
                    updateAward(award.id, 'date', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>Award Type *</Label>
                <Select
                  value={award.type}
                  onChange={(e) =>
                    updateAward(award.id, 'type', e.target.value)
                  }
                >
                  {getAwardTypes().map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </Select>
              </FormGroup>
            </Grid>

            <FormGroup>
              <Label>Description</Label>
              <TextArea
                value={award.description}
                onChange={(e) =>
                  updateAward(award.id, 'description', e.target.value)
                }
                placeholder="Brief description of the award and what it recognizes..."
              />
            </FormGroup>

            <FormGroup>
              <Label>Significance & Impact</Label>
              <TextArea
                value={award.significance}
                onChange={(e) =>
                  updateAward(award.id, 'significance', e.target.value)
                }
                placeholder="Explain why this award is significant and its impact on your career..."
              />
            </FormGroup>

            <FormGroup>
              <Label>Verification URL</Label>
              <Input
                type="url"
                value={award.url}
                onChange={(e) => updateAward(award.id, 'url', e.target.value)}
                placeholder="https://www.example.com/award-verification"
              />
            </FormGroup>

            <ButtonGroup>
              <Button className="danger" onClick={() => removeAward(award.id)}>
                Remove Award
              </Button>
            </ButtonGroup>
          </AwardCard>
        ))}
      </AwardsList>

      <AddButton className="primary" onClick={addAward}>
        + Add Award
      </AddButton>

      {awards.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>
            No awards added yet. Click "Add Award" to showcase your achievements
            and recognition.
          </p>
        </div>
      )}

      <div
        style={{
          marginTop: '2rem',
          padding: '1rem',
          background: '#f8f9fa',
          borderRadius: '8px',
        }}
      >
        <h4>Types of Awards to Consider:</h4>
        <ul style={{ fontSize: '0.9rem', color: '#6c757d' }}>
          <li>
            <strong>Academic:</strong> Dean's List, Scholarships, Research
            Awards
          </li>
          <li>
            <strong>Professional:</strong> Employee of the Month, Performance
            Awards
          </li>
          <li>
            <strong>Leadership:</strong> Leadership Excellence, Team Awards
          </li>
          <li>
            <strong>Innovation:</strong> Innovation Awards, Hackathon Prizes
          </li>
          <li>
            <strong>Community:</strong> Volunteer Recognition, Service Awards
          </li>
          <li>
            <strong>Sports:</strong> Athletic Achievements, Team Championships
          </li>
          <li>
            <strong>Arts:</strong> Creative Competitions, Cultural Awards
          </li>
        </ul>
      </div>
    </Container>
  );
};

export default Awards;
