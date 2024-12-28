from datetime import datetime, UTC
from typing import Optional, Dict, Any
from flask import jsonify

def format_timestamp(timestamp: str) -> str:
    '''Format timestamp for display.
    
    Args:
        timestamp: ISO format timestamp or UTC timestamp string
        
    Returns:
        Formatted timestamp string in 'YYYY-MM-DD HH:MM UTC' format
    '''
    try:
        # Handle ISO format
        if 'T' in timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        # Handle 'YYYY-MM-DD HH:MM:SS UTC' format
        else:
            dt = datetime.strptime(timestamp.replace(' UTC', ''), '%Y-%m-%d %H:%M:%S')
            dt = dt.replace(tzinfo=UTC)
            
        return dt.strftime('%Y-%m-%d %H:%M UTC')
    except (ValueError, AttributeError):
        return timestamp

def format_error_response(error_message: str, status_code: int = 500) -> Dict[str, Any]:
    '''Format error response for API endpoints.
    
    Args:
        error_message: Error message to return
        status_code: HTTP status code (default 500)
        
    Returns:
        Error response dictionary
    '''
    return jsonify({
        'error': error_message,
        'timestamp': datetime.now(UTC).isoformat(),
        'status': 'error'
    }), status_code

def format_data_response(data: Dict[str, Any]) -> Dict[str, Any]:
    '''Format successful data response.
    
    Args:
        data: Data to return
        
    Returns:
        Formatted response dictionary
    '''
    return {
        'data': data,
        'timestamp': datetime.now(UTC).isoformat(),
        'status': 'success'
    }
