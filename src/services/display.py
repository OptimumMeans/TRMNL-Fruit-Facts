from PIL import Image, ImageDraw, ImageFont
import io
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class DisplayGenerator:
    '''Service for generating e-ink display images.'''
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        try:
            self.font = ImageFont.truetype(font='arial.ttf', size=16)
        except Exception as e:
            logger.warning(f'Failed to load TrueType font: {e}')
            self.font = ImageFont.load_default()
    
    def create_display(self, data: Dict[str, Any]) -> Optional[bytes]:
        '''Create a display image for the TRMNL e-ink display.'''
        try:
            image = Image.new('1', (self.width, self.height), 1)
            draw = ImageDraw.Draw(image)
            
            if not data:
                return self.create_error_display('No data available')
            
            # Draw your content here
            self._draw_content(draw, data)
            self._draw_status_bar(draw, data)
            
            buffer = io.BytesIO()
            image.save(buffer, format='BMP')
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f'Error generating display: {str(e)}')
            return self.create_error_display(str(e))
    
    def create_error_display(self, error_message: str) -> bytes:
        '''Create an error display.'''
        image = Image.new('1', (self.width, self.height), 1)
        draw = ImageDraw.Draw(image)
        
        draw.text(
            (20, 20),
            'Error',
            font=self.font,
            fill=0
        )
        
        draw.text(
            (20, 50),
            error_message,
            font=self.font,
            fill=0
        )
        
        buffer = io.BytesIO()
        image.save(buffer, format='BMP')
        return buffer.getvalue()
    
    def _draw_content(self, draw: ImageDraw, data: Dict[str, Any]) -> None:
        '''Draw the main content of the display.'''
        # Implement your display logic here
        pass
    
    def _draw_status_bar(self, draw: ImageDraw, data: Dict[str, Any]) -> None:
        '''Draw a status bar at the bottom of the display.'''
        draw.rectangle(
            [0, self.height-30, self.width, self.height],
            fill=0
        )
        
        status_text = f'Last Update: {data.get('timestamp', 'Unknown')}'
        draw.text(
            (10, self.height-25),
            status_text,
            font=self.font,
            fill=1
        )
