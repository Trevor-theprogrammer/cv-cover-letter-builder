from .ai_services import CVAnalyzer
from .file_handlers import CVFileHandler, CVTextProcessor
from .models import CVAnalysis, UploadedCV
import logging

logger = logging.getLogger(__name__)

class CVScannerService:
    """Service for scanning and analyzing CVs"""
    
    def __init__(self):
        self.analyzer = CVAnalyzer()
    
    def scan_cv(self, uploaded_cv: UploadedCV, job_description: str = "") -> CVAnalysis:
        """Perform comprehensive CV analysis"""
        
        try:
            # Extract text if not already done
            if not uploaded_cv.extracted_text:
                uploaded_cv.extracted_text = self._extract_text_from_upload(uploaded_cv)
                uploaded_cv.save()
            
            # Clean the text
            clean_text = CVTextProcessor.clean_text(uploaded_cv.extracted_text)
            
            # Perform AI analysis
            analysis_result = self.analyzer.analyze_cv(clean_text, job_description)
            
            # Create or update analysis record
            analysis, created = CVAnalysis.objects.get_or_create(
                uploaded_cv=uploaded_cv,
                defaults={
                    'overall_score': analysis_result.get('overall_score', 0),
                    'strengths': analysis_result.get('strengths', []),
                    'improvements': analysis_result.get('improvements', []),
                    'keywords': analysis_result.get('keywords', {}),
                    'experience_level': analysis_result.get('experience_level', 'Unknown'),
                    'ats_compatibility': analysis_result.get('ats_compatibility', 0)
                }
            )
            
            if not created:
                # Update existing analysis
                analysis.overall_score = analysis_result.get('overall_score', 0)
                analysis.strengths = analysis_result.get('strengths', [])
                analysis.improvements = analysis_result.get('improvements', [])
                analysis.keywords = analysis_result.get('keywords', {})
                analysis.experience_level = analysis_result.get('experience_level', 'Unknown')
                analysis.ats_compatibility = analysis_result.get('ats_compatibility', 0)
                analysis.save()
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error scanning CV: {str(e)}")
            # Return basic analysis on error
            return CVAnalysis.objects.create(
                uploaded_cv=uploaded_cv,
                overall_score=0,
                strengths=["CV uploaded successfully"],
                improvements=["Analysis temporarily unavailable"],
                keywords={"present": [], "missing": [], "suggestions": []},
                experience_level="Unknown",
                ats_compatibility=0
            )
    
    def _extract_text_from_upload(self, uploaded_cv: UploadedCV) -> str:
        """Extract text from uploaded CV file"""
        try:
            file_path = uploaded_cv.file.path
            file_extension = uploaded_cv.original_filename.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                return CVFileHandler.extract_text_from_pdf(file_path)
            elif file_extension in ['docx', 'doc']:
                return CVFileHandler.extract_text_from_docx(file_path)
            else:
                return "Unsupported file format"
                
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return "Error extracting text from file"
    
    def get_improvement_suggestions(self, analysis: CVAnalysis) -> list:
        """Get actionable improvement suggestions"""
        suggestions = []
        
        if analysis.overall_score < 70:
            suggestions.append("Consider adding more relevant keywords from job descriptions")
        
        if analysis.ats_compatibility < 80:
            suggestions.append("Improve ATS compatibility by using standard formatting and keywords")
        
        if analysis.experience_level == "Entry Level" and analysis.overall_score < 60:
            suggestions.append("Add more quantifiable achievements and specific examples")
        
        # Add suggestions based on missing keywords
        keywords = analysis.keywords
        if 'missing' in keywords and keywords['missing']:
            suggestions.append(f"Consider adding these keywords: {', '.join(keywords['missing'][:5])}")
        
        return suggestions
    
    def generate_score_breakdown(self, analysis: CVAnalysis) -> dict:
        """Generate detailed score breakdown"""
        return {
            'overall_score': analysis.overall_score,
            'experience_level': analysis.experience_level,
            'ats_compatibility': analysis.ats_compatibility,
            'strengths_count': len(analysis.strengths),
            'improvements_count': len(analysis.improvements),
            'keywords_score': len(analysis.keywords.get('present', [])) * 2,
            'grade': self._get_grade(analysis.overall_score)
        }
    
    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"
