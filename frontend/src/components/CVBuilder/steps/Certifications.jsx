import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const CertificationsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const CertificationCard = styled.div`
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

const Certifications = ({ data, updateData }) => {
  const [certifications, setCertifications] = useState(
    data.certifications || []
  );

  const addCertification = () => {
    const newCert = {
      id: Date.now(),
      name: '',
      issuer: '',
      issueDate: '',
      expiryDate: '',
      credentialId: '',
      credentialUrl: '',
      description: '',
      skills: [],
    };

    const updated = [...certifications, newCert];
    setCertifications(updated);
    updateData({ ...data, certifications: updated });
  };

  const updateCertification = (id, field, value) => {
    const updated = certifications.map((cert) =>
      cert.id === id ? { ...cert, [field]: value } : cert
    );
    setCertifications(updated);
    updateData({ ...data, certifications: updated });
  };

  const removeCertification = (id) => {
    const updated = certifications.filter((cert) => cert.id !== id);
    setCertifications(updated);
    updateData({ ...data, certifications: updated });
  };

  const handleSkillsChange = (id, skillsString) => {
    const skills = skillsString
      .split(',')
      .map((skill) => skill.trim())
      .filter((skill) => skill);
    updateCertification(id, 'skills', skills);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  return (
    <Container>
      <h2>Certifications & Licenses</h2>
      <p>
        Add your professional certifications and licenses to validate your
        expertise
      </p>

      <CertificationsList>
        {certifications.map((cert, index) => (
          <CertificationCard key={cert.id}>
            <h3>Certification {index + 1}</h3>

            <Grid>
              <FormGroup>
                <Label>Certification Name *</Label>
                <Input
                  type="text"
                  value={cert.name}
                  onChange={(e) =>
                    updateCertification(cert.id, 'name', e.target.value)
                  }
                  placeholder="AWS Certified Solutions Architect"
                />
              </FormGroup>

              <FormGroup>
                <Label>Issuing Organization *</Label>
                <Input
                  type="text"
                  value={cert.issuer}
                  onChange={(e) =>
                    updateCertification(cert.id, 'issuer', e.target.value)
                  }
                  placeholder="Amazon Web Services"
                />
              </FormGroup>

              <FormGroup>
                <Label>Issue Date *</Label>
                <Input
                  type="month"
                  value={cert.issueDate}
                  onChange={(e) =>
                    updateCertification(cert.id, 'issueDate', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>Expiry Date</Label>
                <Input
                  type="month"
                  value={cert.expiryDate}
                  onChange={(e) =>
                    updateCertification(cert.id, 'expiryDate', e.target.value)
                  }
                />
              </FormGroup>

              <FormGroup>
                <Label>Credential ID</Label>
                <Input
                  type="text"
                  value={cert.credentialId}
                  onChange={(e) =>
                    updateCertification(cert.id, 'credentialId', e.target.value)
                  }
                  placeholder="AWS-12345678"
                />
              </FormGroup>

              <FormGroup>
                <Label>Credential URL</Label>
                <Input
                  type="url"
                  value={cert.credentialUrl}
                  onChange={(e) =>
                    updateCertification(
                      cert.id,
                      'credentialUrl',
                      e.target.value
                    )
                  }
                  placeholder="https://www.credly.com/badges/..."
                />
              </FormGroup>
            </Grid>

            <FormGroup>
              <Label>Description</Label>
              <TextArea
                value={cert.description}
                onChange={(e) =>
                  updateCertification(cert.id, 'description', e.target.value)
                }
                placeholder="Brief description of what this certification covers and its significance..."
              />
            </FormGroup>

            <FormGroup>
              <Label>Relevant Skills (comma-separated)</Label>
              <Input
                type="text"
                value={cert.skills.join(', ')}
                onChange={(e) => handleSkillsChange(cert.id, e.target.value)}
                placeholder="Cloud Computing, AWS, Architecture, Security"
              />
            </FormGroup>

            <ButtonGroup>
              <Button
                className="danger"
                onClick={() => removeCertification(cert.id)}
              >
                Remove Certification
              </Button>
            </ButtonGroup>
          </CertificationCard>
        ))}
      </CertificationsList>

      <AddButton className="primary" onClick={addCertification}>
        + Add Certification
      </AddButton>

      {certifications.length === 0 && (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6c757d' }}>
          <p>
            No certifications added yet. Click "Add Certification" to showcase
            your credentials.
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
        <h4>Popular Certifications to Consider:</h4>
        <ul style={{ fontSize: '0.9rem', color: '#6c757d' }}>
          <li>AWS Certified Solutions Architect</li>
          <li>Google Cloud Professional Cloud Architect</li>
          <li>Microsoft Azure Fundamentals</li>
          <li>Certified Kubernetes Administrator (CKA)</li>
          <li>Project Management Professional (PMP)</li>
          <li>Certified Scrum Master (CSM)</li>
          <li>Google Analytics Individual Qualification</li>
          <li>HubSpot Inbound Marketing Certification</li>
        </ul>
      </div>
    </Container>
  );
};

export default Certifications;
