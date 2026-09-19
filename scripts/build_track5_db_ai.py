# -*- coding: utf-8 -*-
"""
Generator for Track 5: Databases, Caching, and AI / GenAI Deep Dives
Generates:
1. 06-databases-and-caching/sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md
2. 06-databases-and-caching/sql-postgresql/02_postgresql_partitioning_and_replication.md
3. 06-databases-and-caching/redis-caching/01_redis_data_structures_and_eviction_policies.md
4. 06-databases-and-caching/redis-caching/02_redis_distributed_locking_and_pubsub.md
5. 06-databases-and-caching/nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md
6. 06-databases-and-caching/interview-questions/database_indexing_and_caching_questions.md
7. 06-ai-genai/02_vector_search_embeddings_and_hnsw.md
8. 06-ai-genai/03_agentic_workflows_langgraph_and_tool_calling.md
9. 06-ai-genai/04_llm_fine_tuning_lora_and_quantization.md
10. 06-ai-genai/05_production_llm_serving_vllm_and_guardrails.md
11. 06-ai-genai/interview-questions/top_ai_genai_interview_questions.md
12. 06-ai-genai/interview-questions/coding_simple_rag_pipeline_python.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "06-databases-and-caching", "sql-postgresql", "01_postgresql_mvcc_indexing_query_tuning.md"): """# PostgreSQL MVCC, Indexing Strategies, and Query Tuning (EXPLAIN ANALYZE)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purane databases mein jab koi data update karta tha, toh wo table par tala (Lock) laga deta tha: "Main edit kar raha hoon, koi read nahi karega!".
PostgreSQL ka **MVCC (Multi-Version Concurrency Control)** ek **Google Docs Version History** ki tarah hai:
Jab koi writer document update karta hai, wo purani line ko erase nahi karta; wo ek nayi line add kar deta hai jisme naya timestamp hota hai. Readers purana snapshot bina ruke padhte rehte hain! **"Readers never block writers, and writers never block readers."**
Aur jo purani deleted/updated lines bachti hain (Dead Tuples), unhe saaf karne ke liye raat ko ek automated safai karamchari aata hai jiska naam hai **VACUUM**.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **MVCC Internal Tuple Headers**:
   - `xmin`: Transaction ID that inserted this row version.
   - `xmax`: Transaction ID that deleted or updated (created newer version of) this row. Set to 0 if live.
2. **Table Bloat & VACUUM**:
   - `UPDATE` in Postgres is literally `INSERT` (new row) + `DELETE` (mark old row `xmax`).
   - Old dead tuples consume disk and cache until `VACUUM` reclaims the free space.
   - `VACUUM FULL` rewrites the whole table to disk and takes an exclusive table lock (dangerous in production!).
3. **Index Types**:
   - **B-Tree**: Default. Excellent for equality (`=`) and range queries (`<`, `>`, `BETWEEN`).
   - **GIN (Generalized Inverted Index)**: Essential for full-text search and `jsonb` array containment (`@>`).
   - **BRIN (Block Range Index)**: Ultra-compact for huge naturally sequential tables (e.g. time-series timestamp logs).
4. **`EXPLAIN (ANALYZE, BUFFERS)`**:
   - `Seq Scan`: Full table scan (bad if table is large).
   - `Index Scan`: Reads index, then fetches row data from disk heap.
   - `Index Only Scan`: All needed columns exist in the index (no disk heap lookup needed!).
5. **Partial & Expression Indexes**:
   - Partial: `CREATE INDEX idx ON orders(created_at) WHERE status = 'PENDING';` (indexes only pending rows!).

---

## 📊 3. Visual Architecture Diagram

