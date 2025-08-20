from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CVViewSet, AICoverLetterViewSet, 
    UploadedCVViewSet, TemplateViewSet, CVAnalysisViewSet
)
from .api_views_enhanced import EnhancedCVViewSet, EnhancedTemplateViewSet

router = DefaultRouter()
router.register(r'cvs', CVViewSet, basename='cv')
router.register(r'ai-cover-letters', AICoverLetterViewSet, basename='aicoverletter')
router.register(r'uploaded-cvs', UploadedCVViewSet, basename='uploadedcv')
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'cv-analysis', CVAnalysisViewSet, basename='cvanalysis')

# Enhanced endpoints for React frontend
router.register(r'enhanced-cvs', EnhancedCVViewSet, basename='enhanced-cv')
router.register(r'enhanced-templates', EnhancedTemplateViewSet, basename='enhanced-template')

urlpatterns = [
    path('api/', include(router.urls)),
]
