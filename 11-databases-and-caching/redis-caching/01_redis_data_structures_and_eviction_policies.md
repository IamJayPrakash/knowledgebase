# Redis In-Depth: Data Structures, Memory Optimization, and Eviction Policies

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

Redis ek **Ultra-Fast Formula 1 Pit Stop Storage** hai: Sara data computer ke Hard Disk ke bajaye seedhe **RAM (In-Memory)** mein rehta hai, isliye microsecond response time milta hai.
Lekin RAM mehengi aur limited hoti hai. Jab RAM bharne lagti hai, toh Redis ka **Eviction Policy** decide karta hai ki kaun sa purana data bahar feka jaye:

- **LRU (Least Recently Used)**: Jo saman sabse lambe time se kisi ne nahi chhua, use feko.
- **LFU (Least Frequently Used)**: Jo saman sabse kam baar use hua, use feko.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Core Data Structures**:
   - **Strings**: Text, serialized JSON, numbers, bitmaps (`SETBIT`), HyperLogLog (`PFADD`).
   - **Hashes**: Field-value pairs representing objects (`HSET`, `HGETALL`). Highly memory-efficient via `ziplist` / `listpack` encoding.
   - **Lists**: Linked list / quicklist for FIFO queues (`LPUSH`, `RPOP`, `BRPOP`).
   - **Sets**: Unique unordered strings (`SADD`, `SINTER`, `SMEMBERS`).
   - **Sorted Sets (ZSET)**: Stored as SkipLists + HashMaps ordered by floating-point score (`ZADD`, `ZRANGEBYSCORE`). Ideal for leaderboards and sliding-window rate limiters.
2. **Eviction Policies (`maxmemory-policy`)**:
   - `volatile-lru`: Evicts least recently used keys **with an expiration (TTL)** set.
   - `allkeys-lru`: Evicts least recently used keys across all keys (standard cache).
   - `volatile-lfu`: Evicts least frequently used keys with TTL.
   - `allkeys-lfu`: Evicts least frequently accessed keys overall.
   - `noeviction`: Returns errors on write when memory is full (ideal when Redis is used as a primary queue/broker, not a cache).

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
import redis

# Line 4: Connect to Redis instance
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# 1. Hashes for Object Storage (Memory Optimized)
r.hset("user:101", mapping={
    "name": "Jay Prakash",
    "role": "Lead Architect",
    "login_count": 42
})
# Retrieve single field in O(1)
role = r.hget("user:101", "role")

# 2. Sorted Sets for Real-Time Gaming Leaderboard
r.zadd("leaderboard:global", {"player_alice": 9500, "player_bob": 12400, "player_jay": 18200})

# Line 20: Get top 3 players descending with scores
top_players = r.zrevrange("leaderboard:global", 0, 2, withscores=True)
print("Top 3 Players:", top_players)

# Line 24: Atomic Sliding Window Counter using ZSET
def is_allowed_rate_limit(client_id, max_requests=10, window=60):
    import time
    now = time.time()
    pipe = r.pipeline()
    key = f"rate:{client_id}"
    # Remove old timestamps
    pipe.zremrangebyscore(key, 0, now - window)
    # Add current timestamp
    pipe.zadd(key, {str(now): now})
    # Count requests in window
    pipe.zcard(key)
    # Set expiration on the key to avoid zombie keys
    pipe.expire(key, window)
    results = pipe.execute()
    current_count = results[2]
    return current_count <= max_requests
```