```
                 POSTGRESQL MVCC TUPLE EVOLUTION
                 
  Row 1 (Original):   [ xmin: 101 | xmax: 105 | id: 1 | balance: $100 ] ◄── Dead Tuple!
                                                │ (Updated in Tx 105)
                                                ▼
  Row 2 (New Version):[ xmin: 105 | xmax: 0   | id: 1 | balance: $150 ] ◄── Live Tuple
  
  [ Reader running Tx 102 ] ──► Reads Row 1 (snapshot sees xmax 105 as in the future!)
  [ Reader running Tx 108 ] ──► Reads Row 2 (snapshot sees xmin 105 as committed!)
  
  [ AUTOVACUUM ] ─────────────► Marks Row 1 as reusable disk space!
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```sql
-- Line 1: Check query plan with execution timings and cache buffer hits
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email, created_at
FROM users
WHERE email = 'jay@example.com';

-- Line 7: Creating an optimized Partial Index (Saves 90% disk space)
-- Only indexes active subscriptions, ignoring cancelled accounts
CREATE INDEX CONCURRENTLY idx_active_subscriptions 
ON subscriptions (user_id, plan_id) 
WHERE status = 'ACTIVE';

-- Line 14: Creating an Index on JSONB attributes using GIN
CREATE INDEX CONCURRENTLY idx_user_metadata_gin 
ON users USING GIN (metadata jsonb_path_ops);

-- Line 18: Query utilizing the GIN index for JSON containment
SELECT id, username 
FROM users 
WHERE metadata @> '{"role": "admin", "country": "IN"}';

-- Line 23: Covering Index for "Index Only Scan" (zero table heap reads)
CREATE INDEX CONCURRENTLY idx_orders_covering 
ON orders (customer_id) INCLUDE (total_amount, order_date);
```

---

## 🎯 5. The "Interview Pitch"
> "PostgreSQL delivers high-concurrency throughput through Multi-Version Concurrency Control (MVCC). Rather than locking rows during updates, Postgres writes a new tuple version with an updated `xmin` transaction identifier while marking the previous version with `xmax`. Transactions observe snapshots determined by transaction isolation levels, guaranteeing that readers never block writers. Because obsolete dead tuples generate table bloat, Autovacuum periodically reclaims dead space. When tuning queries, I inspect `EXPLAIN (ANALYZE, BUFFERS)` to diagnose Sequential Scans, leverage Covering Indexes with the `INCLUDE` clause to achieve zero-heap Index Only Scans, and deploy Partial Indexes to minimize index bloat."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an e-commerce database with 80 million orders, the checkout endpoint started experiencing 4-second query timeouts during flash sales on `SELECT * FROM orders WHERE customer_id = $1 AND status = 'PENDING'`.
- **Task**: Reduce query execution latency from 4,000ms to under 5ms under concurrent load.
- **Action**: Running `EXPLAIN ANALYZE` revealed a full Sequential Scan scanning all 80M rows because only 0.05% of orders were in 'PENDING' status at any given time. A standard B-Tree index on `(customer_id, status)` was 6 GB in size and overwhelmed RAM. We created a **Partial Index**: `CREATE INDEX CONCURRENTLY idx_pending ON orders(customer_id) WHERE status = 'PENDING'`.
- **Result**: The partial index size was only 12 MB (a 99.8% reduction), query time dropped from 4,200ms to 0.8ms (Index Scan), and buffer cache hit ratio climbed to 99.9%.
""",

    os.path.join(BASE_DIR, "06-databases-and-caching", "sql-postgresql", "02_postgresql_partitioning_and_replication.md"): """# PostgreSQL Declarative Table Partitioning and Streaming Replication

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Table Partitioning ek **Mega Office File Cabinet** ki tarah hai:
Agar saare 10 saal ke bill ek hi vishal bori mein fek doge, toh 2026 ka bill dhoondne mein ghanton lag jayenge. Partitioning mein aap har saal ka alag drawer bana dete ho: `orders_2024`, `orders_2025`, `orders_2026`. Jab query aati hai `WHERE year = 2026`, toh Postgres baki 9 drawers ko chhoota bhi nahi hai (**Partition Pruning**)!
Streaming Replication **Photocopy Machine Sync** jaisa hai: Main office (Primary) par jo bhi entry hoti hai, photocopy telegraph se branch office (Replica) par turant chhap jati hai (**WAL Streaming**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Partitioning Methods**:
   - **Range**: By dates or numeric IDs (`PARTITION BY RANGE (created_at)`).
   - **List**: By explicit categorical keys (`PARTITION BY LIST (country_code)`).
   - **Hash**: Distributes rows uniformly across partitions (`PARTITION BY HASH (user_id)`).
2. **Partition Pruning**: The query planner excludes irrelevant partition tables from the query plan during planning or execution (`enable_partition_pruning = on`).
3. **Physical Streaming Replication**:
   - Uses Write-Ahead Logging (WAL).
   - Primary streams WAL records to Standby over TCP.
   - Standby continuously applies WAL changes to maintain an exact byte-for-byte read replica.
4. **Synchronous vs Asynchronous Replication**:
   - Asynchronous: Primary commits locally immediately; near-zero latency, but small risk of replication lag data loss during primary crash.
   - Synchronous: Primary waits for at least one replica to write WAL before acknowledging client. Zero data loss (RPO = 0), but higher commit latency.

---

## 💻 3. Line-by-Line Commented Code Snippets

```sql
-- Line 1: Create partitioned parent table
CREATE TABLE audit_logs (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at) -- Partition key MUST be included in Primary Key!
) PARTITION BY RANGE (created_at);

