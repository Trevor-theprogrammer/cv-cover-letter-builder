import React from 'react';

const PersonalInfoForm = ({ data, onChange, errors }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange({ [name]: value });
  };

  return (
    <div className="personal-info-form">
      <h2>Personal Information</h2>

      <div className="form-group">
        <label htmlFor="full_name">Full Name *</label>
        <input
          type="text"
          id="full_name"
          name="full_name"
          value={data.full_name || ''}
          onChange={handleChange}
          className={errors.full_name ? 'error' : ''}
          placeholder="Enter your full name"
        />
        {errors.full_name && (
          <span className="error-message">{errors.full_name}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="email">Email Address *</label>
        <input
          type="email"
          id="email"
          name="email"
          value={data.email || ''}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
          placeholder="Enter your email address"
        />
        {errors.email && <span className="error-message">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="phone">Phone Number</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={data.phone || ''}
          onChange={handleChange}
          placeholder="Enter your phone number"
        />
      </div>

      <div className="form-group">
        <label htmlFor="location">Location</label>
        <input
          type="text"
          id="location"
          name="location"
          value={data.location || ''}
          onChange={handleChange}
          placeholder="City, Country"
        />
      </div>

      <div className="form-group">
        <label htmlFor="summary">Professional Summary *</label>
        <textarea
          id="summary"
          name="summary"
          value={data.summary || ''}
          onChange={handleChange}
          className={errors.summary ? 'error' : ''}
          placeholder="Write a brief professional summary..."
          rows="4"
        />
        {errors.summary && (
          <span className="error-message">{errors.summary}</span>
        )}
      </div>
    </div>
  );
};

export default PersonalInfoForm;
