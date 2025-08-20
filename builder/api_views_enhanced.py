from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CV, Template, CVAnalysis, Experience, Education, Project
from .serializers import CVSerializer, TemplateSerializer
from .ai_services import CVAnalysisService
import logging

logger = logging.getLogger(__name__)

class EnhancedCVViewSet(viewsets.ModelViewSet):
    """
    Enhanced CV ViewSet with additional endpoints for React frontend
    """
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_draft(self, request):
        """Create a new CV draft with auto-save"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cv = serializer.save(user=request.user, is_draft=True)
            return Response({
                'id': cv.id,
                'message': 'CV draft created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def auto_save(self, request, pk=None):
        """Auto-save CV data"""
        cv = self.get_object()
        serializer = self.get_serializer(cv, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'CV auto-saved',
                'last_saved': cv.updated_at
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Generate CV preview"""
        cv = self.get_object()
        serializer = self.get_serializer(cv)
        
        # Generate preview data with new model structure
        experiences = Experience.objects.filter(cv=cv)
        educations = Education.objects.filter(cv=cv)
        projects = Project.objects.filter(cv=cv)
        
        preview_data = {
            'cv': serializer.data,
            'experiences': [{'job_title': exp.job_title, 'company': exp.company, 'description': exp.description} for exp in experiences],
            'educations': [{'degree': edu.degree, 'institution': edu.institution} for edu in educations],
            'projects': [{'name': proj.name, 'description': proj.description} for proj in projects],
            'template': cv.template.name if cv.template else 'Default'
        }
        
        return Response(preview_data)

    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Get available templates"""
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def validate_data(self, request, pk=None):
        """Validate CV data"""
        cv = self.get_object()
        errors = []
        
        # Validate required fields
        if not cv.full_name:
            errors.append("Full name is required")
        if not cv.email:
            errors.append("Email is required")
        if not cv.summary:
            errors.append("Professional summary is required")
            
        # Validate related data
        experiences = Experience.objects.filter(cv=cv)
        if not experiences.exists():
            errors.append("At least one work experience is required")
        
        educations = Education.objects.filter(cv=cv)
        if not educations.exists():
            errors.append("At least one education entry is required")
            
        return Response({
            'is_valid': len(errors) == 0,
            'errors': errors
        })

class EnhancedTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """Enhanced template endpoints"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Get template preview"""
        template = self.get_object()
        return Response({
            'id': template.id,
            'name': template.name,
            'preview_image': template.preview_image.url if template.preview_image else None,
            'description': template.description,
            'fields': template.customizable_fields
        })
