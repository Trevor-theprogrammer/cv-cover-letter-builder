from django.urls import path
from . import views
from .views_cv_builder import create_cv
from .views_template_preview import template_preview
from .views_cv_editor import edit_cv_template, save_cv_draft

app_name = 'builder'

urlpatterns = [
    path('template-previews/', views.template_previews, name='template_previews'),
    path('templates/<str:template_id>/', template_preview, name='template_preview'),
    path('cv/<str:template_id>/edit/', edit_cv_template, name='edit_cv'),
    path('cv/save-draft/', save_cv_draft, name='save_cv_draft'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cv/create/', create_cv, name='create_cv'),  # Updated path for new CV builder
    path('cv/<int:pk>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:pk>/add_section/', views.add_cv_section, name='add_cv_section'),
    path('cv/<int:pk>/edit_section/', views.edit_cv_section, name='edit_cv_section'),
    path('cv/<int:pk>/delete_cv_section/', views.delete_cv_section, name='delete_cv_section'),
    path('cover-letter/', views.enhanced_ai_cover_letter, name='generate_cover_letter'),
    path('register/', views.register, name='register'),
    
    # New AI-powered features
    path('upload-cv/', views.upload_cv_analyzer, name='upload_cv'),
    path('upload-cv-enhanced/', views.upload_cv, name='upload_cv_enhanced'),
    path('ai-cover-letter/', views.ai_cover_letter, name='ai_cover_letter'),
    path('templates/', views.templates, name='templates'),
    path('templates/<str:template_name>/', views.load_cv_template, name='load_template'),
    path('cover-letter-templates/', views.cover_letter_templates, name='cover_letter_templates'),
    path('cv-analyzer/', views.cv_analyzer, name='cv_analyzer'),
    path('cv/template/<str:template_name>/', views.load_cv_template, name='load_cv_template'),
    path('cv/save/', views.save_cv_content, name='save_cv_content'),
    path('template/<int:pk>/', views.template_detail, name='template_detail'),
    path('template/create/', views.create_template, name='create_template'),
    path('template/<int:pk>/edit/', views.edit_template, name='edit_template'),
    
    # Enhanced AI features
    path('enhanced-ai-cover-letter/', views.enhanced_ai_cover_letter, name='enhanced_ai_cover_letter'),
    path('ajax/generate-cover-letter/', views.ajax_generate_cover_letter, name='ajax_generate_cover_letter'),
    path('edit-letter/<uuid:pk>/', views.edit_generated_letter, name='edit_generated_letter'),
    path('cv-analysis/<int:pk>/', views.cv_analysis_detail, name='cv_analysis_detail'),
    
    # Delete endpoints
    path('cv/<int:pk>/delete/', views.delete_cv, name='delete_cv'),
    path('uploaded-cv/<uuid:pk>/delete/', views.delete_uploaded_cv, name='delete_uploaded_cv'),
]
