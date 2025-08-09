"""
Script to automatically generate template preview images using Selenium.
Supports multiple viewport sizes and formats for responsive design.
"""
import os
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from django.conf import settings
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ViewportSize:
    """Represents a viewport size configuration"""
    name: str
    width: int
    height: int

    def __str__(self) -> str:
        return f"{self.name}_{self.width}x{self.height}"

class TemplatePreviewGenerator:
    """Handles generation of template preview images"""
    
    # Default viewport sizes
    VIEWPORT_SIZES = [
        ViewportSize("desktop", 1200, 1600),
        ViewportSize("tablet", 768, 1024),
        ViewportSize("mobile", 375, 812),
    ]
    
    # Supported image formats
    IMAGE_FORMATS = {
        'png': {'ext': 'png', 'mime': 'image/png'},
        'jpg': {'ext': 'jpg', 'mime': 'image/jpeg', 'quality': 95},
        'webp': {'ext': 'webp', 'mime': 'image/webp', 'quality': 90},
    }
    
    # Template configurations
    TEMPLATES = [
        {"name": "modern", "title": "Modern Template"},
        {"name": "classic", "title": "Classic Template"},
        {"name": "minimal", "title": "Minimal Template"},
        {"name": "creative", "title": "Creative Template"},
    ]

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.driver = None
        self.templates_dir = os.path.join(settings.BASE_DIR, "builder", "static", 
                                        "builder", "images", "templates")
        os.makedirs(self.templates_dir, exist_ok=True)

    def setup_driver(self, viewport: ViewportSize) -> None:
        """Setup Chrome driver with specific viewport size"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size={viewport.width},{viewport.height}")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--force-device-scale-factor=1")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_window_size(viewport.width, viewport.height)

    def wait_for_template(self, template_class: str, timeout: int = 10) -> Optional[webdriver.Remote]:
        """Wait for template element to be visible and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, f"{template_class}-preview"))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for template: {template_class}")
            return None

    def capture_template(self, template: Dict[str, str], viewport: ViewportSize, 
                         formats: List[str] = None) -> bool:
        """Capture screenshot of a specific template in specified formats"""
        try:
            template_element = self.wait_for_template(template["name"])
            if not template_element:
                return False

            # Scroll to template and wait for any animations
            self.driver.execute_script("arguments[0].scrollIntoView(true);", template_element)
            time.sleep(0.5)

            # Get PNG screenshot as bytes
            png_data = template_element.screenshot_as_png
            image = Image.open(io.BytesIO(png_data))

            # Save in each requested format
            formats = formats or ['png']  # Default to PNG if no formats specified
            for fmt in formats:
                if fmt not in self.IMAGE_FORMATS:
                    logger.warning(f"Unsupported format: {fmt}, skipping...")
                    continue

                format_config = self.IMAGE_FORMATS[fmt]
                filename = f"{template['name']}-template_{viewport}.{format_config['ext']}"
                filepath = os.path.join(self.templates_dir, filename)

                # Save with format-specific settings
                save_kwargs = {}
                if 'quality' in format_config:
                    save_kwargs['quality'] = format_config['quality']
                
                image.save(filepath, format=fmt.upper(), **save_kwargs)
                logger.info(f"Generated {viewport.name} preview for {template['name']} "
                          f"template in {fmt.upper()} format")

            return True

        except WebDriverException as e:
            logger.error(f"Error capturing {template['name']} template: {str(e)}")
            return False

    def generate_previews(self, viewport_sizes: Optional[List[ViewportSize]] = None) -> None:
        """Generate preview images for all templates at specified viewport sizes"""
        viewport_sizes = viewport_sizes or self.VIEWPORT_SIZES
        
        for viewport in viewport_sizes:
            try:
                self.setup_driver(viewport)
                logger.info(f"Generating {viewport.name} previews...")
                
                # Navigate to preview page
                self.driver.get(f"{self.base_url}/template-previews/")
                
                # Capture each template
                for template in self.TEMPLATES:
                    self.capture_template(template, viewport)
                    
            except Exception as e:
                logger.error(f"Error generating {viewport.name} previews: {str(e)}")
            finally:
                if self.driver:
                    self.driver.quit()

def capture_template_previews(base_url: str = "http://localhost:8000",
                            viewport_sizes: Optional[List[ViewportSize]] = None) -> None:
    """Main function to capture all template previews"""
    try:
        generator = TemplatePreviewGenerator(base_url)
        generator.generate_previews(viewport_sizes)
        logger.info("Template preview generation completed successfully")
    except Exception as e:
        logger.error(f"Fatal error during preview generation: {str(e)}")
        raise

if __name__ == "__main__":
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    capture_template_previews()
