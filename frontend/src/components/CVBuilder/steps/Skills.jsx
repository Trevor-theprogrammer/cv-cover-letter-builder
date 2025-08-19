import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const SkillsSection = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h3`
  color: #333;
  margin-bottom: 1rem;
`;

const SkillsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
`;

const SkillCategory = styled.div`
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
`;

const SkillInput = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
`;

const SkillTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
`;

const SkillTag = styled.div`
  display: flex;
  align-items: center;
  background: #667eea;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
`;

const RemoveButton = styled.button`
  background: none;
  border: none;
  color: white;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
`;

const AddButton = styled.button`
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease;

  &:hover {
    background: #218838;
  }
`;

const Suggestions = styled.div`
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
`;

const SuggestionTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
`;

const SuggestionTag = styled.button`
  background: #e9ecef;
  border: 1px solid #dee2e6;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #667eea;
    color: white;
    border-color: #667eea;
  }
`;

const Skills = ({ data, updateData }) => {
  const [newSkills, setNewSkills] = useState({
    technical: '',
    soft: '',
    languages: '',
    tools: ''
  });

  const [skills, setSkills] = useState(data.skills || {
    technical: [],
    soft: [],
    languages: [],
    tools: []
  });

  const skillSuggestions = {
    technical: ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Java', 'C++', 'TypeScript', 'AWS', 'Docker'],
    soft: ['Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Time Management', 'Adaptability', 'Critical Thinking'],
    languages: ['English', 'Spanish', 'French', 'German', 'Mandarin', 'Japanese', 'Portuguese', 'Arabic'],
    tools: ['Git', 'VS Code', 'Jira', 'Figma', 'Photoshop', 'Excel', 'PowerBI', 'Postman', 'MongoDB']
  };

  const addSkill = (category) => {
    const skillName = newSkills[category].trim();
    if (skillName && !skills[category].find(s => s.name.toLowerCase() === skillName.toLowerCase())) {
      const updatedSkills = {
        ...skills,
        [category]: [...skills[category], { name: skillName, level: 'Intermediate' }]
      };
      setSkills(updatedSkills);
      updateData({ ...data, skills: updatedSkills });
      setNewSkills({ ...newSkills, [category]: '' });
    }
  };

  const removeSkill = (category, skillName) => {
    const updatedSkills = {
      ...skills,
      [category]: skills[category].filter(s => s.name !== skillName)
    };
    setSkills(updatedSkills);
    updateData({ ...data, skills: updatedSkills });
  };

  const addSuggestedSkill = (category, skillName) => {
    if (!skills[category].find(s => s.name === skillName)) {
      const updatedSkills = {
        ...skills,
        [category]: [...skills[category], { name: skillName, level: 'Intermediate' }]
      };
      setSkills(updatedSkills);
      updateData({ ...data, skills: updatedSkills });
    }
  };

  const handleKeyPress = (category, e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill(category);
    }
  };

  const categories = [
    { key: 'technical', label: 'Technical Skills', placeholder: 'e.g., JavaScript, Python, React' },
    { key: 'soft', label: 'Soft Skills', placeholder: 'e.g., Leadership, Communication' },
    { key: 'languages', label: 'Languages', placeholder: 'e.g., English, Spanish' },
    { key: 'tools', label: 'Tools & Software', placeholder: 'e.g., Git, VS Code, Figma' }
  ];

  return (
    <Container>
      <h2>Skills & Expertise</h2>
      <p>Add your skills to highlight your professional capabilities</p>
      
      <SkillsGrid>
        {categories.map(category => (
          <SkillsSection key={category.key}>
            <SectionTitle>{category.label}</SectionTitle>
            
            <SkillInput
              type="text"
              value={newSkills[category.key]}
              onChange={(e) => setNewSkills({ ...newSkills, [category.key]: e.target.value })}
              onKeyPress={(e) => handleKeyPress(category.key, e)}
              placeholder={category.placeholder}
            />
            
            <AddButton onClick={() => addSkill(category.key)}>
              Add {category.label}
            </AddButton>
            
            <SkillTags>
              {skills[category.key].map(skill => (
                <SkillTag key={skill.name}>
                  {skill.name}
                  <RemoveButton onClick={() => removeSkill(category.key, skill.name)}>
                    ×
                  </RemoveButton>
                </SkillTag>
              ))}
            </SkillTags>
            
            <Suggestions>
              <strong>Suggestions:</strong>
              <SuggestionTags>
                {skillSuggestions[category.key].map(suggestion => (
                  <SuggestionTag
                    key={suggestion}
                    onClick={() => addSuggestedSkill(category.key, suggestion)}
                    disabled={skills[category.key].some(s => s.name === suggestion)}
                  >
                    {suggestion}
                  </SuggestionTag>
                ))}
              </SuggestionTags>
            </Suggestions>
          </SkillsSection>
        ))}
      </SkillsGrid>
    </Container>
  );
};

export default Skills;
