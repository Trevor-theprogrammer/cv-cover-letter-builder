from django.contrib import admin
from .models import (
    CV, Experience, Education, Skill, Project, Certification, 
    Language, Award, UploadedCV, AICoverLetter, CVAnalysis, Template
)

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'completion_percentage', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at', 'template']
    search_fields = ['full_name', 'email', 'user__username']
    readonly_fields = ['completion_percentage', 'created_at', 'updated_at']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'cv', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['job_title', 'company', 'cv__full_name']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'cv', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['degree', 'institution', 'cv__full_name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'cv', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['name', 'cv__full_name']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'style', 'is_default', 'created_at']
    list_filter = ['type', 'style', 'is_default']
    search_fields = ['name', 'description']

admin.site.register(Skill)
admin.site.register(Certification)
admin.site.register(Language)
admin.site.register(Award)
admin.site.register(UploadedCV)
admin.site.register(AICoverLetter)
admin.site.register(CVAnalysis)
