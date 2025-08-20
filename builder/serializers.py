from rest_framework import serializers
from .models import (
    CV, Experience, Education, Skill, Project, Certification, 
    Language, Award, AICoverLetter, UploadedCV, Template, CVAnalysis
)

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('cv',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('cv',)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ('cv',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('cv',)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('cv',)

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ('cv',)

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'
        read_only_fields = ('cv',)

class CVSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)

    class Meta:
        model = CV
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'completion_percentage')

class AICoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICoverLetter
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class UploadedCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedCV
        fields = '__all__'
        read_only_fields = ('user', 'uploaded_at')

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

class CVAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVAnalysis
        fields = '__all__'
        read_only_fields = ('uploaded_cv', 'created_at')
