import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    '''Application configuration.'''
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Plugin Configuration
    REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '900'))
    
    # TRMNL Configuration
    TRMNL_API_KEY = os.getenv('TRMNL_API_KEY')
    TRMNL_PLUGIN_UUID = os.getenv('TRMNL_PLUGIN_UUID')
    
    # Display Configuration
    DISPLAY_WIDTH = int(os.getenv('DISPLAY_WIDTH', '800'))
    DISPLAY_HEIGHT = int(os.getenv('DISPLAY_HEIGHT', '480'))
    
    # Cache Configuration
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '600'))
    
    @classmethod
    def validate(cls):
        '''Validate required configuration.'''
        required_keys = [
            'TRMNL_API_KEY',
            'TRMNL_PLUGIN_UUID'
        ]
        
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_keys)}"
            )
