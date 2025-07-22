import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import UploadedCVForm
from .models import UploadedCV, CVAnalysis
from .ai_services import EnhancedAICoverLetterService

logger = logging.getLogger(__name__)

@login_required
def upload_cv_optimized(request):
    """Optimized upload CV view with integrated analysis"""
    from .forms import UploadedCVForm
    
    if request.method == 'POST':
        form = UploadedCVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_cv = form.save(commit=False)
                uploaded_cv.user = request.user
                
                # Process the uploaded file
                uploaded_file = request.FILES['file']
                uploaded_cv.original_filename = uploaded_file.name
                
                # Validate file security
                from .file_validators import FileValidator
                try:
                    FileValidator.validate_file(uploaded_file)
                    actual_mime_type = FileValidator.get_file_type(uploaded_file)
                except ValidationError as e:
                    messages.error(request, f"File validation failed: {str(e)}")
                    return render(request, 'builder/upload_cv_enhanced.html', {'form': form})
                
                # Fast text extraction with error handling
                cv_text = ""
                try:
                    if actual_mime_type == 'application/pdf':
                        try:
                            import PyPDF2
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                            cv_text = text[:3000] if text.strip() else "No text found in PDF"
                        except Exception as pdf_error:
                            logger.error(f"PDF extraction failed: {str(pdf_error)}")
                            cv_text = "PDF text extraction failed"
                            
                    elif actual_mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                        try:
                            import docx
                            doc = docx.Document(uploaded_file)
                            text = ""
                            for paragraph in doc.paragraphs:
                                text += paragraph.text + "\n"
                            cv_text = text[:3000] if text.strip() else "No text found in document"
                        except Exception as docx_error:
                            logger.error(f"DOCX extraction failed: {str(docx_error)}")
                            cv_text = "Document text extraction failed"
                    else:
                        cv_text = "Text extraction not supported for this format"
                        
                    uploaded_cv.extracted_text = cv_text
                    uploaded_cv.processed = True
                    uploaded_cv.save()
                    
                    # Fast AI analysis
                    service = EnhancedAICoverLetterService()
                    
                    # Quick analysis for faster results
                    quick_analysis = service.quick_cv_analysis(cv_text)
                    
                    # Create CV analysis
                    cv_analysis = CVAnalysis.objects.create(
                        uploaded_cv=uploaded_cv,
                        overall_score=quick_analysis.get('overall_score', 75),
                        strengths=quick_analysis.get('strengths', ['Good structure', 'Clear formatting']),
                        improvements=quick_analysis.get('improvements', ['Add more keywords', 'Include metrics']),
                        keywords=quick_analysis.get('keywords', {'present': [], 'missing': []}),
                        experience_level=quick_analysis.get('experience_level', 'Mid-level'),
                        ats_compatibility=quick_analysis.get('ats_compatibility', 80)
                    )
                    
                    return render(request, 'builder/upload_cv_enhanced.html', {
                        'analysis': quick_analysis,
                        'uploaded_cv': uploaded_cv,
                        'cv_analysis': cv_analysis,
                        'form': form
                    })
                    
                except Exception as e:
                    logger.error(f"File processing failed: {str(e)}")
                    uploaded_cv.extracted_text = f"Error processing file: {str(e)}"
                    uploaded_cv.save()
                    
            except Exception as e:
                logger.error(f"Upload failed: {str(e)}")
                return render(request, 'builder/upload_cv_enhanced.html', {
                    'form': form,
                    'error': 'Upload failed. Please try again.'
                })
    else:
        form = UploadedCVForm()
    
    return render(request, 'builder/upload_cv_enhanced.html', {'form': form})
