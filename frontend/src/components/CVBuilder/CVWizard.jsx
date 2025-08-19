import React from 'react';
import styled from 'styled-components';
import PersonalInfo from './steps/PersonalInfo';
import Summary from './steps/Summary';
import Experience from './steps/Experience';
import Education from './steps/Education';
import Skills from './steps/Skills';
import Projects from './steps/Projects';
import Certifications from './steps/Certifications';
import Languages from './steps/Languages';
import Awards from './steps/Awards';
import TemplateSelect from './steps/TemplateSelect';

const WizardContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const WizardHeader = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
`;

const WizardTitle = styled.h1`
  margin: 0;
  font-size: 2.5rem;
  font-weight: 300;
`;

const WizardSubtitle = styled.p`
  margin: 0.5rem 0 0;
  opacity: 0.9;
  font-size: 1.1rem;
`;

const StepIndicator = styled.div`
  display: flex;
  justify-content: center;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
`;

const Step = styled.div`
  display: flex;
  align-items: center;
  margin: 0 1rem;
  font-size: 0.9rem;
  color: ${(props) => (props.active ? '#667eea' : '#6c757d')};
  font-weight: ${(props) => (props.active ? '600' : '400')};
`;

const StepNumber = styled.div`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: ${(props) => (props.active ? '#667eea' : '#e9ecef')};
  color: ${(props) => (props.active ? 'white' : '#6c757d')};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  font-weight: 600;
`;

const WizardContent = styled.div`
  padding: 2rem;
  min-height: 500px;
`;

const WizardActions = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 2rem;
  border-top: 1px solid #e9ecef;
`;

const Button = styled.button`
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;

  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
  }

  &.secondary {
    background: #e9ecef;
    color: #495057;

    &:hover {
      background: #dee2e6;
    }
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const steps = [
  { id: 1, title: 'Personal Info', component: PersonalInfo },
  { id: 2, title: 'Summary', component: Summary },
  { id: 3, title: 'Experience', component: Experience },
  { id: 4, title: 'Education', component: Education },
  { id: 5, title: 'Skills', component: Skills },
  { id: 6, title: 'Projects', component: Projects },
  { id: 7, title: 'Certifications', component: Certifications },
  { id: 8, title: 'Languages', component: Languages },
  { id: 9, title: 'Awards', component: Awards },
  { id: 10, title: 'Template', component: TemplateSelect },
];

const CVWizard = ({
  cvData,
  updateCVData,
  currentStep,
  nextStep,
  prevStep,
}) => {
  const CurrentStepComponent = steps[currentStep - 1].component;

  return (
    <WizardContainer>
      <WizardHeader>
        <WizardTitle>Create Your Professional CV</WizardTitle>
        <WizardSubtitle>Build a stunning resume in minutes</WizardSubtitle>
      </WizardHeader>

      <StepIndicator>
        {steps.map((step) => (
          <Step key={step.id} active={currentStep === step.id}>
            <StepNumber active={currentStep === step.id}>{step.id}</StepNumber>
            {step.title}
          </Step>
        ))}
      </StepIndicator>

      <WizardContent>
        <CurrentStepComponent data={cvData} updateData={updateCVData} />
      </WizardContent>

      <WizardActions>
        <Button
          className="secondary"
          onClick={prevStep}
          disabled={currentStep === 1}
        >
          Previous
        </Button>
        <Button
          className="primary"
          onClick={nextStep}
          disabled={currentStep === steps.length}
        >
          {currentStep === steps.length ? 'Generate CV' : 'Next'}
        </Button>
      </WizardActions>
    </WizardContainer>
  );
};

export default CVWizard;
