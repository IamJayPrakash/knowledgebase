# Low-Level Design (LLD): Production Distributed Rate Limiter

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

Rate Limiter ek **Token Dispenser Machine** ki tarah hai.
Har user ko ek bucket milti hai jisme har second 5 naye tokens girtay hain (**Token Bucket Algorithm**). Jab user API request karta hai, toh ek token kharch ho jata hai. Agar bucket khali ho gayi, toh system request reject kar deta hai (`429 Too Many Requests`).

---

## 📌 2. Key Algorithms Compared

1. **Token Bucket**: Allows controlled bursts; tokens refill at constant rate.
2. **Leaky Bucket**: Enforces strictly smooth output rate like a FIFO queue.
3. **Sliding Window Log**: Stores timestamps of every request (accurate, high memory).
4. **Sliding Window Counter**: Combines counters from current and previous window (low memory, high accuracy).

---

## 💻 3. Line-by-Line Commented Code Solution (Python Token Bucket)

```python
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        # Line 5: Maximum burst capacity of bucket
        self.capacity = capacity
        # Line 7: Rate at which tokens refill into bucket per second
        self.refill_rate = refill_rate_per_sec
        self.current_tokens = capacity
        self.last_refill_timestamp = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_timestamp
        # Line 15: Calculate newly accumulated tokens based on elapsed time
        tokens_to_add = elapsed * self.refill_rate
        self.current_tokens = min(self.capacity, self.current_tokens + tokens_to_add)
        self.last_refill_timestamp = now

    def allow_request(self, tokens_needed: int = 1) -> bool:
        self._refill()
        # Line 22: Consume token if available
        if self.current_tokens >= tokens_needed:
            self.current_tokens -= tokens_needed
            return True
        return False
```