-- Line 10: Create individual partition for January 2026
CREATE TABLE audit_logs_2026_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2026-02-01 00:00:00+00');

-- Line 15: Create partition for February 2026
CREATE TABLE audit_logs_2026_02 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-02-01 00:00:00+00') TO ('2026-03-01 00:00:00+00');

-- Line 20: Partition Pruning verification
-- Query planner scans ONLY audit_logs_2026_01, skipping all other partitions!
EXPLAIN SELECT * FROM audit_logs 
WHERE created_at >= '2026-01-15' AND created_at <= '2026-01-20';
```
""",

    os.path.join(BASE_DIR, "06-databases-and-caching", "redis-caching", "01_redis_data_structures_and_eviction_policies.md"): """# Redis In-Depth: Data Structures, Memory Optimization, and Eviction Policies

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
""",

    os.path.join(BASE_DIR, "06-databases-and-caching", "redis-caching", "02_redis_distributed_locking_and_pubsub.md"): """# Redis Distributed Locking (Redlock) and High-Throughput Pub/Sub

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
""",

    os.path.join(BASE_DIR, "06-databases-and-caching", "nosql-mongodb", "02_mongodb_aggregation_pipeline_mastery.md"): """# MongoDB Aggregation Pipeline: Multi-Stage Document Processing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
MongoDB Aggregation Pipeline ek **Industrial Oil Refinery** ki tarah hai:
Stage 1: Raw crude oil pipeline mein enter hota hai.
Stage 2 (`$match`): Kachra aur mitti chhan kar alag kar di jati hai.
Stage 3 (`$unwind`): Badi barrel khol kar chote packets alag kiye jate hain.
Stage 4 (`$group`): Petrol, diesel, aur kerosene ko alag-alag tanks mein jama karke total quantity sum kiye jate hain.
Stage 5 (`$sort`): Sabse mehenge chemical ko upar display kiya jata hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Pipeline Execution Order**: Stages execute sequentially. Always place `$match` and `$project` as early as possible so subsequent stages process the minimal necessary documents.
2. **Index Utilization**: Only initial stages before any `$project`, `$group`, or `$unwind` can leverage B-Tree indexes for filtering or sorting.
3. **Memory Limits**:
   - Each aggregation stage has a 100 MB RAM limit.
   - If exceeded, MongoDB throws an error unless `allowDiskUse: true` is configured.
4. **Key Stages**:
   - `$match`: Filter documents (uses index if first stage).
   - `$unwind`: Deconstructs an array field from the input documents to output a document for each element.
   - `$lookup`: Performs a left outer join to an unsharded collection.
   - `$group`: Groups documents by a specified identifier and accumulates metrics (`$sum`, `$avg`, `$push`).

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
// MongoDB Aggregation: Calculate Monthly Revenue per Product Category
db.orders.aggregate([
  // Line 3: Stage 1: Filter completed orders within the target year (Uses B-Tree Index!)
  {
    $match: {
      status: "COMPLETED",
      orderDate: {
        $gte: ISODate("2026-01-01T00:00:00Z"),
        $lt: ISODate("2027-01-01T00:00:00Z")
      }
    }
  },

  // Line 14: Stage 2: Deconstruct items array into individual item rows
  {
    $unwind: "$items"
  },

  // Line 19: Stage 3: Join with products collection to retrieve category metadata
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "productDetails"
    }
  },

  // Line 29: Stage 4: Unwind joined product array (1-to-1 match)
  {
    $unwind: "$productDetails"
  },

  // Line 34: Stage 5: Group by Category and calculate revenue and item volume
  {
    $group: {
      _id: "$productDetails.category",
      totalRevenue: {
        $sum: { $multiply: ["$items.quantity", "$items.unitPrice"] }
      },
      totalItemsSold: { $sum: "$items.quantity" },
      uniqueOrders: { $addToSet: "$_id" }
    }
  },

  // Line 46: Stage 6: Sort descending by revenue
  {
    $sort: { totalRevenue: -1 }
  }
], { allowDiskUse: true });
```
""",

    os.path.join(BASE_DIR, "06-databases-and-caching", "interview-questions", "database_indexing_and_caching_questions.md"): """# Top Database & Caching Senior Interview Questions

