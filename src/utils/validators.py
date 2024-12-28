from datetime import datetime
from typing import Optional, Dict, Any, Tuple
import re

def validate_timestamp(timestamp: str) -> bool:
    '''Validate timestamp format.
    
    Args:
        timestamp: Timestamp string
        
    Returns:
        True if valid, False otherwise
    '''
    # Try ISO format
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        pass
    
    # Try 'YYYY-MM-DD HH:MM:SS UTC' format
    try:
        datetime.strptime(timestamp.replace(' UTC', ''), '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def validate_data(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    '''Validate data dictionary structure.
    
    Args:
        data: Dictionary containing data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    '''
    # Add your data validation logic here
    # Example:
    required_fields = ['timestamp']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
            
    # Validate timestamp if present
    if 'timestamp' in data and not validate_timestamp(data['timestamp']):
        return False, 'Invalid timestamp format'
    
    return True, None

def sanitize_string(input_str: str, max_length: int = 100) -> str:
    '''Sanitize string input for display.
    
    Args:
        input_str: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    '''
    if not isinstance(input_str, str):
        return ''
    
    # Remove any non-printable characters
    clean_str = ''.join(char for char in input_str if char.isprintable())
    
    # Remove any potential HTML/script tags
    clean_str = re.sub(r'<[^>]*>', '', clean_str)
    
    # Truncate to max length
    return clean_str[:max_length]
