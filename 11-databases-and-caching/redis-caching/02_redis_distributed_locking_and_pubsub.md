# Redis Distributed Locking (Redlock) and High-Throughput Pub/Sub

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

Single server par ek process thread lock (`mutex`) lagana aasan hai. Lekin jab 20 microservice servers chal rahe hon, toh ek hi database row ko ek sath update hone se rokne ke liye ek **Central Distributed Room Key** chahiye hoti hai.
Redis Distributed Lock (`SET resource_name my_random_token NX PX 30000`) ek **Single Bathroom Key** ki tarah hai:
`NX` = Sirf tab key milegi jab bathroom khali ho.
`PX 30000` = 30 second baad tala apne aap khul jayega taaki agar key holder mar bhi jaye, toh bathroom hamesha ke liye block na ho!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Atomic Lock Acquisition**: `SET lock_key unique_token NX PX 10000`.
   - `NX`: Only set if key does not already exist.
   - `PX 10000`: Expire in 10,000ms to avoid deadlock if worker crashes.
2. **Safe Lock Release via Lua Script**:
   - Releasing the lock MUST verify that `lock_key` still holds `unique_token` before deleting it.
   - If execution took longer than TTL, worker A might delete worker B's newly acquired lock! A Lua script guarantees atomic comparison and deletion.
3. **Pub/Sub Limitations**:
   - Redis Pub/Sub is fire-and-forget. If a subscriber is offline, published messages are lost permanently (Use Redis Streams if persistence and consumer groups are required).

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
import uuid
import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Line 8: Atomic Lua Script to release lock ONLY if token matches
RELEASE_LOCK_LUA = '''
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
'''

class RedisDistributedLock:
    def __init__(self, redis_client, lock_name, ttl_ms=10000):
        self.redis = redis_client
        self.key = f"lock:{lock_name}"
        self.ttl = ttl_ms
        self.token = str(uuid.uuid4())

    def acquire(self) -> bool:
        # Line 25: Atomic acquisition with NX and PX flags
        acquired = self.redis.set(self.key, self.token, nx=True, px=self.ttl)
        return bool(acquired)

    def release(self) -> bool:
        # Line 30: Execute atomic Lua script to release safely
        result = self.redis.eval(RELEASE_LOCK_LUA, 1, self.key, self.token)
        return result == 1

# Usage:
lock = RedisDistributedLock(r, "order_placement_user_101", ttl_ms=5000)
if lock.acquire():
    try:
        print("Acquired distributed lock! Processing financial transaction safely...")
        time.sleep(1)
    finally:
        lock.release()
        print("Distributed lock released cleanly.")
else:
    print("Could not acquire lock; concurrent request already in progress!")
```
