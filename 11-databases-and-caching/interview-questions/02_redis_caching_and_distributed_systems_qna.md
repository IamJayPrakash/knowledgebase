# Databases & Caching Master Interview Bank: Part 2 (Q21 - Q40)

## Redis Architecture, In-Memory Internals, Clustering & Redlock

---

### Q21: Why is Redis single-threaded yet capable of handling 100,000+ QPS?

**Answer:**
Redis executes commands on a **single execution thread** using 3 primary architectural principles:

1. **In-Memory Operations:** All data resides directly in RAM. There are zero random disk seeks or page faults. In-memory read/writes complete in nanoseconds.
2. **Non-Blocking I/O Multiplexing (`epoll` / `kqueue`):** A single thread monitors thousands of client TCP sockets simultaneously using OS event-driven notification primitives. When a socket has data ready, Redis reads and processes it without blocking on idle connections.
3. **Zero Thread-Lock Overhead:** Because command execution is single-threaded, Redis has **zero thread context switching, zero mutex lock contention, and zero race conditions** in its core data operations!

*(Note: In Redis 6.0+, multi-threading was added strictly for parsing network socket reads and writes, while command execution remains single-threaded).*

---

### Q22: What are the 6 core Redis Data Structures and their internal C implementations?

**Answer:**

1. **String:** Implemented as **Simple Dynamic String (SDS)**. Stores length in header ($O(1)$ `strlen`), binary safe, pre-allocates buffer to prevent buffer overflows.
2. **List:** Implemented as a **Quicklist** (a doubly linked list of compact **Listpack / ZipList** nodes to minimize pointer memory overhead).
3. **Hash:** Small hashes use **Listpack** (memory efficient); large hashes convert to a **Dict** (Hash table with incremental rehashing).
4. **Set:** Sets of small integers use **Intset** (sorted contiguous integer array); general sets use a **Dict** with `NULL` values.
5. **Sorted Set (ZSet):** Composite data structure pairing a **Hash Table** ($O(1)$ score lookups) + a **SkipList** ($O(\log N)$ range queries and rank operations).
6. **HyperLogLog:** Probabilistic data structure estimating the cardinality of billions of unique items with a fixed **12 KB memory footprint** and $< 1\%$ error margin!

---

### Q23: How does a SkipList work in Redis Sorted Sets (ZSet)?

**Answer:**

- A **SkipList** is a probabilistic hierarchy of layered linked lists.
- **The Structure:**
  - Base layer (Level 0) contains all elements in sorted order.
  - Each higher level acts as an "express lane", skipping over a fraction of elements based on a random geometric coin-flip distribution (probability $p = 0.25$).
- **Search Performance:** By traversing high-level express lanes and dropping down when overshooting, search, insertion, and deletion run in **$O(\log N)$ average time**, rivaling Red-Black trees but being much simpler to implement and range-scan.

---

### Q24: Explain the 8 Redis Cache Eviction Policies

**Answer:**
When Redis memory usage exceeds `maxmemory`:

1. **`noeviction` (Default):** Returns an error (`OOM command not allowed`) on write operations; read requests continue working.
2. **`allkeys-lru`:** Evicts least recently used keys across **all keys** (standard cache policy).
3. **`volatile-lru`:** Evicts least recently used keys among those with an **expiration TTL set**.
4. **`allkeys-lfu`:** Evicts least frequently used keys across all keys (counts access frequency).
5. **`volatile-lfu`:** Evicts least frequently used keys among those with an expiration TTL set.
6. **`volatile-ttl`:** Evicts the key with the **shortest remaining Time-To-Live (TTL)**.
7. **`allkeys-random`:** Evicts random keys from the entire keyspace.
8. **`volatile-random`:** Evicts random keys from those with an expiration TTL.

---

### Q25: How does Redis approximate LRU without storing a linked list of all keys?

**Answer:**

- Maintaining a true doubly linked list of millions of keys would require massive pointer memory and expensive lock updates on every read operation.
- **Approximated LRU in Redis:**
  - Every object struct stores a 24-bit timestamp: `lru_clock`.
  - When eviction is triggered, Redis samples a small random batch of keys (default: $N = 5$ keys).
  - It finds the key with the oldest timestamp in that sample and evicts it!
  - Increasing sample size to $N = 10$ produces an eviction curve virtually indistinguishable from true mathematical LRU while consuming zero additional RAM.

---

### Q26: Compare Redis Persistence: RDB (Snapshots) vs AOF (Append-Only File)

**Answer:**

