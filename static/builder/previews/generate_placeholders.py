"""
Script to generate placeholder template preview images
Run this to create basic placeholder images for templates
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Template names from views_cv_builder.py
templates = ['modern', 'creative', 'minimal', 'classic', 'basic']

# Create directory if it doesn't exist
os.makedirs('static/builder/previews', exist_ok=True)

# Generate placeholder images
for template_name in templates:
    # Create a 300x424 image (A4 aspect ratio)
    img = Image.new('RGB', (300, 424), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Add template name
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Center text
    text = template_name.title()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (300 - text_width) // 2
    y = (424 - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='#2563eb', font=font)
    
    # Save image
    img.save(f'static/builder/previews/{template_name}.png')

print("Generated placeholder template preview images")
