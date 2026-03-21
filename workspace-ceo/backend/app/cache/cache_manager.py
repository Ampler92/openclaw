from typing import Any, Optional
import time
import json

class CacheManager:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 60):
        self.default_ttl = default_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value with optional TTL"""
        ttl = ttl or self.default_ttl
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value if not expired"""
        entry = self.cache.get(key)
        if not entry:
            return None
        
        if time.time() > entry["expires_at"]:
            del self.cache[key]
            return None
        
        return entry["value"]
    
    def delete(self, key: str) -> None:
        """Delete cache entry"""
        self.cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