---

## 1. What is the difference between Clustered and Non-Clustered Indexes?
- **Clustered Index**: Determines the physical order of data rows stored on disk. A table can have **only one** clustered index (e.g. Primary Key in MySQL InnoDB).
- **Non-Clustered Index**: A separate data structure (B-Tree) containing sorted index columns and a pointer (RowID or Primary Key value) back to the actual data row in the clustered table.

---

## 2. Explain the Cache Penetration, Cache Breakdown, and Cache Avalanche problems.
- **Cache Penetration**: Queries request keys that do **not exist in either cache or database**. Every request hits the DB.
  - *Fix*: Cache null values with short TTL, or deploy a Bloom Filter at the gateway.
- **Cache Breakdown**: A single super-hot key expires, and thousands of concurrent requests hit the database simultaneously.
  - *Fix*: Distributed mutex locking (Redlock) or background asynchronous pre-fetching before expiry.
- **Cache Avalanche**: A massive number of cached keys expire at the exact same second, causing the database to crash under sudden load.
  - *Fix*: Add random jitter (e.g. TTL + random(1, 300) seconds) to expiry times.

---

## 3. What is Database Connection Pooling and why is it required?
- Opening a TCP connection to PostgreSQL or MySQL requires a 3-way TCP handshake, TLS negotiation, process/thread allocation, authentication verification, and memory structure initialization (taking 20-100ms per connection).
- Connection pooling maintains a pool of pre-authenticated active connections (e.g. HikariCP in Spring Boot, PgBouncer in Postgres). Applications borrow connections in under 1ms and return them upon query completion.
""",

    os.path.join(BASE_DIR, "06-ai-genai", "02_vector_search_embeddings_and_hnsw.md"): """# Vector Embeddings, Similarity Metrics, and HNSW Indexing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Traditional search (SQL `LIKE %apple%`) **Exact Spelling Match** dhoondta hai. Agar user ne type kiya "red juicy fruit", toh SQL ko "apple" kabhi nahi milega.
