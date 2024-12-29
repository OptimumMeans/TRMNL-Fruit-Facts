import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    '''Application configuration.'''
    
    # Development Mode
    DEV_MODE = os.getenv('DEV_MODE', 'True').lower() == 'true'
    
    # Server Configuration
    HOST = os.getenv('HOST', 'localhost')  # Changed from 0.0.0.0 to localhost
    PORT = int(os.getenv('PORT', 5000))    # Changed from 8080 to 5000
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Plugin Configuration
    REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '3600'))  # 1 hour default
    FRUIT_ROTATION_INTERVAL = int(os.getenv('FRUIT_ROTATION_INTERVAL', '86400'))  # 24 hours default
    
    # TRMNL Configuration
    TRMNL_API_KEY = os.getenv('TRMNL_API_KEY', 'dev-key' if DEV_MODE else None)
    TRMNL_PLUGIN_UUID = os.getenv('TRMNL_PLUGIN_UUID', 'dev-uuid' if DEV_MODE else None)
    
    # Display Configuration
    DISPLAY_WIDTH = int(os.getenv('DISPLAY_WIDTH', '800'))
    DISPLAY_HEIGHT = int(os.getenv('DISPLAY_HEIGHT', '480'))
    
    # Cache Configuration
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '3600'))  # 1 hour cache
    
    # Fruityvice API Configuration
    FRUITYVICE_API_URL = 'https://fruityvice.com/api/fruit'
    
    # Display Layout Configuration
    LAYOUT_CONFIG = {
        'HEADER_HEIGHT': 80,
        'FOOTER_HEIGHT': 40,
        'PADDING': 20,
        'GRID_COLUMNS': 2,
        'NUTRITION_BOX_HEIGHT': 200
    }
    
    @classmethod
    def validate(cls):
        '''Validate required configuration.'''
        if cls.DEV_MODE:
            return  # Skip validation in development mode
            
        required_keys = [
            'TRMNL_API_KEY',
            'TRMNL_PLUGIN_UUID'
        ]
        
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_keys)}"
            )

    @classmethod
    def get_layout_dimensions(cls):
        '''Get usable content area dimensions.'''
        return {
            'content_width': cls.DISPLAY_WIDTH - (2 * cls.LAYOUT_CONFIG['PADDING']),
            'content_height': (
                cls.DISPLAY_HEIGHT - 
                cls.LAYOUT_CONFIG['HEADER_HEIGHT'] - 
                cls.LAYOUT_CONFIG['FOOTER_HEIGHT'] - 
                (2 * cls.LAYOUT_CONFIG['PADDING'])
            )
        }