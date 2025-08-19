import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const TextArea = styled.textarea`
  width: 100%;
  min-height: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const CharacterCount = styled.div`
  text-align: right;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: ${(props) => (props.nearLimit ? '#e74c3c' : '#6c757d')};
`;

const Tips = styled.div`
  background: #f8f9fa;
  border-left: 4px solid #667eea;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
`;

const TipList = styled.ul`
  margin: 0.5rem 0;
  padding-left: 1.5rem;
`;

const Summary = ({ data, updateData }) => {
  const maxLength = 500;
  const currentLength = data.summary?.length || 0;

  const handleChange = (value) => {
    updateData({
      ...data,
      summary: value,
    });
  };

  const generateSummary = () => {
    const { personalInfo } = data;
    const title = personalInfo?.title || 'Professional';
    const experience = data.experience?.length || 0;
    const skills =
      data.skills
        ?.slice(0, 3)
        .map((s) => s.name)
        .join(', ') || '';

    const generated = `${title} with ${
      experience > 0 ? experience + ' years of' : ''
    } experience. Skilled in ${skills}. Passionate about delivering high-quality solutions and driving business growth through innovative approaches.`;

    updateData({
      ...data,
      summary: generated,
    });
  };

  return (
    <Container>
      <h2>Professional Summary</h2>
      <p>
        Write a compelling summary that highlights your key strengths and career
        goals
      </p>

      <TextArea
        value={data.summary || ''}
        onChange={(e) => handleChange(e.target.value)}
        placeholder="Example: Results-driven software engineer with 5+ years of experience in developing scalable web applications. Proven track record of delivering high-quality solutions using modern technologies. Passionate about clean code and continuous learning..."
        maxLength={maxLength}
      />

      <CharacterCount nearLimit={currentLength > maxLength * 0.9}>
        {currentLength}/{maxLength} characters
      </CharacterCount>

      <Tips>
        <strong>💡 Tips for a great summary:</strong>
        <TipList>
          <li>Keep it concise (3-4 sentences)</li>
          <li>Highlight your most relevant skills and experience</li>
          <li>Mention your career goals or what you're looking for</li>
          <li>Use action words and quantifiable achievements when possible</li>
        </TipList>
      </Tips>

      <button
        onClick={generateSummary}
        style={{
          marginTop: '1rem',
          padding: '0.5rem 1rem',
          background: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Generate Summary
      </button>
    </Container>
  );
};

export default Summary;
