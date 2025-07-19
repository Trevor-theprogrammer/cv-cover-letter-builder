import os
import io
from typing import Optional
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
import PyPDF2
from docx import Document
import re

class CVFileHandler:
    """Handler for processing uploaded CV files (PDF/DOCX)"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                return text.strip()
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text content from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            return f"Error extracting DOCX text: {str(e)}"
    
    @staticmethod
    def extract_text_from_file(uploaded_file: UploadedFile) -> str:
        """Extract text from uploaded file based on file type"""
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Save file temporarily
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_file.name)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        
        try:
            with open(temp_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            if file_extension == '.pdf':
                text = CVFileHandler.extract_text_from_pdf(temp_file_path)
            elif file_extension in ['.docx', '.doc']:
                text = CVFileHandler.extract_text_from_docx(temp_file_path)
            else:
                text = f"Unsupported file type: {file_extension}"
            
            # Clean up temp file
            os.remove(temp_file_path)
            return text
            
        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return f"Error processing file: {str(e)}"
    
    @staticmethod
    def validate_file_type(file: UploadedFile) -> bool:
        """Validate if the uploaded file is a supported type"""
        allowed_extensions = ['.pdf', '.docx', '.doc']
        file_extension = os.path.splitext(file.name)[1].lower()
        return file_extension in allowed_extensions
    
    @staticmethod
    def get_file_size(file: UploadedFile) -> int:
        """Get file size in bytes"""
        return file.size
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove special characters and spaces
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.lower()

class CVTextProcessor:
    """Processor for cleaning and normalizing extracted CV text"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:@-]', '', text)
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_skills(text: str, common_skills: list = None) -> list:
        """Extract skills from CV text"""
        if common_skills is None:
            common_skills = [
                'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
                'AWS', 'Docker', 'Kubernetes', 'Git', 'Linux', 'Machine Learning',
                'Data Analysis', 'Project Management', 'Agile', 'Scrum', 'Leadership'
            ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
