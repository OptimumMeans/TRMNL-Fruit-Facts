from datetime import datetime, UTC
import pytest
from src.services.display import DisplayGenerator
from src.services.api_service import APIService

def test_display_generator_initialization():
    '''Test DisplayGenerator initialization'''
    display = DisplayGenerator(800, 480)
    assert display.width == 800
    assert display.height == 480
    assert display.font is not None

def test_error_display():
    '''Test error display generation'''
    display = DisplayGenerator(800, 480)
    error_msg = 'Test error message'
    image_data = display.create_error_display(error_msg)
    assert image_data is not None
    assert len(image_data) > 0

def test_api_service():
    '''Test APIService basic functionality'''
    service = APIService()
    data = service.get_data()
    assert isinstance(data, dict)
    assert 'timestamp' in data
    assert 'status' in data

def test_display_creation():
    '''Test display creation with mock data'''
    display = DisplayGenerator(800, 480)
    test_data = {
        'timestamp': datetime.now(UTC).isoformat(),
        'status': 'ok',
        'test_value': 123
    }
    image_data = display.create_display(test_data)
    assert image_data is not None
    assert len(image_data) > 0
