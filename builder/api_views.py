from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CV, AICoverLetter, UploadedCV, Template, CVAnalysis, Experience, Education, Project
from .serializers import (
    CVSerializer, AICoverLetterSerializer, 
    UploadedCVSerializer, TemplateSerializer, CVAnalysisSerializer
)
from .ai_services import EnhancedAICoverLetterService
import logging
import json

logger = logging.getLogger(__name__)

class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_cover_letter(self, request, pk=None):
        """Generate cover letter for this CV"""
        cv = self.get_object()
        job_title = request.data.get('job_title')
        job_description = request.data.get('job_description')
        tone = request.data.get('tone', 'professional')
        
        if not job_title or not job_description:
            return Response(
                {'error': 'Job title and description are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = EnhancedAICoverLetterService()
            cv_text = self._extract_cv_text(cv)
            
            cv_insights = service.extract_cv_insights(cv_text)
            job_match = service.match_cv_to_job(cv_insights, job_title, job_description)
            cover_letter = service.generate_tailored_cover_letter(
                cv_insights, job_match, job_title, job_description, tone
            )
            
            ai_cover_letter = AICoverLetter.objects.create(
                user=request.user,
                job_title=job_title,
                job_description=job_description,
                generated_letter=cover_letter,
                cv_analysis=cv_text[:500],
                tone=tone
            )
            
            return Response({
                'cover_letter': cover_letter,
                'cv_insights': cv_insights,
                'job_match': job_match,
                'id': ai_cover_letter.id
            })
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {str(e)}")
            return Response(
                {'error': 'Failed to generate cover letter'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        """Export CV as PDF - placeholder implementation"""
        return Response(
            {'error': 'PDF generation not yet implemented'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def _extract_cv_text(self, cv):
        """Extract text content from CV"""
        text_parts = []
        if cv.summary:
            text_parts.append(f"Summary: {cv.summary}")
        
        # Add experiences
        experiences = Experience.objects.filter(cv=cv)
        for exp in experiences:
            text_parts.append(f"Experience: {exp.job_title} at {exp.company} - {exp.description}")
        
        # Add education
        educations = Education.objects.filter(cv=cv)
        for edu in educations:
            text_parts.append(f"Education: {edu.degree} from {edu.institution}")
        
        # Add projects
        projects = Project.objects.filter(cv=cv)
        for proj in projects:
            text_parts.append(f"Project: {proj.name} - {proj.description}")
        
        return "\n\n".join(text_parts)

class AICoverLetterViewSet(viewsets.ModelViewSet):
    serializer_class = AICoverLetterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AICoverLetter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate cover letter with new parameters"""
        cover_letter = self.get_object()
        tone = request.data.get('tone', cover_letter.tone)
        
        try:
            service = EnhancedAICoverLetterService()
            cv = cover_letter.cv
            
            cv_text = self._extract_cv_text(cv)
            cv_insights = service.extract_cv_insights(cv_text)
            job_match = service.match_cv_to_job(
                cv_insights, 
                cover_letter.job_title, 
                cover_letter.job_description
            )
            
            new_letter = service.generate_tailored_cover_letter(
                cv_insights, job_match, 
                cover_letter.job_title, 
                cover_letter.job_description, 
                tone
            )
            
            cover_letter.generated_letter = new_letter
            cover_letter.tone = tone
            cover_letter.save()
            
            return Response({
                'cover_letter': new_letter,
                'cv_insights': cv_insights,
                'job_match': job_match
            })
            
        except Exception as e:
            logger.error(f"Cover letter regeneration failed: {str(e)}")
            return Response(
                {'error': 'Failed to regenerate cover letter'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _extract_cv_text(self, cover_letter):
        """Extract text content from CV"""
        cv = cover_letter.cv
        text_parts = []
        if cv.summary:
            text_parts.append(f"Summary: {cv.summary}")
        
        # Add experiences
        experiences = Experience.objects.filter(cv=cv)
        for exp in experiences:
            text_parts.append(f"Experience: {exp.job_title} at {exp.company} - {exp.description}")
        
        # Add education
        educations = Education.objects.filter(cv=cv)
        for edu in educations:
            text_parts.append(f"Education: {edu.degree} from {edu.institution}")
        
        # Add projects
        projects = Project.objects.filter(cv=cv)
        for proj in projects:
            text_parts.append(f"Project: {proj.name} - {proj.description}")
        
        return "\n\n".join(text_parts)

class UploadedCVViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedCVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedCV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def placeholder_action(self, request, pk=None):
        """Placeholder action to fix indentation error."""
        pass

class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Template.objects.all()

class CVAnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = CVAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CVAnalysis.objects.filter(cv__user=self.request.user)