| Feature | RDB (Redis Database Snapshot) | AOF (Append-Only File) |
| :--- | :--- | :--- |
| **Mechanism** | Point-in-time binary snapshot of entire dataset dumped to disk (`dump.rdb`). | Logs every single write command sequentially to an append-only file (`appendonly.aof`). |
| **Data Loss Window** | Minutes (data written since last snapshot is lost on crash). | Minimal (typically $\le 1$ second of data loss). |
| **File Size** | **Compact & small** (ideal for disaster recovery backups). | Larger file size; requires background rewriting (`AOF Rewrite`). |
| **Recovery Speed** | **Fastest** (loads binary snapshot directly into RAM). | Slower (must replay every command in the log). |
| **Performance Impact** | Forks a background child process (`bgsave`), which can cause latency spikes on large heaps. | Continuous disk I/O overhead on background disk thread. |

---

### Q27: How does `AOF Rewrite` work without blocking client requests?

**Answer:**
Over time, the AOF log file balloons in size with redundant commands (e.g. 1,000 `INCR count` operations).

- **`BGREWRITEAOF`:**
  1. Redis calls `fork()` to spawn a background child process.
  2. The child process reads the current in-memory dataset and writes the minimal state representation directly into a temporary new AOF file.
  3. Meanwhile, the parent process continues serving client writes, buffering new mutations in an **AOF Rewrite Buffer**.
  4. When the child finishes, the parent appends the buffered mutations and atomically renames the temporary file, replacing the old bloated AOF file!

---

### Q28: How do you implement a Distributed Lock correctly with single-instance Redis?

**Answer:**

- **Acquire Lock:**
  Must be atomic using `SET` with `NX` (only set if not exists) and `PX` (millisecond expiration):

  ```redis
  SET resource_lock my_random_unique_token NX PX 30000
  ```

- **Release Lock (MANDATORY Lua Script):**
  Never use a simple `DEL`! If the lock expires while the client is still processing and another client acquires it, a simple `DEL` would delete the other client's lock!
  The client must check if the token matches before deleting:

  ```lua
  if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
  else
      return 0
  end
  ```

---

### Q29: What is the Redlock Algorithm and what is Martin Kleppmann's critique?

**Answer:**

- **Redlock (Salvatore Sanfilippo):**
  Designed for multi-node Redis clusters without shared state:
  1. Client attempts to acquire lock across $N$ independent Redis master nodes (e.g. 5 nodes) sequentially using matching tokens and timeouts.
  2. The lock is acquired if client gets lock on majority ($\ge \lfloor N/2 \rfloor + 1 = 3$) nodes within elapsed time $< \text{TTL}$.
- **Martin Kleppmann's Critique:**
  Redlock relies on physical time assumptions. If a client suffers a stop-the-world GC pause or clock jump, its lock can expire silently while the client continues executing, corrupting shared data.
  - *Solution:* Must pair distributed locks with **Fencing Tokens** (monotonically increasing integer tokens verified by storage).

---

### Q30: How do Redis Transactions (`MULTI`/`EXEC`) differ from SQL ACID transactions?

**Answer:**

- Redis transactions are command queues:
  - `MULTI`: Starts queuing commands.
  - `EXEC`: Executes all queued commands sequentially in a single atomic batch.
  - `DISCARD`: Flushes queued commands.
- **Major Differences from SQL:**
  1. **No Rollback on Runtime Error:** If a command in the transaction fails (e.g. calling list operation on a string key), Redis **continues executing the remaining commands anyway**! There is NO rollback.
  2. **Optimistic Locking via `WATCH`:** `WATCH key` monitors keys for changes. If another client modifies the watched key before `EXEC`, the entire transaction aborts.

---

### Q31: What are Redis Hash Slots in Redis Cluster?

**Answer:**

- Redis Cluster does not use consistent hashing rings; it divides the keyspace into **16,384 Hash Slots** ($0$ to $16,383$).
- **Slot Assignment Formula:**
  $$\text{Slot} = \text{CRC16}(\text{key}) \pmod{16384}$$
- **Multi-Node Distribution:**
  - In a 3-node cluster: Node A holds slots $0-5460$; Node B holds $5461-10922$; Node C holds $10923-16383$.
- **Live Re-sharding:** Adding a 4th node simply moves slots from existing nodes to the new node **without any cluster downtime**!

---

### Q32: What are Hash Tags (`{...}`) in Redis Cluster and why are they needed?

**Answer:**

- In Redis Cluster, multi-key operations (`MGET`, transactions, Lua scripts) are **strictly forbidden if keys belong to different hash slots** (`CROSSSLOT Keys in request don't hash to the same slot`).
- **Hash Tags Solution:**
  Enclosing a substring in braces `{...}` forces Redis to compute the CRC16 hash **only on the text inside the braces**:
  - `user:{1001}:profile` $\to$ hashes `"1001"`.
  - `user:{1001}:orders` $\to$ hashes `"1001"`.
- Guarantees that all related keys for user `1001` reside on the **exact same Redis node and hash slot**, allowing multi-key atomic transactions!

---

### Q33: How does Redis Sentinel provide High Availability?

**Answer:**

