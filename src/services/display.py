from PIL import Image, ImageDraw, ImageFont
import io
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class DisplayGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        try:
            self.title_font = ImageFont.truetype('arial.ttf', size=48)
            self.heading_font = ImageFont.truetype('arial.ttf', size=32)
            self.body_font = ImageFont.truetype('arial.ttf', size=24)
            self.small_font = ImageFont.truetype('arial.ttf', size=16)
        except Exception as e:
            logger.warning(f'Failed to load TrueType fonts: {e}')
            self.title_font = ImageFont.load_default()
            self.heading_font = ImageFont.load_default()
            self.body_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

    def create_display(self, data: Dict[str, Any]) -> Optional[bytes]:
        '''Create a display image for the TRMNL e-ink display.'''
        try:
            if not data or 'fruit' not in data:
                return self.create_error_display('No fruit data available')

            fruit = data['fruit']
            image = Image.new('1', (self.width, self.height), 1)  # White background
            draw = ImageDraw.Draw(image)

            # Draw main sections
            self._draw_header(draw, fruit)
            self._draw_nutrition_panel(draw, fruit['nutritions'])
            self._draw_taxonomy_panel(draw, fruit)
            self._draw_status_bar(draw, data)

            buffer = io.BytesIO()
            image.save(buffer, format='BMP')
            return buffer.getvalue()

        except Exception as e:
            logger.error(f'Error generating display: {str(e)}')
            return self.create_error_display(str(e))

    def _draw_header(self, draw: ImageDraw, fruit: Dict[str, Any]) -> None:
        '''Draw the fruit name and header section.'''
        # Draw title box
        draw.rectangle([0, 0, self.width, 80], fill=0)  # Black background
        
        # Draw fruit name
        name = fruit['name'].upper()
        bbox = draw.textbbox((0, 0), name, font=self.title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 20), name, font=self.title_font, fill=1)  # White text

    def _draw_nutrition_panel(self, draw: ImageDraw, nutrition: Dict[str, Any]) -> None:
        '''Draw the nutritional information panel.'''
        start_y = 100
        items = [
            ('Calories', f"{nutrition['calories']} kcal"),
            ('Carbohydrates', f"{nutrition['carbohydrates']}g"),
            ('Protein', f"{nutrition['protein']}g"),
            ('Fat', f"{nutrition['fat']}g"),
            ('Sugar', f"{nutrition['sugar']}g")
        ]

        # Draw panel border
        panel_width = (self.width // 2) - 30
        draw.rectangle([20, start_y, panel_width + 20, start_y + 200], outline=0, width=1)
        
        # Draw "Nutrition Facts" header
        draw.text((30, start_y + 10), "Nutrition Facts", font=self.heading_font, fill=0)
        
        # Draw nutrition items
        y = start_y + 50
        for label, value in items:
            draw.text((40, y), label, font=self.body_font, fill=0)
            draw.text((panel_width - 100, y), value, font=self.body_font, fill=0)
            y += 30

    def _draw_taxonomy_panel(self, draw: ImageDraw, fruit: Dict[str, Any]) -> None:
        '''Draw the taxonomic classification panel.'''
        start_y = 100
        start_x = (self.width // 2) + 10
        panel_width = (self.width // 2) - 30
        
        # Draw panel border
        draw.rectangle(
            [start_x, start_y, start_x + panel_width, start_y + 200],
            outline=0,
            width=1
        )
        
        # Draw "Classification" header
        draw.text(
            (start_x + 10, start_y + 10),
            "Classification",
            font=self.heading_font,
            fill=0
        )
        
        # Draw taxonomy items
        items = [
            ('Family', fruit['family']),
            ('Order', fruit['order']),
            ('Genus', fruit['genus'])
        ]
        
        y = start_y + 50
        for label, value in items:
            draw.text((start_x + 20, y), label, font=self.body_font, fill=0)
            draw.text((start_x + 120, y), value, font=self.body_font, fill=0)
            y += 30

    def _draw_status_bar(self, draw: ImageDraw, data: Dict[str, Any]) -> None:
        '''Draw status bar at the bottom.'''
        status_height = 30
        bar_y = self.height - status_height - 10
        
        # Draw status bar background
        draw.rectangle(
            [0, bar_y, self.width, bar_y + status_height],
            fill=0
        )
        
        # Format timestamp
        timestamp = data.get('timestamp', 'Unknown')
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%Y-%m-%d %H:%M UTC')
            except ValueError:
                pass
        
        # Draw timestamp and fruit count
        status_text = f'Last Update: {timestamp}'
        fruit_count = f'Fruit {data.get("current_index", 0) + 1} of {data.get("total_fruits", 0)}'
        
        draw.text((10, bar_y + 5), status_text, font=self.small_font, fill=1)
        
        count_bbox = draw.textbbox((0, 0), fruit_count, font=self.small_font)
        count_width = count_bbox[2] - count_bbox[0]
        draw.text(
            (self.width - count_width - 10, bar_y + 5),
            fruit_count,
            font=self.small_font,
            fill=1
        )

    def create_error_display(self, error_message: str) -> bytes:
        '''Create an error display.'''
        image = Image.new('1', (self.width, self.height), 1)
        draw = ImageDraw.Draw(image)
        
        draw.text(
            (20, 20),
            'Error',
            font=self.heading_font,
            fill=0
        )
        
        draw.text(
            (20, 60),
            error_message,
            font=self.body_font,
            fill=0
        )
        
        buffer = io.BytesIO()
        image.save(buffer, format='BMP')
        return buffer.getvalue()