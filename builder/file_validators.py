import magic
import tempfile
import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

class FileValidator:
    """Secure file validation using python-magic for MIME type detection"""
    
    ALLOWED_MIME_TYPES = {
        'application/pdf': ['.pdf'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/msword': ['.doc'],
        'text/plain': ['.txt'],
    }
    
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    @classmethod
    def validate_file(cls, uploaded_file: UploadedFile) -> None:
        """
        Validate uploaded file for security and type compatibility
        
        Args:
            uploaded_file: Django UploadedFile instance
            
        Raises:
            ValidationError: If file validation fails
        """
        # Check file size
        if uploaded_file.size > cls.MAX_FILE_SIZE:
            raise ValidationError(f"File size exceeds maximum limit of {cls.MAX_FILE_SIZE // (1024*1024)}MB")
        
        # Check if file is empty
        if uploaded_file.size == 0:
            raise ValidationError("Empty file is not allowed")
        
        # Create temporary file to check MIME type
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            try:
                # Write uploaded file content to temporary file
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                
                # Reset file pointer for later use
                uploaded_file.seek(0)
                
                # Check MIME type using python-magic
                actual_mime_type = magic.from_file(tmp_file.name, mime=True)
                
                if actual_mime_type not in cls.ALLOWED_MIME_TYPES:
                    raise ValidationError(f"File type '{actual_mime_type}' is not supported")
                
                # Verify file extension matches MIME type
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                allowed_extensions = cls.ALLOWED_MIME_TYPES[actual_mime_type]
                
                if file_extension not in allowed_extensions:
                    raise ValidationError(
                        f"File extension '{file_extension}' doesn't match file type '{actual_mime_type}'"
                    )
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_file.name)
                except OSError:
                    pass  # File already deleted or doesn't exist
    
    @classmethod
    def get_file_type(cls, uploaded_file: UploadedFile) -> str:
        """
        Get the actual MIME type of uploaded file
        
        Args:
            uploaded_file: Django UploadedFile instance
            
        Returns:
            str: MIME type of the file
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            try:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                
                uploaded_file.seek(0)  # Reset file pointer
                return magic.from_file(tmp_file.name, mime=True)
                
            finally:
                try:
                    os.unlink(tmp_file.name)
                except OSError:
                    pass
