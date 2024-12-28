from flask import Flask, Response, jsonify
from flask_cors import CORS
import logging
from datetime import datetime, UTC
import traceback
import os

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
api_service = APIService()
display_generator = DisplayGenerator(Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT)

@app.route('/')
def home():
    '''Root route that explains the API.'''
    return jsonify({
        'name': 'TRMNL Plugin',
        'description': 'TRMNL Plugin Boilerplate',
        'version': '1.0.0',
        'status': 'running',
        'last_update': api_service.last_update.isoformat() if api_service.last_update else None,
        'refresh_interval': Config.REFRESH_INTERVAL
    })

@app.route('/webhook', methods=['GET'])
def trmnl_webhook():
    '''Main webhook endpoint for TRMNL.'''
    try:
        # Get data from your service
        data = api_service.get_data()
        logger.info(f'Data retrieved: {data}')
        
        # Generate display
        image_data = display_generator.create_display(data)
        
        # Return binary image with TRMNL headers
        return Response(
            image_data,
            mimetype='image/bmp',
            headers={
                'X-TRMNL-Refresh': str(Config.REFRESH_INTERVAL),
                'X-TRMNL-Plugin-UUID': Config.TRMNL_PLUGIN_UUID
            }
        )
        
    except Exception as e:
        logger.error(f'Webhook error: {str(e)}')
        logger.error(traceback.format_exc())
        return Response(
            display_generator.create_error_display(str(e)),
            mimetype='image/bmp'
        )

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
