# System Design Master Cheat Sheet: Numbers, Formulas, Patterns & Matrices

> The ultimate rapid-recall architecture and capacity estimation cheat sheet for Senior and Staff System Design interviews.

---

## 📊 1. Latency Numbers Every Systems Architect Must Know

| Operation | Latency (Normalized) | Human Analogy Equivalent |
| :--- | :---: | :---: |
| **L1 CPU Cache Reference** | $0.5 \text{ ns}$ | 1 heartbeat (0.5 sec) |
| **Branch Mispredict** | $5 \text{ ns}$ | 10 seconds |
| **L2 CPU Cache Reference** | $7 \text{ ns}$ | 14 seconds |
| **Mutex Lock / Unlock** | $25 \text{ ns}$ | 50 seconds |
| **Main Memory (RAM) Reference** | $100 \text{ ns}$ | 3.3 minutes |
| **Compress 1KB with Zstandard** | $2,000 \text{ ns}$ ($2 \text{ µs}$) | 1 hour |
| **Read 1MB Sequentially from Memory** | $3,000 \text{ ns}$ ($3 \text{ µs}$) | 1.5 hours |
| **Round Trip inside Same Datacenter** | $500,000 \text{ ns}$ ($0.5 \text{ ms}$) | 6 days |
| **Read 1MB Sequentially from NVMe SSD**| $1,000,000 \text{ ns}$ ($1 \text{ ms}$) | 12 days |
| **Read 1MB Sequentially from Magnetic Disk**| $20,000,000 \text{ ns}$ ($20 \text{ ms}$) | 8 months |
| **Internet Packet: California to Netherlands**| $150,000,000 \text{ ns}$ ($150 \text{ ms}$) | 5 years |
| **OS TCP Retransmit Timeout** | $1,000,000,000 \text{ ns}$ ($1 \text{ s}$) | 32 years |

> **Key Senior Architectural Takeaway**: Memory is $1,000\times$ faster than NVMe SSD, and NVMe SSD is $20\times$ faster than spinning disk. Network crossing oceans takes centuries compared to CPU cycles. **Always design around caching and sequential memory access!**

---

## 🔢 2. Back-of-the-Envelope Capacity Estimation Formulas

### Rule of Thumb Conversions:
- $1 \text{ Day} \approx 86,400 \text{ seconds} \approx 10^5 \text{ seconds}$ (simplifies mental math).
- $1 \text{ Million Requests/Day} \approx \frac{10^6}{86,400} \approx \mathbf{12 \text{ QPS}}$ (Queries Per Second).
- $10 \text{ Million Requests/Day} \approx \mathbf{120 \text{ QPS}}$.
- $100 \text{ Million Requests/Day} \approx \mathbf{1,200 \text{ QPS}}$.
- $1 \text{ Billion Requests/Day} \approx \mathbf{12,000 \text{ QPS}}$.

### Peak Traffic Multiplier:
- $\text{Peak QPS} = \text{Average QPS} \times 2 \text{ to } 5$ (typically assume $2.5\times$ for consumer apps).

### Storage Sizing Formula:
$$\text{Storage per Day} = \text{Daily Writes} \times \text{Average Payload Size}$$
$$\text{Storage (5 Years)} = \text{Storage per Day} \times 365 \times 5 \times (\text{Replication Factor: } 3)$$

### Memory Cache Sizing (The 80/20 Pareto Principle):
- $20\%$ of daily read requests generate $80\%$ of total read volume.
- $\text{RAM Cache Required} = \text{Daily Active Read Volume} \times 20\%$.

---

## ⚖️ 3. Fundamental Distributed Theorems & Laws

### 1. CAP Theorem (Brewer)
In any asynchronous network experiencing a Network Partition ($P$):
- **CP (Consistency + Partition Tolerance)**: Reject writes if replicas cannot reach quorum (e.g., HBase, Spanner, ZooKeeper, etcd).
- **AP (Availability + Partition Tolerance)**: Accept writes on any available node; reconcile later via eventual consistency (e.g., Cassandra, DynamoDB, CouchDB).
- *Note: "CA" systems do not exist in distributed cloud networks because network partitions are physically inevitable.*

### 2. PACELC Theorem (Abadi)
Extends CAP for normal non-partition operating states:
- **If Partition ($P$)**: Choose Availability ($A$) or Consistency ($C$).
- **Else ($E$)**: Choose Latency ($L$) or Consistency ($C$).
- *Examples*:
  - **DynamoDB / Cassandra**: $PA / EL$ (Favors Availability under partition, favors low Latency normally).
  - **Spanner / HBase**: $PC / EC$ (Favors Consistency under partition, favors Consistency normally at cost of latency).
  - **MongoDB**: $PC / EC$ (Default) or $PA / EL$ (with read preference `nearest`).

