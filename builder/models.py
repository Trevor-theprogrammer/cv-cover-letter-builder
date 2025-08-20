from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, URLValidator
import uuid
import json

class CV(models.Model):
    """Enhanced CV model with comprehensive fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()])
    portfolio_url = models.URLField(blank=True, validators=[URLValidator()])
    github_url = models.URLField(blank=True, validators=[URLValidator()])
    
    # Professional Summary
    summary = models.TextField(blank=True)
    professional_title = models.CharField(max_length=100, blank=True)
    
    # Template Selection
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status and Progress
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    
    # File Generation
    pdf_file = models.FileField(upload_to='generated_cvs/', blank=True, null=True)
    pdf_generation_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_saved = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s CV"

    def calculate_completion(self):
        """Calculate completion percentage based on filled fields"""
        required_fields = [
            self.full_name, self.email, self.summary,
            self.professional_title
        ]
        filled_fields = sum(1 for field in required_fields if field)
        
        # Check for at least one experience entry
        has_experience = self.experiences.exists()
        # Check for at least one education entry
        has_education = self.educations.exists()
        
        total_required = len(required_fields) + 2  # +2 for experience and education
        filled_total = filled_fields + (1 if has_experience else 0) + (1 if has_education else 0)
        
        return int((filled_total / total_required) * 100)

    def save(self, *args, **kwargs):
        self.completion_percentage = self.calculate_completion()
        super().save(*args, **kwargs)

class Experience(models.Model):
    """Work experience entries for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.JSONField(default=list)  # List of achievements
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class Education(models.Model):
    """Education entries for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    gpa = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Skill(models.Model):
    """Skills for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    category = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

class Project(models.Model):
    """Projects for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.JSONField(default=list)
    url = models.URLField(blank=True, validators=[URLValidator()])
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

class Certification(models.Model):
    """Certifications for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True, validators=[URLValidator()])
    
    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return self.name

class Language(models.Model):
    """Languages for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('conversational', 'Conversational'),
            ('fluent', 'Fluent'),
            ('native', 'Native'),
        ],
        default='conversational'
    )
    
    def __str__(self):
        return self.name

class Award(models.Model):
    """Awards and achievements for CV"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='awards')
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

# These redundant models have been removed in favor of the enhanced models above
# The new CV model includes comprehensive fields and relationships

# New AI-powered models
class UploadedCV(models.Model):
    """Model for storing uploaded CV files (PDF/DOCX)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_cvs/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.original_filename} - {self.user.username}"

class AICoverLetter(models.Model):
    """Model for AI-generated cover letters"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_cv = models.ForeignKey(UploadedCV, on_delete=models.CASCADE, null=True, blank=True)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    generated_letter = models.TextField()
    cv_analysis = models.TextField(blank=True)
    template_type = models.CharField(max_length=50, default='standard')
    tone = models.CharField(max_length=20, choices=[
        ('professional', 'Professional'),
        ('creative', 'Creative'),
        ('formal', 'Formal'),
        ('casual', 'Casual'),
    ], default='professional')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"AI Cover Letter for {self.job_title}"

class CVAnalysis(models.Model):
    """Model for CV strength analysis results"""
    uploaded_cv = models.OneToOneField(UploadedCV, on_delete=models.CASCADE)
    overall_score = models.IntegerField(default=0)
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    keywords = models.JSONField(default=dict)
    experience_level = models.CharField(max_length=50, default='Entry Level')
    ats_compatibility = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.uploaded_cv.original_filename}"

class Template(models.Model):
    """Model for editable cover letter templates"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    template_content = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_image = models.ImageField(
        upload_to='template_previews/',
        null=True,
        blank=True,
        help_text='Preview image for the template'
    )
    type = models.CharField(
        max_length=20,
        choices=[
            ('cv', 'CV Template'),
            ('cover_letter', 'Cover Letter Template')
        ],
        default='cv'
    )
    style = models.CharField(
        max_length=20,
        choices=[
            ('modern', 'Modern'),
            ('classic', 'Classic'),
            ('creative', 'Creative'),
            ('minimal', 'Minimal'),
            ('basic', 'Basic')
        ],
        default='modern'
    )

    def __str__(self):
        return self.name
