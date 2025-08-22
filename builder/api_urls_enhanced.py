from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views_enhanced import (
    EnhancedCVViewSet,
    ExperienceViewSet,
    EducationViewSet,
    SkillViewSet,
    ProjectViewSet,
    CertificationViewSet,
    LanguageViewSet,
    AwardViewSet,
    EnhancedAICoverLetterViewSet,
    EnhancedUploadedCVViewSet,
    EnhancedTemplateViewSet,
    CVAnalysisViewSet
)

# Create router for enhanced API endpoints
router = DefaultRouter()

# CV Management
router.register(r'cv', EnhancedCVViewSet, basename='enhanced-cv')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'awards', AwardViewSet, basename='award')

# AI Services
router.register(r'ai-cover-letters', EnhancedAICoverLetterViewSet, basename='ai-cover-letter')
router.register(r'uploaded-cvs', EnhancedUploadedCVViewSet, basename='uploaded-cv')
router.register(r'templates', EnhancedTemplateViewSet, basename='template')
router.register(r'cv-analyses', CVAnalysisViewSet, basename='cv-analysis')

urlpatterns = [
    path('enhanced/', include(router.urls)),
]
