from django.db import models
from django.contrib.auth.models import User
import uuid

class CV(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CVSection(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Section for {self.cv.title}"

class CoverLetter(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(default='')
    generated_letter = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

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
    uploaded_cv = models.ForeignKey(UploadedCV, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    generated_letter = models.TextField()
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
    
    def __str__(self):
        return self.name