### 3. Little's Law
$$L = \lambda \times W$$
- $L$ = Average number of concurrent requests in the system.
- $\lambda$ = Arrival rate (Requests Per Second - RPS).
- $W$ = Average latency / processing time per request (seconds).
- *Application*: If your API handles $2,000 \text{ RPS}$ and average latency is $0.1 \text{ s}$ ($100\text{ms}$), your server must support $2000 \times 0.1 = \mathbf{200 \text{ concurrent connections}}$ without thread starvation.

---

## 🗄️ 4. Database Selection Decision Matrix

| Database Type | Best Fit Technologies | Primary Use Case | Scaling Mechanism | Key Bottleneck / Pitfall |
| :--- | :--- | :--- | :--- | :--- |
| **Relational (RDBMS)** | PostgreSQL, MySQL | Financial ledgers, ACID transactions, complex joins | Vertical scale-up, read replicas, declarative sharding | Complex distributed joins across shards |
| **Document NoSQL** | MongoDB, Couchbase | Catalogs, polymorphic user profiles, JSON schemas | Horizontal auto-sharding via shard key | No multi-document cross-collection ACID locks (pre-v4) |
| **Wide-Column NoSQL** | Apache Cassandra, ScyllaDB | High-write time-series, IoT telemetry, chat histories | Consistent hashing masterless ring ($O(1)$ writes) | Query patterns must strictly match partition key |
| **Key-Value In-Memory**| Redis, Dragonfly, KeyDB | Session store, rate limiting, leaderboards, hot caches | In-memory RAM, Redis Cluster hash slots | RAM cost, data loss if persistence not tuned |
| **Search Engine** | Elasticsearch, OpenSearch | Full-text search, log aggregation, fuzzy matching | Inverted indexes, distributed shards | High RAM overhead for heap & fielddata |
| **Vector Database** | Qdrant, Pinecone, Milvus | AI embeddings, semantic search, RAG retrieval | HNSW graphs, IVF-PQ quantization | High memory consumption for raw graph traversal |
| **Graph Database** | Neo4j, Amazon Neptune | Social networks, fraud detection rings, knowledge graphs | Index-free adjacency pointer chasing | Difficult to partition across multi-node clusters |

---

## ⚡ 5. Caching & Eviction Matrix

| Pattern | Write Path | Read Path | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Cache-Aside (Lazy)** | App writes directly to DB, deletes/invalidates cache key | App reads cache; on miss, queries DB and populates cache | Memory efficient; handles node failures gracefully | Cache miss latency spike; stale data if updates fail |
| **Write-Through** | App writes to Cache; Cache synchronously writes to DB | App reads exclusively from Cache | Cache is always consistent with DB | Higher write latency (two round trips per write) |
| **Write-Behind (Write-Back)** | App writes to Cache immediately; Cache buffers and batch writes to DB asynchronously | App reads from Cache | Ultra-low write latency; absorbs massive write spikes | Risk of data loss if cache crashes before DB flush |
| **Refresh-Ahead** | Standard write | Cache automatically re-fetches hot keys from DB before TTL expires | Zero cache-miss latency for hot keys | Inaccurate prediction algorithms waste DB bandwidth |

---

## 🛡️ 6. Distributed Stability & Resilience Patterns

1. **Circuit Breaker Pattern**:
   - **Closed**: Requests pass normally.
   - **Open**: When failure rate exceeds threshold (e.g., $50\%$), calls fail-fast immediately without touching downstream server.
   - **Half-Open**: Periodically allows probe requests. If successful, resets to Closed; if failing, trips back to Open.
2. **Bulkhead Pattern**: Isolates thread pools, memory, and database connection pools by client or tenant so failure in one tenant cannot consume all system resources.
3. **Exponential Backoff with Full Jitter**:
   $$\text{Sleep} = \text{random}(0, \min(\text{Cap}, \text{Base} \times 2^{\text{attempt}}))$$
   Full random jitter breaks phase synchronization, preventing the "Thundering Herd" from crashing recovering databases.
4. **Transactional Outbox Pattern**: Solves dual-write problems between Database and Message Broker (Kafka/RabbitMQ). Writes business data and outbound message to the *same* database transaction, while a Debezium CDC (Change Data Capture) worker tails the WAL to reliably publish to Kafka with zero data loss.
5. **Saga Pattern (Choreography vs Orchestration)**:
   - Manages distributed multi-microservice transactions without two-phase commit (2PC) locking.
   - Every local transaction has an accompanying **Compensating Transaction** (e.g., `cancelPayment()`) executed in reverse order if a downstream step fails.
