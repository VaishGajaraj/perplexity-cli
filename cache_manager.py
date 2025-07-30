import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class CacheManager:
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, query: str, cache_type: str) -> str:
        """Generate a cache key from query and type"""
        hash_input = f"{query}:{cache_type}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get the file path for a cache key"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, query: str, cache_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached data if it exists and is not expired"""
        cache_key = self._get_cache_key(query, cache_type)
        cache_path = self._get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=self.ttl_hours):
                os.remove(cache_path)
                return None
            
            return cached_data['data']
        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid cache file, remove it
            os.remove(cache_path)
            return None
    
    def set(self, query: str, cache_type: str, data: Dict[str, Any]) -> None:
        """Store data in cache"""
        cache_key = self._get_cache_key(query, cache_type)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'type': cache_type,
            'data': data
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def clear(self) -> None:
        """Clear all cached data"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, filename))