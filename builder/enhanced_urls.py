from django.urls import path
from . import enhanced_views

urlpatterns = [
    path('enhanced-ai-cover-letter/', enhanced_views.enhanced_ai_cover_letter, name='enhanced_ai_cover_letter'),
    path('preview-cover-letter/', enhanced_views.preview_cover_letter, name='preview_cover_letter'),
    path('edit-generated-letter/<uuid:pk>/', enhanced_views.edit_generated_letter, name='edit_generated_letter'),
    path('cv-analysis-detail/<uuid:pk>/', enhanced_views.cv_analysis_detail, name='cv_analysis_detail'),
    path('ajax-generate-cover-letter/', enhanced_views.ajax_generate_cover_letter, name='ajax_generate_cover_letter'),
    path('cover-letter-templates/', enhanced_views.cover_letter_templates, name='cover_letter_templates'),
    path('use-template/<int:template_id>/', enhanced_views.use_template, name='use_template'),
]
