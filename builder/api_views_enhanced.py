from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from .models import (
    CV, Experience, Education, Skill, Project, 
    Certification, Language, Award, AICoverLetter, 
    UploadedCV, Template, CVAnalysis
)
from .serializers import (
    CVSerializer, ExperienceSerializer, EducationSerializer,
    SkillSerializer, ProjectSerializer, CertificationSerializer,
    LanguageSerializer, AwardSerializer, AICoverLetterSerializer,
    UploadedCVSerializer, TemplateSerializer, CVAnalysisSerializer
)
from .ai_services import EnhancedAICoverLetterService
from .cv_analysis_service import CVAnalysisService
import logging
import json

logger = logging.getLogger(__name__)

class EnhancedCVViewSet(viewsets.ModelViewSet):
    """Enhanced CV ViewSet with comprehensive endpoints"""
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user).prefetch_related(
            'experiences', 'educations', 'skills', 'projects',
            'certifications', 'languages', 'awards'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def completion_status(self, request, pk=None):
        """Get detailed completion status for CV"""
        cv = self.get_object()
        return Response({
            'completion_percentage': cv.completion_percentage,
            'is_completed': cv.is_completed,
            'missing_sections': self._get_missing_sections(cv)
        })

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a CV with all its content"""
        original_cv = self.get_object()
        
        with transaction.atomic():
            # Create new CV
            new_cv = CV.objects.create(
                user=request.user,
                title=f"{original_cv.title} (Copy)",
                full_name=original_cv.full_name,
                email=original_cv.email,
                phone=original_cv.phone,
                location=original_cv.location,
                linkedin_url=original_cv.linkedin_url,
                portfolio_url=original_cv.portfolio_url,
                github_url=original_cv.github_url,
                summary=original_cv.summary,
                professional_title=original_cv.professional_title,
                template=original_cv.template
            )
            
            # Copy experiences
            for exp in original_cv.experiences.all():
                Experience.objects.create(
                    cv=new_cv,
                    job_title=exp.job_title,
                    company=exp.company,
                    location=exp.location,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    is_current=exp.is_current,
                    description=exp.description,
                    achievements=exp.achievements
                )
            
            # Copy education
            for edu in original_cv.educations.all():
                Education.objects.create(
                    cv=new_cv,
                    degree=edu.degree,
                    institution=edu.institution,
                    location=edu.location,
                    start_date=edu.start_date,
                    end_date=edu.end_date,
                    is_current=edu.is_current,
                    gpa=edu.gpa,
                    description=edu.description
                )
            
            # Copy skills
            for skill in original_cv.skills.all():
                Skill.objects.create(
                    cv=new_cv,
                    name=skill.name,
                    level=skill.level,
                    category=skill.category
                )
            
            # Copy projects
            for proj in original_cv.projects.all():
                Project.objects.create(
                    cv=new_cv,
                    name=proj.name,
                    description=proj.description,
                    technologies=proj.technologies,
                    url=proj.url,
                    start_date=proj.start_date,
                    end_date=proj.end_date,
                    is_current=proj.is_current
                )
            
            # Copy certifications
            for cert in original_cv.certifications.all():
                Certification.objects.create(
                    cv=new_cv,
                    name=cert.name,
                    issuer=cert.issuer,
                    issue_date=cert.issue_date,
                    expiry_date=cert.expiry_date,
                    credential_id=cert.credential_id,
                    url=cert.url
                )
            
            # Copy languages
            for lang in original_cv.languages.all():
                Language.objects.create(
                    cv=new_cv,
                    name=lang.name,
                    proficiency=lang.proficiency
                )
            
            # Copy awards
            for award in original_cv.awards.all():
                Award.objects.create(
                    cv=new_cv,
                    name=award.name,
                    issuer=award.issuer,
                    date=award.date,
                    description=award.description
                )
        
        serializer = self.get_serializer(new_cv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_missing_sections(self, cv):
        """Identify missing sections in CV"""
        missing = []
        
        if not cv.summary:
            missing.append('summary')
        if not cv.experiences.exists():
            missing.append('experience')
        if not cv.educations.exists():
            missing.append('education')
        if not cv.skills.exists():
            missing.append('skills')
        
        return missing

class ExperienceViewSet(viewsets.ModelViewSet):
    """Experience management endpoints"""
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class EducationViewSet(viewsets.ModelViewSet):
    """Education management endpoints"""
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class SkillViewSet(viewsets.ModelViewSet):
    """Skill management endpoints"""
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class ProjectViewSet(viewsets.ModelViewSet):
    """Project management endpoints"""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class CertificationViewSet(viewsets.ModelViewSet):
    """Certification management endpoints"""
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certification.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class LanguageViewSet(viewsets.ModelViewSet):
    """Language management endpoints"""
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Language.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class AwardViewSet(viewsets.ModelViewSet):
    """Award management endpoints"""
    serializer_class = AwardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Award.objects.filter(cv__user=self.request.user)

    def perform_create(self, serializer):
        cv_id = self.request.data.get('cv')
        cv = get_object_or_404(CV, id=cv_id, user=self.request.user)
        serializer.save(cv=cv)

class EnhancedAICoverLetterViewSet(viewsets.ModelViewSet):
    """Enhanced AI Cover Letter generation endpoints"""
    serializer_class = AICoverLetterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AICoverLetter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def generate_from_cv(self, request):
        """Generate cover letter from CV ID"""
        cv_id = request.data.get('cv_id')
        job_title = request.data.get('job_title')
        job_description = request.data.get('job_description')
        tone = request.data.get('tone', 'professional')
        
        if not all([cv_id, job_title, job_description]):
            return Response(
                {'error': 'cv_id, job_title, and job_description are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cv = get_object_or_404(CV, id=cv_id, user=request.user)
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
            
            serializer = self.get_serializer(ai_cover_letter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {str(e)}")
            return Response(
                {'error': 'Failed to generate cover letter'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def analyze_and_regenerate(self, request, pk=None):
        """Analyze current cover letter and regenerate with improvements"""
        cover_letter = self.get_object()
        
        try:
            service = EnhancedAICoverLetterService()
            
            # Analyze current letter
            analysis = service.analyze_cover_letter(cover_letter.generated_letter)
            
            # Regenerate with improvements
            new_letter = service.regenerate_with_improvements(
                cover_letter.generated_letter,
                analysis
            )
            
            cover_letter.generated_letter = new_letter
            cover_letter.save()
            
            return Response({
                'cover_letter': new_letter,
                'analysis': analysis
            })
            
        except Exception as e:
            logger.error(f"Cover letter analysis failed: {str(e)}")
            return Response(
                {'error': 'Failed to analyze and regenerate cover letter'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _extract_cv_text(self, cv):
        """Extract comprehensive text from CV"""
        text_parts = []
        
        # Personal info
        text_parts.append(f"Name: {cv.full_name}")
        text_parts.append(f"Email: {cv.email}")
        if cv.professional_title:
            text_parts.append(f"Title: {cv.professional_title}")
        
        # Summary
        if cv.summary:
            text_parts.append(f"Summary: {cv.summary}")
        
        # Experience
        experiences = cv.experiences.all()
        if experiences:
            text_parts.append("Experience:")
            for exp in experiences:
                text_parts.append(f"- {exp.job_title} at {exp.company}")
                text_parts.append(f"  {exp.description}")
                if exp.achievements:
                    text_parts.append(f"  Achievements: {', '.join(exp.achievements)}")
        
        # Education
        educations = cv.educations.all()
        if educations:
            text_parts.append("Education:")
            for edu in educations:
                text_parts.append(f"- {edu.degree} from {edu.institution}")
        
        # Skills
        skills = cv.skills.all()
        if skills:
            text_parts.append("Skills:")
            for skill in skills:
                text_parts.append(f"- {skill.name} ({skill.level})")
        
        # Projects
        projects = cv.projects.all()
        if projects:
            text_parts.append("Projects:")
            for proj in projects:
                text_parts.append(f"- {proj.name}: {proj.description}")
                if proj.technologies:
                    text_parts.append(f"  Technologies: {', '.join(proj.technologies)}")
        
        return "\n\n".join(text_parts)

class EnhancedUploadedCVViewSet(viewsets.ModelViewSet):
    """Enhanced uploaded CV management"""
    serializer_class = UploadedCVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedCV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def analyze_cv(self, request, pk=None):
        """Analyze uploaded CV for strengths and improvements"""
        uploaded_cv = self.get_object()
        
        try:
            service = CVAnalysisService()
            analysis = service.analyze_cv(uploaded_cv)
            
            return Response(analysis)
            
        except Exception as e:
            logger.error(f"CV analysis failed: {str(e)}")
            return Response(
                {'error': 'Failed to analyze CV'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EnhancedTemplateViewSet(viewsets.ModelViewSet):
    """Enhanced template management"""
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Template.objects.all()

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get templates by type"""
        template_type = request.query_params.get('type', 'cv')
        templates = self.get_queryset().filter(type=template_type)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_style(self, request):
        """Get templates by style"""
        style = request.query_params.get('style')
        if style:
            templates = self.get_queryset().filter(style=style)
        else:
            templates = self.get_queryset()
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)

class CVAnalysisViewSet(viewsets.ModelViewSet):
    """CV Analysis results endpoints"""
    serializer_class = CVAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CVAnalysis.objects.filter(uploaded_cv__user=self.request.user)
