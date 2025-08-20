import React from 'react';

const ProgressIndicator = ({ currentStep, totalSteps }) => {
  const steps = [
    { number: 1, title: 'Personal Info', description: 'Basic information' },
    { number: 2, title: 'Experience', description: 'Work history' },
    { number: 3, title: 'Education', description: 'Academic background' },
    { number: 4, title: 'Projects', description: 'Portfolio items' },
    { number: 5, title: 'Template', description: 'Choose design' },
  ];

  const getStepStatus = (stepNumber) => {
    if (stepNumber < currentStep) return 'completed';
    if (stepNumber === currentStep) return 'active';
    return 'pending';
  };

  const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;

  return (
    <div className="progress-indicator">
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progressPercentage}%` }}
        />
      </div>

      <div className="steps-container">
        {steps.map((step) => (
          <div
            key={step.number}
            className={`step ${getStepStatus(step.number)}`}
          >
            <div className="step-circle">
              {getStepStatus(step.number) === 'completed' ? (
                <svg
                  className="check-icon"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              ) : (
                <span className="step-number">{step.number}</span>
              )}
            </div>
            <div className="step-content">
              <div className="step-title">{step.title}</div>
              <div className="step-description">{step.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressIndicator;
