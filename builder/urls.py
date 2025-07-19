from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cv/', views.create_cv, name='create_cv'),
    path('cv/<int:pk>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:pk>/add_section/', views.add_cv_section, name='add_cv_section'),
    path('cv/<int:pk>/edit_section/', views.edit_cv_section, name='edit_cv_section'),
    path('cv/<int:pk>/delete_cv_section/', views.delete_cv_section, name='delete_cv_section'),
    path('generate_cover_letter/', views.generate_cover_letter, name='generate_cover_letter'),
    path('register/', views.register, name='register'),
    
    # New AI-powered features
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('ai-cover-letter/', views.ai_cover_letter, name='ai_cover_letter'),
    path('cv-analyzer/', views.cv_analyzer, name='cv_analyzer'),
    path('templates/', views.templates, name='templates'),
    path('template/<int:pk>/', views.template_detail, name='template_detail'),
    path('template/create/', views.create_template, name='create_template'),
    path('template/<int:pk>/edit/', views.edit_template, name='edit_template'),
    
    # Delete endpoints
    path('cv/<int:pk>/delete/', views.delete_cv, name='delete_cv'),
    path('uploaded-cv/<uuid:pk>/delete/', views.delete_uploaded_cv, name='delete_uploaded_cv'),
]
