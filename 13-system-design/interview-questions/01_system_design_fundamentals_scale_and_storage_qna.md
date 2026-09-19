# System Design Master Interview Bank: Part 1 (Q1 - Q20)

## Scale, Latency, Storage, Databases & Caching

---

### Q1: What is the difference between Scalability, Availability, and Reliability?

**Answer:**

- **Scalability:** The ability of a system to handle increased load without performance degradation by adding resources (Vertical scaling / scaling up, or Horizontal scaling / scaling out).
- **Availability:** The percentage of time a system remains operational and accessible to process requests over a given period (e.g. 99.99% "Four Nines" = at most 52.6 minutes of downtime per year). Calculated as:
  $$\text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$
  *(MTBF = Mean Time Between Failures, MTTR = Mean Time To Repair).*
- **Reliability:** The probability that a system will perform its required functions correctly without error over a specified duration.
  - *Distinction:* A system can be **available** (returns HTTP 200) but **unreliable** (returns corrupted data or empty payloads).

---

### Q2: What is the trade-off between Latency and Throughput?

**Answer:**

- **Latency:** The time required to process a single request from client dispatch to response delivery (measured in milliseconds; reported as P50, P90, P99, P99.9).
- **Throughput:** The number of actions or operations processed per unit of time (measured in Queries Per Second `QPS`, Requests Per Second `RPS`, or Megabytes/sec).
- **The Trade-off:** Maximizing throughput often increases latency due to queuing delays (Little's Law: $L = \lambda W$). Batching multiple operations increases throughput by amortizing fixed network/disk overhead, but increases the latency of individual items waiting in the batch buffer.

---

### Q3: When should you choose SQL (Relational) vs NoSQL (Non-Relational)?

**Answer:**

```
                            System Requirements
                                     │
      ┌──────────────────────────────┴──────────────────────────────┐
      ▼                                                             ▼
[ Choose Relational (SQL) ]                             [ Choose NoSQL ]
- Strict ACID transactions                              - Massive unstructured or polymorphic data
- Normalized data with complex JOINs                    - Petabyte-scale horizontal scale-out
- Strong financial consistency                          - High write throughput (append-only)
- Predictable schema                                    - Flexible, schema-less document JSON
- Examples: PostgreSQL, MySQL, Spanner                  - Examples: Cassandra, MongoDB, DynamoDB
```

---

### Q4: Explain ACID properties in Relational Database Management Systems

**Answer:**

- **Atomicity:** All operations within a transaction succeed completely or all are rolled back. No partial state is ever committed.
- **Consistency:** A transaction transitions the database from one valid state to another, satisfying all schema constraints, cascades, foreign keys, and unique checks.
- **Isolation:** Concurrent transactions execute without interfering with one another. (Isolation Levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable).
- **Durability:** Once a transaction is committed, its results are permanent and guaranteed to survive server crashes or power outages (achieved via Write-Ahead Logging `WAL`).

---

### Q5: How do B-Tree and B+Tree Indexes work, and why are B+Trees preferred for databases?

**Answer:**

- **B-Tree:** Self-balancing multi-way search tree. Keys and data pointers are stored in both internal nodes and leaf nodes.
- **B+Tree:**
  1. Internal nodes store **keys only** (acting as routing signposts), allowing each 4KB disk page to hold hundreds of branching keys (High Fanout, low tree height $\le 3-4$ levels).
  2. Leaf nodes store **all actual data pointers/records**.
  3. All leaf nodes are linked together in a **doubly linked list**.
- **Why B+Trees win:** Range queries (`WHERE age BETWEEN 20 AND 30`) only require a single $O(\log N)$ lookup to the first leaf node, followed by a linear linked list traversal across contiguous disk blocks, completely eliminating random disk seeks.

---

### Q6: What is a Clustered Index vs a Non-Clustered (Secondary) Index?

**Answer:**

- **Clustered Index:**
  - Dictates the **physical order of rows on disk storage**.
  - The leaf nodes of the clustered index contain the actual table row data.
  - A table can have **only one clustered index** (almost always the Primary Key).
- **Non-Clustered (Secondary) Index:**
  - A separate B+Tree structure stored independently from table rows.
  - The leaf nodes contain the indexed column key and a pointer (e.g. Primary Key ID) to the clustered index row.
  - Requires a secondary **Index Lookup (Bookmark Lookup)** to fetch remaining columns unless it is a **Covering Index**.

---

### Q7: What is a Covering Index and how does it eliminate Bookmark Lookups?

**Answer:**

- A **Covering Index** contains all the columns referenced in a query (`SELECT`, `WHERE`, `ORDER BY`).
- Because all requested data exists directly inside the leaf nodes of the secondary index tree, the database engine satisfies the entire query from the index alone without touching the underlying table blocks, cutting disk I/O in half.

```sql
-- Query:
SELECT user_id, email, status FROM users WHERE status = 'ACTIVE';

-- Covering Index (PostgreSQL INCLUDE clause):
CREATE INDEX idx_users_status_covering ON users (status) INCLUDE (user_id, email);
```

---

### Q8: What is Horizontal Partitioning (Sharding) and how do you choose a Shard Key?

**Answer:**

- **Sharding:** Dividing a single database table horizontally across multiple autonomous database servers (shards), where each server holds a subset of the rows.
- **Selecting an Ideal Shard Key:**
  1. **High Cardinality:** Key must have millions of distinct values (e.g., `user_id` or `uuid`), avoiding low-cardinality keys like `country` or `gender`.
  2. **Uniform Distribution:** Eliminates **Hot Shards** (preventing celebrity accounts like Justin Bieber from overwhelming a single server).
  3. **Colocation:** Sharding by keys that keep related data together on the same physical shard to avoid expensive distributed cross-shard JOINs.

---

### Q9: What are the trade-offs of Range-Based vs Hash-Based vs Directory-Based Sharding?

**Answer:**

| Sharding Strategy | Mechanism | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Range-Based** | Partition by contiguous value ranges (`A-C`, `D-F` or timestamps). | Natural support for range scans. | **Hotspots** on recent dates or active categories. |
| **Hash-Based** | `Shard = Hash(Key) % N`. | Even, uniform data distribution. | Range queries require broadcasting to **all shards** (Scatter-Gather). |
| **Directory-Based** | A central lookup service maps keys to shard IDs. | Flexible; can dynamically move individual partitions. | The lookup directory becomes a Single Point of Failure (SPOF) and latency bottleneck. |

---

### Q10: What is Consistent Hashing and how does it solve the $N$-Node Rehashing Problem?

**Answer:**

- In naive hashing (`Hash(k) % N`), if a node is added or removed ($N \to N+1$), almost **100% of all keys rehash to different servers**, triggering massive cache invalidation storms.
- **Consistent Hashing:**
  1. Maps both servers and cache keys to positions on a circular **360-degree Hash Ring** (e.g. $[0, 2^{32}-1]$).
  2. To locate a key's server, walk clockwise from the key's position until the first server node is reached.
  3. Adding or removing a node only moves keys from its immediate neighbor—on average, only $\frac{1}{N}$ keys are migrated!
  4. **Virtual Nodes (VNodes):** Each physical machine is mapped to multiple positions on the ring (e.g., 256 virtual points), ensuring uniform load distribution even with unequal hardware.

---

### Q11: Explain Caching Strategies: Cache-Aside vs Write-Through vs Write-Back vs Refresh-Ahead

**Answer:**

- **Cache-Aside (Lazy Loading):**
  App reads from cache. On cache miss, app reads from DB, writes to cache, and returns. Most popular pattern; cache only holds requested data.
- **Write-Through:**
  App writes to cache; cache writes to DB **synchronously**. Guarantees data consistency, but write latency includes DB round-trip.
- **Write-Back (Write-Behind):**
  App writes to cache; cache acknowledges immediately and writes to DB **asynchronously in background batches**. Ultra-low write latency, but data loss risk if cache crashes before flushing to DB.
- **Refresh-Ahead:**
  Cache automatically reloads frequently accessed keys before their TTL expires based on access patterns.

---

### Q12: What is a Cache Stampede (Thundering Herd) and how do you prevent it?

**Answer:**

- **Cache Stampede:** Occurs when a high-traffic cache key expires or is invalidated, and thousands of concurrent client requests miss the cache at the same millisecond and hit the backend database simultaneously, crashing the database.
- **Mitigations:**
  1. **Distributed Mutex (Locking):** Only the first request acquires a lock (`SET NX PX` in Redis) to query DB and update cache; other requests wait or retry.
  2. **Probabilistic Early Expiration (XFetch Algorithm):** Recompute key before expiration based on read frequency and computation time:
     $$\text{Recompute if: } -\beta \times \delta \times \ln(\text{random}()) > \text{TTL}$$
  3. **Mutual Exclusion Background Worker:** Never expire keys with hard TTL; use background cron jobs to refresh hot cache entries.

---

### Q13: What is the difference between Cache Eviction Policies: LRU, LFU, and FIFO?

**Answer:**

- **LRU (Least Recently Used):** Discards the item that has not been accessed for the longest period of time (tracks access timestamp / linked list order).
- **LFU (Least Frequently Used):** Discards the item with the lowest access count. Solves the flaw where an old, popular item is evicted due to a sudden burst of one-off scans.
- **FIFO (First-In, First-Out):** Evicts items in the order they were inserted, regardless of access frequency.

---

### Q14: What is Connection Pooling and why is opening DB connections expensive?

**Answer:**

- Establishing a database connection involves: DNS resolution, TCP 3-way handshake, TLS negotiation, authentication credentials verification, and allocating server process memory (often 2-10 MB per connection in PostgreSQL).
- **Connection Pool (HikariCP / PgBouncer):** Maintains a pre-allocated cache of persistent database connections. Applications borrow a connection from the pool, execute their query, and return the connection to the pool without closing the underlying TCP socket.

---

### Q15: What is Database Denormalization and when should you use it?

**Answer:**

- **Denormalization:** Intentionally adding redundant data to database tables to eliminate expensive multi-table JOINs and optimize read query latency.
- **When to Use:** Read-heavy systems (e.g. 100:1 read-to-write ratio) where read latency SLAs (P99 < 20ms) cannot be achieved with normalized relational schemas.
- **Trade-off:** Increases storage space and introduces update anomalies (updating a customer name requires updating multiple denormalized tables or asynchronous background worker synchronization).

---

### Q16: What is the N+1 Query Problem and how do you detect and fix it?

**Answer:**

- Occurs when an ORM queries a parent record, and then executes $N$ separate SQL queries to fetch child relations for each of the $N$ parent records.
  - *Example:* 1 query to fetch 50 orders + 50 individual queries to fetch each order's customer = 51 queries.
- **Fix:** Eager Loading via SQL `JOIN` or `IN` operator:
  `SELECT * FROM customers WHERE id IN (1, 2, 3, ..., 50)`. Reduces 51 network round-trips to exactly 2 queries.

---

### Q17: What are Read Replicas and Replication Lag?

**Answer:**

- **Read Replicas:** Secondary database nodes continuously synchronized with the Primary (Write) database via asynchronous replication of Write-Ahead Logs (WAL).
- **Replication Lag:** The delay between when data is committed on the Primary and when it is applied on the Replica.
- **Impact (Read-Your-Own-Writes Problem):** A user updates their profile, the write goes to Primary, they refresh immediately, and the read hits an out-of-sync Replica, showing their old profile!
- **Fix:** Route reads for recently modified data to the Primary for a short grace window (e.g. 5 seconds), or track replication lag LSNs (Log Sequence Numbers).

---

### Q18: What is Layer 4 vs Layer 7 Load Balancing?

**Answer:**

- **Layer 4 (Transport Layer - TCP/UDP):**
  - Routes traffic based on IP address and TCP port alone without inspecting payload.
  - High performance, minimal CPU overhead. Cannot inspect HTTP headers, cookies, or URL paths.
  - *Examples:* AWS Network Load Balancer (NLB), HAProxy (TCP mode).
- **Layer 7 (Application Layer - HTTP/HTTPS/gRPC):**
  - Terminates TLS, parses HTTP headers, inspects URL paths (`/api/v1` vs `/static`), and evaluates session cookies.
  - Enables intelligent content-based routing, header rewrites, and WebSocket upgrades.
  - *Examples:* AWS Application Load Balancer (ALB), NGINX, Envoy.

---

### Q19: What Load Balancing Algorithms exist and when do you use each?

**Answer:**

1. **Round Robin:** Sequential rotation across instances. Best for stateless servers with identical hardware and equal request durations.
2. **Weighted Round Robin:** Assigns higher request shares to more powerful server nodes.
3. **Least Connections:** Routes to the server with the fewest active TCP connections. Ideal for long-lived connections (WebSockets, database pools).
4. **IP Hash:** Hashes client IP to bind requests from a user to the same backend server (Session Stickiness).
5. **Least Response Time:** Routes traffic to the server responding with the lowest latency.

---

### Q20: What is Database Index Cardinality and Selective Indexing?

**Answer:**

- **Cardinality:** The number of unique values in a table column relative to the total number of rows.
  - *High Cardinality:* `user_id`, `email`, `uuid` (unique values per row). Excellent candidates for B+Tree indexes.
  - *Low Cardinality:* `gender`, `is_active`, `status` (only 2-5 unique values across millions of rows).
- **Why Low Cardinality Indexes Fail:** If a column has only 2 unique values (50/50 split), traversing a secondary index and performing millions of random bookmark lookups is much slower than a sequential Full Table Scan. Use **Partial Indexes** (`WHERE status = 'FAILED'`) or Bitmap Indexes instead.
