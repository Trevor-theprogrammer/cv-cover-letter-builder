import React from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  min-height: 80px;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const FullWidth = styled.div`
  grid-column: 1 / -1;
`;

const PersonalInfo = ({ data, updateData }) => {
  const handleChange = (field, value) => {
    updateData({
      ...data,
      personalInfo: {
        ...data.personalInfo,
        [field]: value
      }
    });
  };

  return (
    <div>
      <h2>Personal Information</h2>
      <p>Let's start with your basic details</p>
      
      <FormContainer>
        <FormGroup>
          <Label>First Name *</Label>
          <Input
            type="text"
            value={data.personalInfo?.firstName || ''}
            onChange={(e) => handleChange('firstName', e.target.value)}
            placeholder="John"
          />
        </FormGroup>

        <FormGroup>
          <Label>Last Name *</Label>
          <Input
            type="text"
            value={data.personalInfo?.lastName || ''}
            onChange={(e) => handleChange('lastName', e.target.value)}
            placeholder="Doe"
          />
        </FormGroup>

        <FormGroup>
          <Label>Email *</Label>
          <Input
            type="email"
            value={data.personalInfo?.email || ''}
            onChange={(e) => handleChange('email', e.target.value)}
            placeholder="john.doe@email.com"
          />
        </FormGroup>

        <FormGroup>
          <Label>Phone *</Label>
          <Input
            type="tel"
            value={data.personalInfo?.phone || ''}
            onChange={(e) => handleChange('phone', e.target.value)}
            placeholder="+1 (555) 123-4567"
          />
        </FormGroup>

        <FormGroup>
          <Label>Location</Label>
          <Input
            type="text"
            value={data.personalInfo?.location || ''}
            onChange={(e) => handleChange('location', e.target.value)}
            placeholder="New York, NY"
          />
        </FormGroup>

        <FormGroup>
          <Label>LinkedIn URL</Label>
          <Input
            type="url"
            value={data.personalInfo?.linkedin || ''}
            onChange={(e) => handleChange('linkedin', e.target.value)}
            placeholder="linkedin.com/in/johndoe"
          />
        </FormGroup>

        <FormGroup>
          <Label>Portfolio/Website</Label>
          <Input
            type="url"
            value={data.personalInfo?.website || ''}
            onChange={(e) => handleChange('website', e.target.value)}
            placeholder="johndoe.dev"
          />
        </FormGroup>

        <FullWidth>
          <FormGroup>
            <Label>Professional Title</Label>
            <Input
              type="text"
              value={data.personalInfo?.title || ''}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Senior Software Engineer"
            />
          </FormGroup>
        </FullWidth>
      </FormContainer>
    </div>
  );
};

export default PersonalInfo;