Vector Embedding ek sentence ko **3D Space ke GPS Coordinates (Floating Point Array)** mein convert karta hai:
"King" aur "Queen" coordinate space mein paas-paas honge, jabki "Submarine" bohot door hogi.
**HNSW (Hierarchical Navigable Small World)** ek **Multi-Floor Airport Map (Express Highway)** ki tarah hai: Top floor par sirf bade interstate highways hain jo seedhe New York se London le jaate hain. Jaise hi aap paas aate ho, aap neeche ke local floor par utar kar exact gali dhoond lete ho (**Logarithmic $O(\\log N)$ Nearest Neighbor Search**)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Embeddings**: Dense numerical vectors representing semantic meaning generated by models (e.g. OpenAI `text-embedding-3-small`, Cohere, HuggingFace).
2. **Similarity Metrics**:
   - **Cosine Similarity**: Measures cosine angle between vectors ($[-1, 1]$). Ignores vector magnitude (length).
   - **Dot Product**: Measures angle AND magnitude. If vectors are normalized to unit length, Dot Product equals Cosine Similarity and computes much faster.
   - **Euclidean Distance (L2)**: Measures straight-line distance between vector tips.
3. **The Curse of Dimensionality & Exhaustive kNN**:
   - Exact nearest neighbor ($k$NN) compares query against all $N$ vectors ($O(N \\cdot D)$). Unusable for millions of documents.
4. **HNSW (Approximate Nearest Neighbors - ANN)**:
   - Constructs a multi-layer graph based on skip-list principles.
   - Top layers have long-range sparse edges for fast traversal.
   - Bottom layer contains all nodes with dense local neighborhood connections.
   - Delivers sub-millisecond retrieval with 98%+ recall.

---

## 📊 3. Visual Architecture Diagram

```
                 HNSW MULTI-LAYER GRAPH TRAVERSAL
                 
   Layer 2 (Express): [ Entry Point ] ──────────────────────► [ Node A ]
                                                                   │
                                                                   ▼ (Drop down)
   Layer 1 (Sub-highways):             [ Node B ] ──────────► [ Node A ] ──► [ Node C ]
                                                                   │
                                                                   ▼ (Drop down)
   Layer 0 (Local Dense):  [ D ] ──► [ B ] ──► [ E ] ──► [ Nearest Match! ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```python
import numpy as np

# Line 3: Vector Math Foundations: Cosine Similarity from scratch
def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    # Dot product divided by the product of L2 norms
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(dot_product / (norm_v1 * norm_v2))

# Vector search demonstration with FAISS (HNSW Index)
import faiss

dimension = 128
num_elements = 10000

# Generate synthetic vector database
data_vectors = np.random.random((num_elements, dimension)).astype("float32")
faiss.normalize_L2(data_vectors) # Normalize for inner product search

# Line 23: Create HNSW Index with M=32 neighbors per node
index = faiss.IndexHNSWFlat(dimension, 32)
index.hnsw.efConstruction = 64 # Construction search depth
index.add(data_vectors)

# Perform query
query_vector = np.random.random((1, dimension)).astype("float32")
faiss.normalize_L2(query_vector)

