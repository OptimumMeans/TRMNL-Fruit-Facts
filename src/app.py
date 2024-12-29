from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime, UTC
import traceback
import os
import webbrowser
from threading import Timer

from .config import Config
from .services.display import DisplayGenerator
from .services.api_service import APIService
from .utils.formatters import format_timestamp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
Config.validate()
api_service = APIService()
display_generator = DisplayGenerator(Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT)

@app.route('/')
def home():
    """Home endpoint with plugin information."""
    # Check if it's a browser request
    if request.headers.get('Accept', '').find('text/html') != -1:
        # Redirect browser requests to webhook
        return f'''
        <html>
            <head>
                <meta http-equiv="refresh" content="0;url=/webhook">
            </head>
            <body>
                Redirecting to webhook...
            </body>
        </html>
        '''
    
    return jsonify({
        'name': 'TRMNL Fruit Facts',
        'description': 'Displays fruit nutritional facts and information',
        'version': '1.0.0',
        'status': 'running',
        'last_update': api_service.last_update.isoformat() if api_service.last_update else None,
        'refresh_interval': Config.REFRESH_INTERVAL,
        'rotation_interval': Config.FRUIT_ROTATION_INTERVAL,
        'fruits_loaded': len(api_service._all_fruits) if api_service._all_fruits else 0
    })

@app.route('/webhook', methods=['GET'])
def trmnl_webhook():
    """Main webhook endpoint for TRMNL device."""
    try:
        # Get fruit data
        data = api_service.get_data()
        if not data:
            raise Exception("Failed to fetch fruit data")
        
        logger.info(
            f"Serving fruit: {data['fruit']['name']} "
            f"({data['current_index'] + 1}/{data['total_fruits']})"
        )
        
        # Generate display image
        image_data = display_generator.create_display(data)
        
        # Calculate next refresh based on rotation interval
        next_refresh = min(Config.REFRESH_INTERVAL, Config.FRUIT_ROTATION_INTERVAL)
        
        # Set up response
        response = Response(
            image_data,
            mimetype='image/bmp',
            headers={
                'X-TRMNL-Refresh': str(next_refresh),
                'X-TRMNL-Plugin-UUID': Config.TRMNL_PLUGIN_UUID,
                'Content-Type': 'image/bmp'
            }
        )
        
        # Ensure no caching
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        logger.error(f'Webhook error: {str(e)}')
        logger.error(traceback.format_exc())
        
        # Create error display
        error_display = display_generator.create_error_display(
            f"Error: {str(e)}\nPlease check logs or try again later."
        )
        
        return Response(
            error_display,
            mimetype='image/bmp',
            headers={
                'X-TRMNL-Refresh': '300',  # Retry in 5 minutes on error
                'X-TRMNL-Plugin-UUID': Config.TRMNL_PLUGIN_UUID,
                'Content-Type': 'image/bmp'
            }
        )

if __name__ == '__main__':
    print('=' * 80)
    print('TRMNL Fruit Facts Plugin')
    print('=' * 80)
    print(f'Server URL: http://{Config.HOST}:{Config.PORT}')
    print('-' * 80)
    print('Press Ctrl+C to quit')
    print('=' * 80)
    
    # Open browser at startup
    if Config.HOST == 'localhost':
        Timer(1.5, lambda: webbrowser.open(f'http://{Config.HOST}:{Config.PORT}/webhook')).start()
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )