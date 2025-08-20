import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CVPreview = ({ cvId, cvData }) => {
    const [previewData, setPreviewData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (cvId) {
            fetchPreview();
        }
    }, [cvId, cvData]);

    const fetchPreview = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`/api/enhanced-cvs/${cvId}/preview/`);
            setPreviewData(response.data);
        } catch (error) {
            console.error('Failed to fetch preview:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="cv-preview loading">
                <div className="loading-spinner">Loading preview...</div>
            </div>
        );
    }

    if (!previewData) {
        return (
            <div className="cv-preview empty">
                <div className="empty-state">
                    <h3>CV Preview</h3>
                    <p>Your CV preview will appear here as you fill in the information.</p>
                </div>
            </div>
        );
    }

    const { cv, sections, template } = previewData;

    return (
        <div className="cv-preview">
            <div className="preview-header">
                <h3>Preview</h3>
                <div className="template-info">
                    Template: {template || 'Default'}
                </div>
            </div>

            <div className="preview-content">
                {/* Header Section */}
                <div className="cv-header">
                    <h1>{cv.full_name || 'Your Name'}</h1>
                    <div className="contact-info">
                        {cv.email && <span>{cv.email}</span>}
                        {cv.phone && <span>{cv.phone}</span>}
                        {cv.location && <span>{cv.location}</span>}
                    </div>
                </div>

                {/* Professional Summary */}
                {cv.summary && (
                    <div className="cv-section">
                        <h2>Professional Summary</h2>
                        <p>{cv.summary}</p>
                    </div>
                )}

                {/* Experience Section */}
                {cvData.sections?.experience?.length > 0 && (
                    <div className="cv-section">
                        <h2>Work Experience</h2>
                        {cvData.sections.experience.map((exp, index) => (
                            <div key={index} className="experience-item">
                                <div className="item-header">
                                    <h3>{exp.job_title}</h3>
                                    <span className="company">{exp.company}</span>
                                </div>
                                <div className="item-meta">
                                    <span className="date">
                                        {exp.start_date} - {exp.is_current ? 'Present' : exp.end_date}
                                    </span>
                                    {exp.location && <span className="location">{exp.location}</span>}
                                </div>
                                {exp.description && (
                                    <p className="description">{exp.description}</p>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Education Section */}
                {cvData.sections?.education?.length > 0 && (
                    <div className="cv-section">
                        <h2>Education</h2>
                        {cvData.sections.education.map((edu, index) => (
                            <div key={index} className="education-item">
                                <div className="item-header">
                                    <h3>{edu.degree}</h3>
                                    <span className="institution">{edu.institution}</span>
                                </div>
                                <div className="item-meta">
                                    <span className="date">
                                        {edu.start_date} - {edu.is_current ? 'Present' : edu.end_date}
                                    </span>
                                    {edu.location && <span className="location">{edu.location}</span>}
                                    {edu.gpa && <span className="gpa">GPA: {edu.gpa}</span>}
                                </div>
                                {edu.description && (
                                    <p className="description">{edu.description}</p>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Projects Section */}
                {cvData.sections?.projects?.length > 0 && (
                    <div className="cv-section">
                        <h2>Projects</h2>
                        {cvData.sections.projects.map((project, index) => (
                            <div key={index} className="project-item">
                                <div className="item-header">
                                    <h3>{project.name}</h3>
                                    {project.url && (
                                        <a href={project.url} target="_blank" rel="noopener noreferrer">
                                            View Project
                                        </a>
                                    )}
                                </div>
                                <div className="item-meta">
                                    <span className="date">
                                        {project.start_date} - {project.is_current ? 'Present' : project.end_date}
                                    </span>
                                    {project.technologies?.length > 0 && (
                                        <div className="technologies">
                                            {project.technologies.map((tech, i) => (
                                                <span key={i} className="tech-tag">{tech}</span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                {project.description && (
                                    <p className="description">{project.description}</p>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default CVPreview;
