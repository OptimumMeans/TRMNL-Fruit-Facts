from datetime import datetime, UTC
import logging
import requests
import random
from typing import Optional, Dict, Any, List
from ..config import Config

logger = logging.getLogger(__name__)

class APIService:
    '''Service for handling Fruityvice API interactions.'''
    
    BASE_URL = 'https://fruityvice.com/api/fruit'
    
    def __init__(self):
        self.last_update = None
        self._cached_data = None
        self._cache_timestamp = None
        self._current_fruit_index = 0
        self._all_fruits = []
        
    def get_data(self) -> Optional[Dict[str, Any]]:
        '''Get fruit data with rotation logic.'''
        try:
            # Initialize or refresh full fruit list if needed
            if not self._all_fruits or not self._is_cache_valid():
                self._all_fruits = self._fetch_all_fruits()
                if not self._all_fruits:
                    raise Exception("Failed to fetch fruits from API")
                
                # Shuffle the list for random rotation
                random.shuffle(self._all_fruits)
                self._current_fruit_index = 0
            
            # Get current fruit and prepare response
            current_fruit = self._all_fruits[self._current_fruit_index]
            
            # Rotate to next fruit for next time
            self._current_fruit_index = (self._current_fruit_index + 1) % len(self._all_fruits)
            
            # Format response
            response = {
                'timestamp': datetime.now(UTC).isoformat(),
                'status': 'ok',
                'fruit': current_fruit,
                'total_fruits': len(self._all_fruits),
                'current_index': self._current_fruit_index
            }
            
            # Update cache
            self._update_cache(response)
            self.last_update = datetime.now(UTC)
            
            return response
            
        except Exception as e:
            logger.error(f"Error fetching fruit data: {str(e)}")
            return None
    
    def _fetch_all_fruits(self) -> List[Dict[str, Any]]:
        '''Fetch all fruits from the API.'''
        try:
            response = requests.get(f"{self.BASE_URL}/all")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return []
    
    def _fetch_fruit_by_id(self, fruit_id: int) -> Optional[Dict[str, Any]]:
        '''Fetch a specific fruit by ID.'''
        try:
            response = requests.get(f"{self.BASE_URL}/{fruit_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch fruit {fruit_id}: {str(e)}")
            return None
    
    def _update_cache(self, data: Dict[str, Any]) -> None:
        '''Update the cache with new data.'''
        self._cached_data = data
        self._cache_timestamp = datetime.now(UTC)
    
    def _is_cache_valid(self) -> bool:
        '''Check if cached data is still valid.'''
        if not self._cache_timestamp:
            return False
            
        cache_age = (datetime.now(UTC) - self._cache_timestamp).total_seconds()
        return cache_age < Config.CACHE_TIMEOUT