k = 5 # Retrieve top 5 closest neighbors
distances, indices = index.search(query_vector, k)
print("Top 5 Vector Indices:", indices)
print("Distances:", distances)
```
""",

    os.path.join(BASE_DIR, "06-ai-genai", "03_agentic_workflows_langgraph_and_tool_calling.md"): """# Agentic Workflows: State Machines, LangGraph, and Tool Calling

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Single-prompt LLM ek **Ek Baar Bolne Wale Astrologer** ki tarah hai: Aapne question poocha, usne ek lamba paragraph bol diya. Agar galat bola, toh bhi wo correction nahi kar sakta.
Agentic Workflow ek **Autonomous Project Team (State Machine)** ki tarah hai:
Step 1: Manager (LLM) plan banata hai.
Step 2: Analyst tool execute karta hai (Search Google, Query SQL).
Step 3: Quality Reviewer output check karta hai. Agar error aayi, toh loop wapas Step 1 par jaata hai (**Self-Correction Loop**) jab tak result 100% accurate na ho!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **ReAct Pattern (Reasoning + Acting)**:
   - LLM generates a Thought -> Chooses an Action (Tool call) -> Receives Observation -> Generates next Thought.
2. **LangGraph StateGraph Architecture**:
   - Represents agent workflows as a cyclic graph of **Nodes** (Python functions) and **Edges** (conditional transitions).
   - Unlike DAGs, LangGraph natively supports **Loops** (essential for reflection, linting, and retrying).
3. **Structured Tool Calling**:
   - Modern LLMs (GPT-4o, Claude 3.5, Gemini 1.5 Pro) output strict JSON arguments conforming to provided JSON Schema definitions.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from typing import TypedDict, Annotated, Sequence
import operator

# Line 5: Define shared agent state schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], operator.add]
    current_step: str
    retry_count: int

# Simulated LangGraph Node Functions
def router_node(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]["content"]

    # Conditional branching logic
    if "error" in last_message and state["retry_count"] < 3:
        return "retry_step"
    elif "finish" in last_message:
        return "end"
    return "execute_tool"

def execute_tool_node(state: AgentState) -> dict:
    print("Executing external API tool call...")
    return {
        "messages": [{"role": "system", "content": "Database returned 42 records"}],
        "current_step": "tool_executed",
        "retry_count": state["retry_count"]
    }
```
""",

    os.path.join(BASE_DIR, "06-ai-genai", "04_llm_fine_tuning_lora_and_quantization.md"): """# LLM Fine-Tuning: LoRA, QLoRA, and Quantization (GGUF, AWQ, GPTQ)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Full Fine-Tuning 70 Billion parameters wale model ke **Har Ek Screw Ko Khologe Dobara Fit Karne Jaisa Hai** (Requires $100,000 worth of GPUs and 80GB VRAM).
**LoRA (Low-Rank Adaptation)** ek **Chote Transparent Sticky Note** ki tarah hai: Asli 1000-page ki book (Base LLM weights) ko chhedne ke bajaye, aap uske upar ek chota sticky note chipkate ho (Rank decomposition matrices A and B). Model wahi rehta hai, sirf 0.1% naye parameters train hote hain!
**Quantization** ek **High-Res 4K Video ko 1080p mein Compress** karne jaisa hai: 16-bit floating point numbers (`FP16`) ko 4-bit integers (`INT4`) mein convert kar diya jata hai taaki 70B model aapke normal gaming laptop par chal sake!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Math of LoRA**:
   - Instead of updating weight matrix $W \\in \\mathbb{R}^{d \\times k}$ directly ($W = W + \\Delta W$), we decompose $\\Delta W$ into two low-rank matrices: $\\Delta W = B \\times A$, where $B \\in \\mathbb{R}^{d \\times r}$ and $A \\in \\mathbb{R}^{r \\times k}$ with rank $r \\ll \\min(d, k)$.
   - Freezes 99.9% of base model weights; only updates adapters.
2. **QLoRA (Quantized LoRA)**:
   - Quantizes the base model weights to NormalFloat4 (NF4) and introduces Double Quantization, enabling fine-tuning a 65B model on a single 48GB GPU.
3. **Quantization Formats**:
   - **GGUF**: Modern standard for CPU/Metal inference (via llama.cpp).
   - **AWQ (Activation-aware Weight Quantization)**: Preserves salient weights based on activation distribution; state-of-the-art for high-throughput GPU serving (vLLM).
   - **GPTQ**: Post-training 4-bit quantization optimized for fast GPU matrix multiplication.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
# PEFT LoRA Configuration Setup
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM

