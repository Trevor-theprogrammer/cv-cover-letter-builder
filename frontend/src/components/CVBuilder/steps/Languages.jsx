import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const LanguagesList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const LanguageCard = styled.div`
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
  background: white;
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

const ProficiencyIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
`;

const ProficiencyBar = styled.div`
  flex: 1;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
`;

const ProficiencyFill = styled.div`
  height: 100%;
  background: ${(props) => {
    switch (props.level) {
      case 'native':
        return '#28a745';
      case 'fluent':
        return '#17a2b8';
      case 'advanced':
        return '#ffc107';
      case 'intermediate':
        return '#fd7e14';
      case 'basic':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  }};
  width: ${(props) => {
    switch (props.level) {
      case 'native':
        return '100%';
      case 'fluent':
        return '85%';
      case 'advanced':
        return '70%';
      case 'intermediate':
        return '50%';
      case 'basic':
        return '30%';
      default:
        return '0%';
    }
  }};
  transition: width 0.3s ease;
`;

const ProficiencyLabel = styled.span`
  font-size: 0.8rem;
  color: #6c757d;
  text-transform: capitalize;
`;

const Languages = ({ data, updateData }) => {
  const [languages, setLanguages] = useState(data.languages || []);

  const addLanguage = () => {
    const newLanguage = {
      id: Date.now(),
      name: '',
      proficiency: 'basic',
      isNative: false,
      certification: '',
      certificationLevel: '',
      yearsOfExperience: 0,
    };

    const updated = [...languages, newLanguage];
    setLanguages(updated);
    updateData({ ...data, languages: updated });
  };

  const updateLanguage = (id, field, value) => {
    const updated = languages.map((lang) =>
      lang.id === id ? { ...lang, [field]: value } : lang
    );
    setLanguages(updated);
    updateData({ ...data, languages: updated });
  };

  const removeLanguage = (id) => {
    const updated = languages.filter((lang) => lang.id !== id);
    setLanguages(updated);
    updateData({ ...data, languages: updated });
  };

  const getProficiencyOptions = () => [
    { value: 'native', label: 'Native' },
    { value: 'fluent', label: 'Fluent' },
    { value: 'advanced', label: 'Advanced' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'basic', label: 'Basic' },
  ];

  const getLanguageOptions = () => [
    'English',
    'Spanish',
    'French',
    'German',
    'Italian',
    'Portuguese',
    'Russian',
    'Chinese (Mandarin)',
    'Chinese (Cantonese)',
    'Japanese',
    'Korean',
    'Arabic',
    'Hindi',
    'Bengali',
    'Urdu',
    'Turkish',
    'Dutch',
    'Swedish',
    'Norwegian',
    'Danish',
    'Finnish',
    'Polish',
    'Czech',
    'Hungarian',
    'Romanian',
    'Greek',
    'Hebrew',
    'Thai',
    'Vietnamese',
    'Indonesian',
    'Malay',
    'Tagalog',
    'Swahili',
  ];

  return (
    <Container>
      <h2>Languages</h2>
      <p>
        Highlight your language skills to demonstrate your ability to work in
        international environments
      </p>

      <LanguagesList>
        {languages.map((language, index) => (
          <LanguageCard key={language.id}>
            <h3>Language {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Language *</Label>
                <Select
                  value={language.name}
                  onChange={(e) =>
                    updateLanguage(language.id, 'name', e.target.value)
                  }
                >
                  <option value="">Select a language</option>
                  {getLanguageOptions().map((lang) => (
                    <option key={lang} value={lang}>
                      {lang}
                    </option>
                  ))}
                </Select>
              </FormGroup>

              <FormGroup>
                <Label>Proficiency Level *</Label>
                <Select
                  value={language.proficiency}
                  onChange={(e) =>
                    updateLanguage(language.id, 'proficiency', e.target.value)
                  }
                >
                  {getProficiencyOptions().map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Select>
                <ProficiencyIndicator>
                  <ProficiencyLabel>{language.proficiency}</ProficiencyLabel>
                  <ProficiencyBar>
                    <ProficiencyFill level={language.proficiency} />
                  </ProficiencyBar>
                </ProficiencyIndicator>
              </FormGroup>

              <FormGroup>
                <Label>
                  <input
                    type="checkbox"
                    checked={language.isNative}
                    onChange={(e) =>
                      updateLanguage(language.id, 'isNative', e.target.checked)
                    }
                  />
                  This is my native language
                </Label>
              </FormGroup>

              <FormGroup>
                <Label>Years of Experience</Label>
                <Input
                  type="number"
                  min="0"
                  max="50"
                  value={language.yearsOfExperience}
                  onChange={(e) =>
                    updateLanguage(
                      language.id,
                      'yearsOfExperience',
                      parseInt(e.target.value) || 0
                    )
                  }
                  placeholder="5"
                />
              </FormGroup>

              <FormGroup>
                <Label>Language Certification</Label>
                <Input
                  type="text"
                  value={cert.certification}
                  onChange={(e) =>
                    updateLanguage(language.id, 'certification', e.target.value)
                  }
                  placeholder="TOEFL, IELTS, DELE, etc."
                />
              </FormGroup>

              <FormGroup>
                <Label>Certification Level</Label>
                <Input
                  type="text"
                  value={cert.certificationLevel}
                  onChange={(e) =>
                    updateLanguage(
                      language.id,
                      'certificationLevel',
                      e.target.value
                    )
                  }
                  placeholder="C1, B2, Advanced, etc."
                />
              </FormGroup>
            </Grid>

            <ButtonGroup>
              <Button
                className="danger"
                onClick={() => removeLanguage(language.id)}
              >
                Remove Language
              </Button>
            </ButtonGroup>
          </LanguageCard>
        ))}
      </LanguagesList>

      <AddButton className="primary" onClick={addLanguage}>
        + Add Language
      </AddButton>

      {languages.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>
            No languages added yet. Click "Add Language" to showcase your
            multilingual abilities.
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
        <h4>Language Proficiency Guidelines:</h4>
        <ul style={{ fontSize: '0.9rem', color: '#6c757d' }}>
          <li>
            <strong>Native:</strong> Mother tongue or equivalent fluency
          </li>
          <li>
            <strong>Fluent:</strong> Professional working proficiency
          </li>
          <li>
            <strong>Advanced:</strong> Can handle complex discussions and
            presentations
          </li>
          <li>
            <strong>Intermediate:</strong> Can manage everyday conversations and
            basic work tasks
          </li>
          <li>
            <strong>Basic:</strong> Can understand and use familiar everyday
            expressions
          </li>
        </ul>
      </div>
    </Container>
  );
};

export default Languages;
