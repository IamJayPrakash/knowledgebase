# -*- coding: utf-8 -*-
"""
Generator for Comprehensive 50 System Design Concepts & Advanced System Design Suites
Generates:
1. 13-system-design/00_master_50_system_design_concepts.md
2. 13-system-design/07_distributed_systems_primitives_consensus_cap_sharding.md
3. 13-system-design/08_resilience_and_stability_patterns.md
4. 13-system-design/09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md
5. 13-system-design/10_event_driven_streaming_batch_mapreduce.md
6. 13-system-design/11_observability_deployments_bluegreen_canary.md
7. 13-system-design/interview-questions/top_system_design_interview_questions_catalog.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "13-system-design", "00_master_50_system_design_concepts.md"): """# The Master 50 System Design Concepts Playbook

> A definitive architectural reference covering all **50 Fundamental System Design Concepts** based on industry-standard distributed systems engineering.

---

## 🗺️ Visual Architecture Map (All 50 Concepts)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 50 SYSTEM DESIGN CONCEPTS                              │
├────────────────────────────┬────────────────────────────┬───────────────────────────────┤
│ 1. Core Architecture       │ 2. Storage & Data Models   │ 3. Distributed Primitives     │
│  - Scalability (#8)        │  - Database (#1)           │  - CAP Theorem (#13)          │
│  - Availability (#3)       │  - SQL vs NoSQL (#2)       │  - Consensus (#19)            │
│  - High Availability (#12) │  - ACID (#30)              │  - Leader Election (#18)      │
│  - Reliability (#4)        │  - Indexing (#17)          │  - Consistency Models (#20)   │
│  - Fault Tolerance (#11)   │  - Sharding (#16)          │  - Erasure Coding (#33)       │
│  - Latency (#5)            │  - Denormalization (#24)   │  - Service Discovery (#34)    │
│                            │  - Query Optimization (#41)│                               │
│                            │  - LSM Trees (#48)         │                               │
├────────────────────────────┼────────────────────────────┼───────────────────────────────┤
│ 4. Communication & APIs    │ 5. Traffic & Caching       │ 6. Messaging & Pipelines      │
│  - API Design (#6)         │  - Load Balancing (#9)     │  - Sync vs Async (#35)        │
│  - REST (#7)               │  - Caching (#10)           │  - Event-Driven (#21)         │
│  - GraphQL (#14)           │  - Cache Stampede (#43)    │  - Message Queue (#22)        │
│  - gRPC (#15)              │  - Connection Pooling (#38)│  - Pub/Sub (#23)              │
│  - WebSockets (#42)        │                            │  - Stream Processing (#50)    │
│  - WebRTC (#45)            │                            │  - Batch Processing (#49)     │
│  - BFF (#37)               │                            │  - MapReduce (#44)            │
│  - Deserialization (#46)   │                            │                               │
├────────────────────────────┼────────────────────────────┴───────────────────────────────┤
│ 7. Resilience & Patterns   │ 8. Observability & Deployments                             │
│  - Bulkhead (#26)          │  - Correlation ID (#36)                                    │
│  - Timeout (#28)           │  - Monitoring (#39) & Alerting (#40)                       │
│  - Retry Logic (#27)       │  - Blue-Green Deployment (#31)                             │
│  - Feature Flags (#29)     │  - Canary Release (#32)                                    │
│  - Strangler Pattern (#47) │  - Secrets Management (#25)                                │
└────────────────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 📚 Detailed Encyclopedia of All 50 Concepts

### 1. Database
- **ELI5**: Digital filing cabinet storing organized structured data.
- **Under the Hood**: Storage engine (e.g. InnoDB, WiredTiger) managing page cache, B-Trees/LSM trees, Write-Ahead Logs (WAL), and disk synchronization.

### 2. SQL vs NoSQL
- **SQL (Relational)**: Structured tables, fixed schema, ACID compliance, complex relational joins. Scaled vertically.
- **NoSQL (Non-relational)**: Document, Key-Value, Wide-column, Graph. Flexible schema, BASE model, high horizontal write throughput.

### 3. Availability
- **ELI5**: Percentage of time a system remains operational and responds to requests.
- **Formula**: `Availability = Uptime / (Uptime + Downtime)`. "Four Nines" (99.99%) allows only 52.6 minutes of downtime per year.

### 4. Reliability
- **ELI5**: Probability that a system will perform its function correctly without failure over a given duration.
- **Key Metric**: Mean Time Between Failures (MTBF) and Mean Time to Recovery (MTTR).

### 5. Latency
- **ELI5**: Time elapsed between initiating a request and receiving the response.
- **Metrics**: Measure P50 (median), P95, P99, and P99.9 latencies. Focus on tail latency rather than average.

### 6. API Design
- **Core Principles**: Clear contracts, backward compatibility, idempotency, proper HTTP status codes, versioning (`/v1/`), rate-limiting headers.

### 7. REST (Representational State Transfer)
- **Architecture**: Stateless, client-server, cacheable, uniform interface over standard HTTP verbs (GET, POST, PUT, PATCH, DELETE).

### 8. Scalability
- **Vertical (Scale Up)**: Adding CPU, RAM, or SSDs to a single server. Hardware ceiling, single point of failure (SPOF).
- **Horizontal (Scale Out)**: Adding more commodity nodes to a distributed cluster behind a load balancer.

### 9. Load Balancing
- **Function**: Distributes incoming network traffic across multiple backend servers.
- **Algorithms**: Round Robin, Weighted Round Robin, Least Connections, Consistent Hashing, IP Hash. Layer 4 (TCP/UDP) vs Layer 7 (HTTP/Application).

### 10. Caching
- **Function**: Storing expensive computation or database query results in fast volatile memory (RAM).
- **Patterns**: Cache-Aside (Lazy Loading), Write-Through, Write-Behind (Write-Back), Refresh-Ahead.

### 11. Fault Tolerance
- **Function**: System's ability to continue operating properly without interruption despite the failure of one or more components.

### 12. High Availability (HA)
- **Mechanics**: Redundant components across multiple Availability Zones (AZs), automated health checks, seamless failover (active-passive or active-active).

### 13. CAP Theorem
- **Rule**: In a distributed data store experiencing a Network Partition (P), you MUST choose between Consistency (C) and Availability (A). You cannot have both.

### 14. GraphQL
- **Function**: Declarative query language for APIs. Client specifies exact fields required, eliminating over-fetching and under-fetching with a single endpoint (`/graphql`).

### 15. gRPC
- **Function**: High-performance RPC framework developed by Google. Uses Protocol Buffers (Protobuf) binary serialization over HTTP/2 multiplexed streams.

### 16. Sharding
- **Function**: Horizontally partitioning a database table into smaller subsets (shards) across multiple database servers.
- **Strategies**: Range-based, Hash-based (Consistent Hashing), Directory-based.

### 17. Indexing
- **Function**: Auxilliary data structure (B-Tree, Hash, GIN, BRIN) improving read query performance at the cost of additional write latency and disk space.

### 18. Leader Election
- **Function**: Selecting a designated coordinator node among a distributed group to prevent split-brain conflicts (e.g. via ZooKeeper, etcd, Bully Algorithm).

### 19. Consensus
- **Function**: Agreement on a single data value among distributed processes despite network delays or node crashes.
- **Algorithms**: Paxos, Raft.

### 20. Consistency Models
- **Spectrum**: Strict Serializability -> Linearizability -> Sequential Consistency -> Causal Consistency -> Eventual Consistency.

### 21. Event-Driven Architecture
- **Function**: Decoupled systems communicating asynchronously through the production, detection, and consumption of state-change events.

### 22. Message Queue
- **Function**: Point-to-point asynchronous FIFO queue where messages are consumed by a single worker (RabbitMQ, SQS).

### 23. Pub/Sub (Publish/Subscribe)
- **Function**: One-to-many broadcast messaging pattern where publishers broadcast to topics and multiple subscribers receive copies (Kafka, Google Cloud Pub/Sub).

### 24. Denormalization
- **Function**: Intentionally adding redundant data copies to relational models to avoid expensive SQL `JOIN` operations on high-read paths.

### 25. Secrets Management
- **Function**: Secure storage, dynamic rotation, and access control for API keys, passwords, and TLS certificates (HashiCorp Vault, AWS Secrets Manager).

### 26. Bulkhead Pattern
- **Function**: Isolating system resources (thread pools, memory, sockets) into distinct pools so failure in one client or downstream service does not sink the entire system.

### 27. Retry Logic
- **Function**: Automatically re-attempting failed network calls using **Exponential Backoff with Full Jitter** to prevent overwhelming recovering servers.

### 28. Timeout
- **Function**: Enforcing strict maximum elapsed time boundaries on outbound network calls to prevent thread pool starvation.

### 29. Feature Flags
- **Function**: Decoupling code deployment from feature release, enabling dynamic runtime feature toggles and dark launches.

### 30. ACID
- **Atomicity**: All operations succeed or all roll back.
- **Consistency**: Transitions database from one valid state to another.
- **Isolation**: Concurrent transactions do not interfere with each other.
- **Durability**: Committed data survives system crashes (WAL).

### 31. Blue-Green Deployment
- **Mechanics**: Two identical production environments. Blue runs current live traffic; Green receives new code. Router flips traffic to Green once verified (0 downtime, instant rollback).

### 32. Canary Release
- **Mechanics**: Gradually routing a small percentage of production traffic (e.g. 5%) to new version, monitoring error rates, then progressively ramping to 100%.

### 33. Erasure Coding
- **Function**: Data protection method that breaks data into fragments, expands and encodes with redundant parity data, and stores across different locations. Requires significantly less storage overhead than 3x replication.

### 34. Service Discovery
- **Function**: Automated detection of dynamic IP addresses and ports assigned to microservice instances (Consul, Eureka, Kubernetes DNS).

### 35. Synchronous vs Asynchronous Communication
- **Synchronous**: Caller blocks waiting for response (HTTP/REST, gRPC).
- **Asynchronous**: Caller initiates request and resumes immediately; response handled via callbacks or event buses (Kafka, RabbitMQ).

### 36. Correlation ID
- **Function**: Unique identifier injected into incoming HTTP request headers (`x-correlation-id`) and propagated across all downstream microservices and logs for distributed tracing.

### 37. BFF (Backend for Frontend)
- **Function**: Dedicated backend layer tailored specifically to the needs of a single user interface (e.g., Mobile BFF vs Desktop Web BFF).

### 38. Connection Pooling
- **Function**: Maintaining a cache of pre-established database connections to eliminate the expensive TCP/TLS handshake latency on every query.

### 39. Monitoring & 40. Alerting
- **Metrics (Prometheus)**: Counter, Gauge, Histogram.
- **Alerting (Alertmanager)**: Threshold and anomaly-based alerting to PagerDuty/Slack based on Service Level Objectives (SLOs).

### 41. Query Optimization
- **Mechanics**: Analyzing query execution plans (`EXPLAIN ANALYZE`), preventing N+1 queries, selecting covering indexes, avoiding SELECT *.

### 42. WebSockets
- **Function**: Full-duplex, persistent bidirectional TCP connection over a single socket handshake. Ideal for live chats and financial tickers.

### 43. Cache Stampede (Thundering Herd)
- **Problem**: When a popular cache key expires, thousands of concurrent requests simultaneously hit the database to recompute it.
- **Fix**: Probabilistic early expiration (XFetch algorithm) or distributed mutex locking.

### 44. MapReduce
- **Function**: Distributed data processing paradigm: Map (filter and transform data in parallel) and Reduce (aggregate and synthesize results).

### 45. WebRTC
- **Function**: Real-time peer-to-peer audio, video, and data streaming between browsers with sub-second latency using STUN/TURN servers.

### 46. Deserialization
- **Function**: Converting bytes, JSON, or XML back into runtime in-memory objects. Vulnerability vector if unvalidated (Remote Code Execution).

### 47. Strangler Fig Pattern
- **Function**: Incrementally migrating a legacy monolithic application to microservices by replacing specific features piece by piece until the monolith is retired.

### 48. LSM Trees (Log-Structured Merge-Trees)
- **Function**: High-write-throughput storage engine structure (used by Cassandra, RocksDB) that buffers writes in a memory MemTable and flushes sequentially to immutable disk SSTables.

### 49. Batch Processing
- **Function**: Processing large volumes of static, historical data in non-real-time scheduled jobs (Apache Spark, Hadoop).

### 50. Stream Processing
- **Function**: Ingesting, transforming, and analyzing unbounded streams of data in real-time with millisecond latencies (Apache Flink, Kafka Streams).
""",

    os.path.join(BASE_DIR, "13-system-design", "07_distributed_systems_primitives_consensus_cap_sharding.md"): """# Distributed Systems Primitives: CAP Theorem, Raft Consensus, and Consistent Hashing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**CAP Theorem**: Socho do dost hain (Server A aur Server B). Beech ka telephone taar toot gaya (**Network Partition**). Ab agar ek customer Server A par aakar balance update karta hai, toh ya toh Server A update accept karega lekin Server B ko nahi pata hoga (**Availability jeeti, Consistency haari - AP**), ya fir Server A customer ko mana kar dega: "Phone line kharab hai, transaction cancelled!" (**Consistency jeeti, Availability haari - CP**)!
**Consistent Hashing**: Ek **Gol Ring (Round Dining Table)** ki tarah hai. Jab naya dost khane par aata hai, toh sabko apni kursi chhod kar nayi jagah nahi baithna padta; sirf ek padosi ki plate se thoda sa khana share hota hai!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **CAP Theorem in Reality**:
   - Network partitions ($P$) are inevitable in physical distributed networks (switch failures, fiber cuts).
   - Therefore, system design is a choice between **CP** (Consistent under Partition) and **AP** (Available under Partition).
   - CA (Consistent + Available without Partition) cannot exist across physical networks.
2. **PACELC Theorem**:
   - Expands CAP: **If Partition ($P$)**: choose Availability ($A$) vs Consistency ($C$); **Else ($E$)**: choose Latency ($L$) vs Consistency ($C$).
3. **Consensus Algorithms (Raft)**:
   - Three roles: Leader, Follower, Candidate.
   - Leader handles all client writes, appends log entries, and broadcasts `AppendEntries` RPCs.
   - Quorum rule: Requires majority $\lfloor N/2 \rfloor + 1$ acknowledgments to commit.
4. **Consistent Hashing**:
   - Maps both servers and keys onto a $2^{32} - 1$ hash ring.
   - Adding or removing a server node only relocates $K/N$ keys on average.
   - **Virtual Nodes (vnodes)**: Distribute each physical server across 100-256 virtual points on the ring, guaranteeing uniform data distribution.

---

## 📊 3. Visual Architecture Diagram

```
                 CONSISTENT HASHING VIRTUAL NODE RING
                 
                         [ Server A (v1) ]
                            0 / 2^32-1
                           /           |
         [ Server C (v2) ]             [ Server B (v1) ]
                 |                             |
                 |      KEY HASH PLACEMENT     |
                 |      key1 ──► Server B      |
                 |      key2 ──► Server C      |
                 |                             |
         [ Server B (v2) ]             [ Server A (v2) ]
                           |           /
                         [ Server C (v1) ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets (Python Consistent Hashing)

```python
import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, replicas: int = 100):
        # Line 6: Number of virtual nodes per physical node
        self.replicas = replicas
        # Line 8: Sorted list of virtual node hashes on the ring
        self.ring = []
        # Line 10: Hash -> Physical node name map
        self.hash_to_node = {}

    def _hash(self, key: str) -> int:
        # Generate 32-bit integer hash from MD5 digest
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16) & 0xFFFFFFFF

    def add_node(self, node: str):
        # Line 17: Place multiple virtual nodes across the ring
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            vnode_hash = self._hash(vnode_key)
            bisect.insort(self.ring, vnode_hash)
            self.hash_to_node[vnode_hash] = node

    def remove_node(self, node: str):
        # Remove all virtual replicas of node
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            vnode_hash = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, vnode_hash)
            if idx < len(self.ring) and self.ring[idx] == vnode_hash:
                del self.ring[idx]
                del self.hash_to_node[vnode_hash]

    def get_node(self, key: str) -> str:
        if not self.ring:
            return None

        # Line 37: Hash the target key and binary search the clockwise successor node
        key_hash = self._hash(key)
        idx = bisect.bisect_right(self.ring, key_hash)

        # If key_hash is beyond the last node, wrap around to index 0 (Ring behavior)
        if idx == len(self.ring):
            idx = 0

        return self.hash_to_node[self.ring[idx]]

# Verification:
ring = ConsistentHashRing(replicas=150)
ring.add_node("cache-node-1")
ring.add_node("cache-node-2")
ring.add_node("cache-node-3")

print("Routing user_101:", ring.get_node("user_101"))
print("Routing user_102:", ring.get_node("user_102"))
```

---

## 🎯 5. The "Interview Pitch"
> "In distributed data systems, Consistent Hashing is the cornerstone of horizontal data partitioning and caching tiers. Unlike traditional modular hashing (`hash(key) % N`) where adding a single server invalidates $100\%$ of mapped keys and causes a devastating cache stampede, consistent hashing places both nodes and keys on a circular hash space. Adding or removing a node relocates only $K/N$ keys. We assign virtual nodes to each physical server to eliminate hot-spotting and ensure uniform key distribution across asymmetric hardware."
""",

    os.path.join(BASE_DIR, "13-system-design", "08_resilience_and_stability_patterns.md"): """# System Resilience Patterns: Bulkhead, Timeouts, Retries with Jitter, and Cache Stampede Mitigation

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Bulkhead Pattern** Titanic ship ke **Alag-Alag Compartments** jaisa hai: Agar ship ke aage wale room mein paani bhar jaye, toh darwaze band ho jate hain taaki baaki ship na dube (**Compartmentalized Thread Pools**).
**Retry with Jitter**: Agar ek darwaza band hai aur 10,000 log ek hi second mein dobara dhakka marenge, toh darwaza toot jayega (**Thundering Herd**). Jitter har bande ko bolta hai: "Koi 1 second baad aao, koi 1.8 second baad, koi 2.5 second baad" (Randomized Backoff).
**Cache Stampede (XFetch)**: Restaurant ka soup khatam hone se 5 minute pehle hi chef naya soup banana shuru kar deta hai taaki customer ko kabhi "Khana khatam ho gaya" na sunna pade!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Danger of Plain Retries**: Retrying immediately or on a fixed interval causes a **Retry Storm**, turning minor transient blips into complete catastrophic cascading outages.
2. **Full Jitter Algorithm (AWS Standard)**:
   `sleep = random_between(0, min(cap, base * 2 ** attempt))`.
3. **Bulkhead Isolation**:
   - Separate thread pools and connection pools per downstream dependency.
   - If Service C hangs, only Service C's thread pool exhausts; Service A and B continue serving users unimpeded.
4. **Cache Stampede Mitigation via XFetch Algorithm**:
   - Rather than waiting for TTL to reach zero, worker threads compute a probabilistic early refresh:
   - Refresh if: `currentTime - (delta * beta * log(random())) > expiryTime`.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
import time
import random
import math

# Line 5: Production Retry with Exponential Backoff and Full Jitter
def execute_with_full_jitter(operation, max_retries=5, base_delay=0.1, max_delay=3.0):
    attempt = 0
    while attempt < max_retries:
        try:
            return operation()
        except Exception as e:
            attempt += 1
            if attempt >= max_retries:
                raise e

            # Line 16: Exponential factor calculation
            backoff = min(max_delay, base_delay * (2 ** attempt))
            # Line 18: Full Jitter: Uniform random duration between 0 and backoff
            sleep_duration = random.uniform(0, backoff)
            print(f"[Retry {attempt}] Network call failed. Sleeping {sleep_duration:.3f}s (Jittered Backoff)...")
            time.sleep(sleep_duration)

# Line 24: XFetch Probabilistic Early Cache Refresh Algorithm
def xfetch_should_refresh(last_compute_time_sec: float, expiry_timestamp: float, beta: float = 1.0) -> bool:
    '''
    last_compute_time_sec (delta): Time it takes to recompute the value from DB
    expiry_timestamp: Exact UNIX timestamp when the cache key expires
    beta: Aggressiveness factor (> 0, default 1.0)
    '''
    now = time.time()
    # Random probability float between 0.0 and 1.0
    u = random.random()
    # If delta * beta * -log(u) exceeds time remaining, asynchronously refresh cache early!
    return (now - (last_compute_time_sec * beta * math.log(u))) > expiry_timestamp
```

---

## 🎯 4. The "Interview Pitch"
> "Building highly available distributed systems requires designing for failure as a first-class citizen. Standard retries without randomized jitter create devastating retry storms on recovering databases. We implement Exponential Backoff with Full Jitter to decouple retrying clients. Furthermore, we deploy the Bulkhead pattern using isolated thread pools per microservice dependency, preventing a slow third-party API from exhausting the global worker thread pool and stalling healthy endpoints. Finally, to eliminate Cache Stampedes where millions of concurrent requests hit the database upon cache key expiration, we employ probabilistic early expiration using the XFetch algorithm."
""",

    os.path.join(BASE_DIR, "13-system-design", "09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md"): """# Distributed Communication Protocols: REST, GraphQL, gRPC, WebSockets, and WebRTC

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
- **REST**: Ek **Post Office Letter** hai: Standard format hai, sab samajhte hain, lekin har letter ka alag envelope hota hai.
- **GraphQL**: Ek **Custom Thali Restaurant** hai: Customer menu card par tick karta hai: "Mujhe sirf 2 roti aur 1 daal chahiye, baaki sab hata do" (Zero over-fetching).
- **gRPC**: Ek **High-Speed Binary Telegram** hai: Human text nahi bhejta, compact zero-and-one binary stream bhejta hai jo 10x fast travel karti hai.
- **WebSockets**: Ek **Open Telephone Call** hai: Dono taraf se log ek sath bol sakte hain (Full Duplex).
- **WebRTC**: Ek **Walkie-Talkie Walk-In** hai: Server ke bina do mobile seedhe aapas mein audio/video stream share karte hain (Peer-to-Peer).

---

## 📌 2. Master Protocol Decision Matrix

| Protocol | Transport | Serialization | Duplex | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **REST** | HTTP/1.1, HTTP/2 | JSON, XML | Request/Response | Public APIs, CRUD services |
| **GraphQL**| HTTP/1.1, HTTP/2 | JSON | Request/Response | Complex UI aggregation, Mobile apps |
| **gRPC** | HTTP/2 Multiplexed | Protocol Buffers (Binary) | Bi-directional streaming | Internal microservice-to-microservice RPC |
| **WebSockets**| TCP (Upgraded HTTP) | Text / Binary | Full-Duplex | Live chats, collaborative whiteboards, stock tickers |
| **WebRTC** | UDP (RTP/SRTP) | Raw Audio/Video/Data | Peer-to-Peer Full Duplex | Video calls (Zoom/Google Meet), P2P gaming |

---

## 📊 3. Visual Architecture Diagram

```
                 COMMUNICATION TOPOLOGIES
                 
   [ Client App ] ──(HTTP/2 REST/GraphQL)──► [ API Gateway ]
                                                    │
                              ┌─────────────────────┴─────────────────────┐
                              ▼                                           ▼
                     (Internal gRPC Protobuf)                    (Internal gRPC Protobuf)
                              ▼                                           ▼
                     [ Microservice A ] ◄──────(gRPC)────────► [ Microservice B ]
```
""",

    os.path.join(BASE_DIR, "13-system-design", "10_event_driven_streaming_batch_mapreduce.md"): """# Event-Driven Architecture, Stream Processing, and MapReduce

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Batch Processing (MapReduce)** ek **Mahine Ke Akhir Ka Electricity Bill** hai: Poore 30 din ka data jama hota hai, raat ko ek sath calculate hota hai aur subah bill nikalta hai.
**Stream Processing (Kafka / Flink)** ek **Live Electric Meter Counter** hai: Jaise hi aapne fan on kiya, meter ka pahiya ghoomta hai aur live reading reflect hoti hai (Millisecond real-time event calculation).
**Exactly-Once Processing**: Banking ATM jaisa hai: Chahe network disconnect ho jaye, aapke account se paisa do baar deduct nahi hoga.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Message Queue vs Event Stream**:
   - Queue (RabbitMQ): Messages deleted immediately after worker acknowledgment (ACK).
   - Event Stream (Kafka): Append-only immutable commit log retained on disk for days/months; consumers track their own offsets.
2. **Delivery Semantics**:
   - **At-Most-Once**: Message delivered 0 or 1 time (messages may be lost).
   - **At-Least-Once**: Message delivered 1 or more times (requires consumer idempotency).
   - **Exactly-Once**: Transactional coordination between producer, log, and consumer state (Kafka Transactions + 2-Phase Commit).
3. **Kappa vs Lambda Architecture**:
   - **Lambda**: Parallel Batch layer (Hadoop) for accuracy + Speed layer (Storm) for low latency. High maintenance.
   - **Kappa**: Single Stream processing layer (Flink/Kafka) for all real-time and historical re-processing.

---

## 💻 3. Line-by-Line Commented Code Snippets (Idempotent Consumer Pattern)

```python
# Production Idempotent Kafka Consumer Pattern
def process_payment_event(event: dict, redis_client, db_connection):
    event_id = event["event_id"]
    order_id = event["order_id"]
    amount = event["amount"]

    # Line 7: Atomically set event ID in Redis with 24-hour TTL to verify idempotency
    # SETNX returns 1 if key was set, 0 if already processed!
    is_new = redis_client.set(f"processed_event:{event_id}", "1", nx=True, ex=86400)

    if not is_new:
        print(f"[Duplicate Ignored] Event {event_id} already processed. Skipping.")
        return

    # Line 15: Safe to execute database mutation
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("UPDATE orders SET payment_status = 'PAID' WHERE id = %s", (order_id,))
            db_connection.commit()
            print(f"[Success] Order {order_id} marked as PAID.")
    except Exception as err:
        # Revert Redis key if DB fails so message can be retried safely
        redis_client.delete(f"processed_event:{event_id}")
        raise err
```
""",

    os.path.join(BASE_DIR, "13-system-design", "11_observability_deployments_bluegreen_canary.md"): """# Observability, Distributed Tracing, and Deployment Strategies

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Correlation ID**: Ek **Hospital Patient Token Number** ki tarah hai: Jab mareez hospital aata hai, use Token #42 milta hai. Doctor, Blood Test Lab, X-Ray room, aur Pharmacy sabhi register mein sirf Token #42 likhte hain. Agar koi gadbad hoti hai, toh Token #42 search karte hi poora rasta pata chal jata hai (**Distributed Tracing**).
**Canary Release**: Purane zamane mein koyla khadan (Coal mine) mein gas leak test karne ke liye choti **Canary Bird** le jaate the. Agar bird safe rahi, toh workers andar jaate the. Software mein 5% traffic naye version par bhejte hain; agar error rate zero raha, tabhi baaki 95% traffic switch karte hain!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Three Pillars of Observability**:
   - **Metrics**: Aggregatable numeric time-series data (Prometheus: QPS, CPU %, Latency).
   - **Logs**: Detailed event records with timestamp and context (ELK, Loki).
   - **Traces**: End-to-end request journeys across distributed microservices (OpenTelemetry, Jaeger).
2. **Deployment Comparison**:
   - **Recreate**: Kill old pods, launch new pods (downtime occurs).
   - **Rolling Update**: Incrementally replace pods one by one (no downtime, but mixed version traffic).
   - **Blue-Green**: Two isolated identical production environments; router flips instantly (zero downtime, instantaneous rollback).
   - **Canary**: Progressive traffic shifting (5% -> 25% -> 50% -> 100%) with automated rollback on SLO breach.

---

## 💻 3. Line-by-Line Commented Code Snippets (OpenTelemetry Context Propagation)

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class DistributedTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Line 7: Extract incoming Correlation ID or generate a new UUID
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())

        # Line 10: Inject correlation ID into request state for application logging
        request.state.correlation_id = correlation_id

        # Line 13: Execute downstream handler
        response = await call_next(request)

        # Line 16: Append correlation ID to response headers for client tracking
        response.headers["x-correlation-id"] = correlation_id
        return response
```
""",

    os.path.join(BASE_DIR, "13-system-design", "interview-questions", "top_system_design_interview_questions_catalog.md"): """# Top System Design High-Frequency Interview Problems Catalog

---

## 1. Design a Distributed Unique ID Generator (Twitter Snowflake)

### Requirements & Constraints:
- 64-bit numeric IDs.
- Globally unique, roughly time-sorted, capable of generating 10,000+ IDs per second per node.

### Snowflake 64-Bit Structure:
```
  [ 1 Bit: Sign (0) ] 
  [ 41 Bits: Timestamp in Milliseconds (Epoch offset provides ~69 years) ] 
  [ 10 Bits: Machine / Datacenter Node ID (Supports 1024 distinct nodes) ] 
  [ 12 Bits: Per-Node Sequence Counter (Supports 4096 IDs per ms per node) ]
```

### Python Implementation:
```python
import time

class SnowflakeIDGenerator:
    def __init__(self, node_id: int, epoch: int = 1704067200000):
        self.node_id = node_id # 0 - 1023
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1

    def generate_id(self) -> int:
        now = int(time.time() * 1000)
        if now < self.last_timestamp:
            raise Exception("Clock moved backwards! Refusing to generate ID.")

        if now == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF # 12 bits max (4095)
            if self.sequence == 0:
                # Sequence exhausted for this millisecond, wait for next ms
                while now <= self.last_timestamp:
                    now = int(time.time() * 1000)
        else:
            self.sequence = 0

        self.last_timestamp = now

        # Construct 64-bit ID using bit-shifting
        snowflake_id = (
            ((now - self.epoch) << 22) |
            (self.node_id << 12) |
            self.sequence
        )
        return snowflake_id

generator = SnowflakeIDGenerator(node_id=7)
print("Generated Snowflake ID:", generator.generate_id())
```

---

## 2. Design a Distributed Key-Value Store (Dynamo Style)
- **Data Partitioning**: Consistent Hashing with virtual nodes.
- **Replication**: Sloppy Quorum and Hinted Handoff ($N=3, R=2, W=2$).
- **Conflict Resolution**: Vector Clocks and Read Repair.
- **Node Failure Detection**: Gossip Protocol.

---

## 3. Design a Scalable Notification System
- **Scale**: 100 Million notifications per day.
- **Components**:
  - API Gateway -> Rate Limiter -> Notification Ingestion Service -> Kafka Message Topic (Priority: Critical vs Bulk) -> Notification Worker Pool -> Third-Party Providers (APNs for iOS, FCM for Android, Twilio for SMS, SendGrid for Email).
  - User Preference Cache in Redis (DND hours, opted-out categories).

---

## 4. Design a Distributed Web Crawler
- **Scale**: 1 Billion web pages per month.
- **Components**:
  - URL Frontier (Priority Queue + Politeness Queue with Hostname hashing).
  - DNS Cache (Pre-resolved hostnames).
  - HTML Fetcher & Parser.
  - Content Seen Detector (Fingerprinting via SimHash to eliminate duplicate pages).
  - URL Filter (`robots.txt` compliance).
"""
}

def main():
    print(f"Generating {len(FILES)} 50 System Design Concepts & Advanced Suites...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("50 System Design Concepts generation complete!")

if __name__ == "__main__":
    main()