# Line 5: Define LoRA Hyperparameters
lora_config = LoraConfig(
    r=16,                                    # Rank dimension (lower = fewer parameters)
    lora_alpha=32,                           # Scaling factor for adapter weights
    target_modules=["q_proj", "v_proj"],     # Apply LoRA to attention query and value layers
    lora_dropout=0.05,                       # Dropout for regularization
    bias="none",                             # Do not train bias terms
    task_type=TaskType.CAUSAL_LM             # Generative Language Modeling task
)

# Base model load with 4-bit quantization (BitsAndBytes)
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B", load_in_4bit=True)
# peft_model = get_peft_model(model, lora_config)
# peft_model.print_trainable_parameters()
# Trainable params: 0.08% of total weights!
```
""",

    os.path.join(BASE_DIR, "06-ai-genai", "05_production_llm_serving_vllm_and_guardrails.md"): """# Production LLM Serving: vLLM, PagedAttention, and Guardrails

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Traditional LLM inference mein jab 100 users chat karte hain, toh server har user ke liye pehle se memory book karke rakh leta hai (**KV Cache Fragmentation**). Aadhe se zyada GPU VRAM khali padi rehti hai lekin dusre users ko "Out of Memory" error mil jata hai.
**vLLM ka PagedAttention** Operating System ke **Virtual Memory Paging** ki tarah hai: Ye VRAM ko 16-token ke chote chote pages mein todta hai aur tabhi memory allocate karta hai jab actual word generate hota hai. Isse ek hi GPU par 4x se 10x zyada concurrent users serve ho jate hain!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The KV Cache Bottleneck**: In autoregressive generation, past Key and Value matrices are cached to prevent recalculating past tokens. KV Cache grows dynamically with sequence length.
2. **PagedAttention**: Divides continuous KV Cache into non-contiguous physical memory blocks. Reduces memory waste to < 4%.
3. **Continuous Batching (Iteration-level Scheduling)**:
   - Instead of waiting for the slowest request in a batch to finish, vLLM injects new requests into the running iteration as soon as any request completes.
4. **Guardrails & Content Safety (NeMo Guardrails / Llama Guard)**:
   - Input Guardrails: Detect prompt injections, jailbreaks, and PII leaks.
   - Output Guardrails: Validate hallucination metrics, schema compliance, and toxicity.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
# Serving with vLLM Python Engine
from vllm import LLM, SamplingParams

# Line 4: Configure high-throughput inference engine
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    max_tokens=256
)

# Line 11: vLLM automatically utilizes PagedAttention and continuous batching
llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    tensor_parallel_size=1, # Number of GPUs
    gpu_memory_utilization=0.90 # Utilize 90% of GPU VRAM for KV cache
)

prompts = [
    "Explain quantum computing in 2 sentences.",
    "Write a Python function to check for prime numbers."
]

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(f"Generated text: {output.outputs[0].text}")
```
""",

    os.path.join(BASE_DIR, "06-ai-genai", "interview-questions", "top_ai_genai_interview_questions.md"): """# Top AI & GenAI Senior Interview Questions (Production Systems)

---

## 1. What is the difference between RAG (Retrieval-Augmented Generation) and Fine-Tuning?
- **RAG**:
  - Injects external knowledge dynamically into the LLM context window at query time.
  - Ideal for constantly updating company knowledge bases, verifiable citations, and zero training costs.
  - Cannot alter the fundamental tone, style, or vocabulary of the model.
- **Fine-Tuning**:
  - Updates the actual weights of the neural network using specialized datasets.
  - Ideal for teaching domain-specific output formats (JSON/SQL), specialized styles, or complex syntax.
  - Static: Does not possess knowledge of documents created after the training cutoff.

---

## 2. What causes Hallucinations in LLMs and how do you mitigate them?
- **Causes**: LLMs are probabilistic token prediction engines trained on statistical likelihood, not fact-checkers. Gaps in training data or ambiguous context prompt the model to generate plausible-sounding falsehoods.
- **Mitigation**:
  - Enforce strict ground-truth context via RAG.
  - Lower the sampling `temperature` to 0.0 or 0.1 for factual tasks.
  - Add negative constraints: "If the information is not present in the provided context, state 'I do not have enough information'".
  - Implement programmatic output evaluation guardrails (e.g. Ragas faithfulness checks).

