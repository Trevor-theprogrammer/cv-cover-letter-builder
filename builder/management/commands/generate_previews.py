"""
Django management command to generate template previews.
Supports multiple viewport sizes and custom configurations.
"""
from django.core.management.base import BaseCommand
from scripts.generate_template_previews import capture_template_previews, ViewportSize

class Command(BaseCommand):
    help = 'Generate preview images for CV templates at various viewport sizes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            default='http://localhost:8000',
            help='Base URL of the application'
        )
        parser.add_argument(
            '--viewports',
            nargs='+',
            help='List of viewport sizes to generate (desktop, tablet, mobile)'
        )
        parser.add_argument(
            '--custom-viewport',
            nargs=3,
            metavar=('NAME', 'WIDTH', 'HEIGHT'),
            help='Custom viewport size (e.g., "large 1440 900")'
        )
        parser.add_argument(
            '--formats',
            nargs='+',
            choices=['png', 'jpg', 'webp'],
            default=['png'],
            help='Image formats to generate (png, jpg, webp)'
        )
        parser.add_argument(
            '--templates',
            nargs='+',
            choices=['modern', 'classic', 'minimal', 'creative'],
            help='Specific templates to generate (default: all)'
        )

    def handle(self, *args, **options):
        viewport_sizes = None

        if options['custom_viewport']:
            name, width, height = options['custom_viewport']
            viewport_sizes = [ViewportSize(name, int(width), int(height))]
        elif options['viewports']:
            viewport_map = {
                'desktop': ViewportSize('desktop', 1200, 1600),
                'tablet': ViewportSize('tablet', 768, 1024),
                'mobile': ViewportSize('mobile', 375, 812),
            }
            viewport_sizes = [viewport_map[v] for v in options['viewports'] if v in viewport_map]

        try:
            self.stdout.write('Generating template previews...')
            capture_template_previews(
                base_url=options['url'],
                viewport_sizes=viewport_sizes
            )
            self.stdout.write(self.style.SUCCESS(
                'Successfully generated template previews'
                + (f' for viewports: {", ".join(options["viewports"])}' if options['viewports'] else '')
                + (f' at custom size: {options["custom_viewport"][0]}' if options['custom_viewport'] else '')
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating previews: {str(e)}'))
