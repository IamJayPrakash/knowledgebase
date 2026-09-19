# Machine Coding: Distributed Sliding Window Rate Limiting Middleware in FastAPI

---

## 🐣 1. Layman's Analogy

Rate limiter ek club ke bouncer ki tarah hai. Rules hain: "Ek minute mein ek aadmi 60 se zyada drinks nahi le sakta". Bouncer har customer ke aane ka exact time stamp register karta hai. Agar pichle 60 seconds ke andar 60 stamps ho chuke hain, toh bouncer bolta hai: `"HTTP 429: Too Many Requests, bhai 5 second wait kar!"`.

---

## 💻 2. Line-by-Line Commented Code Solution

```python
from fastapi import FastAPI, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class SlidingWindowRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # In-memory storage: IP -> List of request timestamps
        # In distributed production, use Redis Sorted Sets (ZADD / ZREMRANGEBYSCORE)
        self.request_history = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Line 17: Extract client IP
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        window_start = current_time - self.window_seconds

        # Line 22: Clean up timestamps older than current window
        history = self.request_history[client_ip]
        self.request_history[client_ip] = [ts for ts in history if ts > window_start]

        # Line 26: Check rate limit threshold
        if len(self.request_history[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later."
            )

        # Line 33: Record current request timestamp
        self.request_history[client_ip].append(current_time)

        # Line 36: Forward request downstream
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(SlidingWindowRateLimiterMiddleware, max_requests=10, window_seconds=60)
```