- **Redis Sentinel:** A distributed monitoring system running alongside Redis Master-Replica setups:
  1. **Monitoring:** Continuously sends `PING` heartbeats to check master and replica health.
  2. **Notification:** Sends alerts via API when an instance fails.
  3. **Automatic Failover:** If a master is unreachable (`SDOWN` - Subjectively Down) and a quorum of Sentinels agree (`ODOWN` - Objectively Down), Sentinels elect a leader via Raft and **promote a healthy replica to master**.
  4. **Configuration Provider:** Clients query Sentinel to discover the current active master IP address.

---

### Q34: What is the difference between Redis Pub/Sub and Redis Streams?

**Answer:**

| Feature | Redis Pub/Sub | Redis Streams (`XADD`, `XREAD`) |
| :--- | :--- | :--- |
| **Persistence** | **Ephemeral** (fire-and-forget). If consumer is offline, message is permanently lost. | **Durable** append-only log persisted on disk. |
| **Consumer Groups** | ❌ No. Every subscriber gets every message. | ✅ Yes. Supports consumer groups and load-balanced reading (like Kafka). |
| **Message ACK** | ❌ No acknowledgement. | ✅ Yes (`XACK`). Unacked messages tracked in Pending Entries List (PEL). |
| **History Replay** | ❌ Cannot replay historical events. | ✅ Can read from any historical ID or offset. |

---

### Q35: What is a Redis Pipeline and how does it reduce network latency?

**Answer:**

- Normally, Redis operations follow a request-response ping-pong pattern: client sends command 1, waits for network RTT, receives response, then sends command 2.
- **Pipelining:**
  The client buffers multiple commands and sends them **in a single TCP network packet** to Redis. Redis executes all commands and returns all responses together in a single packet.
- **Benefit:** Reduces 100 sequential operations from 100 network RTTs (~100ms) down to a **single network RTT (~1ms)**!

---

### Q36: What is the "Cache Penetration" problem and how do you prevent it?

**Answer:**

- **Cache Penetration:** Requests query for keys that **do not exist in the cache AND do not exist in the database** (e.g. malicious requests querying `user_id = -99999`).
- Because the key never exists, it can never be cached, so every single request penetrates through to the database, exhausting database resources.
- **Mitigations:**
  1. **Cache Null Values:** If DB returns empty, write `{"user_id": -99999, "status": "NOT_FOUND"}` into Redis with a short TTL (e.g. 60 seconds).
  2. **Bloom Filter at Edge:** Check a Bloom Filter containing all valid IDs before querying Redis or DB.

---

### Q37: What is "Cache Breakdown" (Hotspot Invalidated) vs "Cache Avalanche"?

**Answer:**

- **Cache Breakdown:** A **single, ultra-hot key** (e.g. trending news item or flash sale product) expires, and thousands of concurrent requests miss the cache simultaneously, overwhelming the database.
  - *Fix:* Distributed mutex lock (`SET NX`) or probabilistic early refresh (XFetch).
- **Cache Avalanche:** A **massive number of different keys expire at the exact same second** (e.g. setting fixed 1-hour TTL on 1,000,000 keys at once) or the Redis server crashes.
  - *Fix:* **Add Random Jitter to TTL**: `TTL = base_ttl + random(0, 300)` to spread expiration times evenly across a 5-minute window.

---

### Q38: What is Redis Replication and how does PSYNC2 work?

**Answer:**

- Replicas connect to master and request synchronization via **`PSYNC`**:
  1. **Full Synchronization:** Master runs `BGSAVE` in background, creates RDB file, sends RDB to replica, and replica flushes memory and loads RDB.
  2. **Partial Resynchronization (PSYNC2):**
     If network blips briefly, master tracks recent writes in a circular in-memory buffer called the **Replication Backlog**.
     When replica reconnects with its replication offset, master streams only the missing byte delta without repeating an expensive full RDB dump!

---

### Q39: What is BigKey in Redis and why is it dangerous?

**Answer:**

- **BigKey:** A key containing an excessively large value (e.g. a String $> 5\text{MB}$ or a Hash/Set containing $> 50,000$ fields).
- **Dangers:**
  1. Blocks the single-threaded execution loop during read/delete operations.
  2. Deleting a BigKey (`DEL my_big_set`) blocks Redis for hundreds of milliseconds.
- **Solution:** Use **`UNLINK` (Asynchronous Deletion)** instead of `DEL`. `UNLINK` removes the key from the keyspace instantly and deallocates memory in a background thread.

---

### Q40: What are Redis Bitmaps and Bitfields?

**Answer:**

- Bitmaps are string values treated as a continuous array of individual bits ($0$ or $1$) using `SETBIT` and `GETBIT`.
- **Use Case:** Tracking daily active users (DAU) or user login streaks.
  - Assign each user an integer ID. Setting bit `user_id` to 1 on day offset requires only **1 bit per user**!
  - 100,000,000 users' login status requires only **~12 Megabytes of RAM**!
  - `BITOP AND` computes intersection of users active on both Monday and Tuesday in milliseconds.
