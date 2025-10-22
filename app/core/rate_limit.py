# app/core/rate_limit.py
import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException


class RateLimiter:
    def __init__(self, per_minute: int = 60):
        self.per_minute = per_minute
        self.buckets: Dict[str, Tuple[int, float]] = {}

    def check(self, request: Request):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        count, reset = self.buckets.get(ip, (0, now + 60))
        if now > reset:
            count, reset = 0, now + 60
        count += 1
        self.buckets[ip] = (count, reset)
        if count > self.per_minute:
            retry = int(reset - now)
            raise HTTPException(status_code=429, detail="Trop de requêtes. Réessayez plus tard.",
                                headers={"Retry-After": str(max(1, retry))})


limiter = RateLimiter()