---

## 3. Explain how PagedAttention solves the KV-Cache memory fragmentation problem.
- In traditional inference, KV-Cache memory must be allocated contiguously based on the maximum possible sequence length (e.g. 4096 tokens). Because most requests are much shorter, up to 70% of GPU VRAM is wasted in internal fragmentation.
- PagedAttention divides the KV Cache into fixed-sized blocks (pages) stored in non-contiguous physical GPU memory, managed via a page table like modern OS virtual memory. Memory is allocated on-demand, enabling massive batch concurrency.
""",

    os.path.join(BASE_DIR, "06-ai-genai", "interview-questions", "coding_simple_rag_pipeline_python.md"): """# Machine Coding: End-to-End RAG Pipeline in Pure Python

---

## 🐣 1. Layman's Analogy
RAG pipeline ek **Open-Book Exam** ki tarah hai: Jab question aata hai, toh student (Search Engine) library se relevant 2 page nikalta hai (`Chunk Retrieval`), aur fir professor (LLM) ko bolta hai: "Sirf in 2 panno ko dekh kar answer likho, apne man se kahani mat banao" (`Grounded Prompt Generation`)!

---

## 💻 2. Line-by-Line Commented Code Solution

```python
import numpy as np

# Simple In-Memory Vector Store for RAG Pipeline
class SimpleVectorRAG:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    # Simulated embedding generator (In production, call OpenAI / HuggingFace API)
    def _mock_embed(self, text: str) -> np.ndarray:
        # Deterministic pseudo-embedding based on character hashes for demo
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(64).astype("float32")
        norm = np.linalg.norm(vec)
        return vec / (norm if norm > 0 else 1.0)

    # Line 18: Ingest and chunk documents
    def add_document(self, doc_id: str, text: str):
        self.documents.append({"id": doc_id, "text": text})
        embedding = self._mock_embed(text)
        self.embeddings.append(embedding)

    # Line 24: Retrieve Top-K most relevant document chunks
    def retrieve(self, query: str, k: int = 2):
        query_vec = self._mock_embed(query)
        similarities = []

        for idx, doc_vec in enumerate(self.embeddings):
            # Calculate cosine similarity (vectors are unit normalized)
            score = float(np.dot(query_vec, doc_vec))
            similarities.append((score, self.documents[idx]))

        # Sort descending by similarity score
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]

    # Line 38: Construct augmented grounded prompt for LLM
    def generate_grounded_prompt(self, user_query: str) -> str:
        relevant_chunks = self.retrieve(user_query, k=2)
        context_str = "\\n---\\n".join([c[1]["text"] for c in relevant_chunks])

        prompt = f'''You are an enterprise AI assistant. Answer the user question strictly using ONLY the provided context below.
If the answer cannot be deduced from the context, respond with "I cannot find this information in the knowledge base."

CONTEXT:
{context_str}

USER QUESTION:
{user_query}

ANSWER:'''
        return prompt

# Test RAG Pipeline
rag = SimpleVectorRAG()
rag.add_document("doc1", "Next.js App Router uses React Server Components by default to eliminate client bundle size.")
rag.add_document("doc2", "Redis distributed locking requires the Redlock algorithm or atomic SET NX PX with Lua script verification.")

augmented_prompt = rag.generate_grounded_prompt("How does Next.js handle server components?")
print("Constructed Grounded Prompt:\\n")
print(augmented_prompt)
```
"""
}

def main():
    print(f"Generating {len(FILES)} Track 5 Database, Caching & AI/GenAI deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 5 Database, Caching & AI/GenAI generation complete!")

if __name__ == "__main__":
    main()
