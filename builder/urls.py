from django.urls import path
from . import views

app_name = 'builder'

urlpatterns = [
    path('template-previews/', views.template_previews, name='template_previews'),
    path('templates/<str:template_name>-preview/', views.template_preview, name='template_preview'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cv/', views.create_cv, name='create_cv'),
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
    path('cover-letter-templates/', views.cover_letter_templates, name='cover_letter_templates'),
    path('cv-analyzer/', views.cv_analyzer, name='cv_analyzer'),
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
