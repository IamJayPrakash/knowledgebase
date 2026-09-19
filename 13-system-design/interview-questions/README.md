# 🏗️ System Design Senior & Staff Master Interview Question Bank (100 Questions)

> Comprehensive, production-grade 100-question interview bank covering all 50 foundational distributed system concepts, consensus protocols, streaming pipelines, resilience patterns, and top 20 real-world HLD system design case studies.

---

## 📑 Curriculum & Question Bank Structure

```
13-system-design/interview-questions/
├── 01_system_design_fundamentals_scale_and_storage_qna.md ──► Questions 1 to 20
├── 02_distributed_systems_consensus_and_consistency_qna.md ──► Questions 21 to 40
├── 03_event_driven_streaming_and_messaging_qna.md         ──► Questions 41 to 60
├── 04_protocols_resilience_and_sre_patterns_qna.md         ──► Questions 61 to 80
├── 05_classic_hld_architectures_and_case_studies_qna.md    ──► Questions 81 to 100
├── system_design_interview_framework.md                   ──► 45-Minute Playbook & Heuristics
├── top_system_design_interview_questions_catalog.md        ──► Quick Catalog & Cheat Sheet
└── [System_Design_Interview_Questions (1).pdf](../System_Design_Interview_Questions%20%281%29.pdf) ──► 📕 Printable Master 50-Concept PDF Guide
```

> 📕 **Offline / PDF Version Available**: You can also read, view, or download the companion document: [**`System_Design_Interview_Questions (1).pdf`**](../System_Design_Interview_Questions%20%281%29.pdf).

---

## 🎯 Master Question Index (1 - 100)

### Part 1: Scale, Latency, Storage, Databases & Caching (Q1 - Q20)

* [`01_system_design_fundamentals_scale_and_storage_qna.md`](./01_system_design_fundamentals_scale_and_storage_qna.md)
  1. Scalability vs Availability vs Reliability differences and formulas.
  2. Latency vs Throughput trade-offs and Little's Law.
  3. SQL (Relational) vs NoSQL decision tree.
  4. ACID properties in relational databases and Write-Ahead Logging (WAL).
  5. B-Tree vs B+Tree indexes and leaf node linked list range queries.
  6. Clustered Index vs Non-Clustered (Secondary) Index and bookmark lookups.
  7. Covering Index and eliminating random disk I/O.
  8. Horizontal Partitioning (Sharding) and shard key selection criteria.
  9. Range-Based vs Hash-Based vs Directory-Based Sharding comparison.
  10. Consistent Hashing with Virtual Nodes and the $N$-node rehashing solution.
  11. Caching strategies: Cache-Aside vs Write-Through vs Write-Back vs Refresh-Ahead.
  12. Cache Stampede (Thundering Herd) and XFetch early invalidation algorithm.
  13. Cache eviction policies: LRU vs LFU vs FIFO mechanics.
  14. Database connection pooling and socket connection overhead.
  15. Database Denormalization trade-offs for read-heavy systems.
  16. The N+1 Query problem detection and eager loading fix.
  17. Read Replicas, asynchronous WAL replication, and replication lag.
  18. Layer 4 (Transport TCP/UDP) vs Layer 7 (Application HTTP/gRPC) Load Balancing.
  19. Load balancing algorithms (Round Robin, Least Connections, IP Hash).
  20. Index cardinality, selectivity, and partial indexes.

### Part 2: Distributed Systems, Consensus, CAP Theorem & Consistency (Q21 - Q40)

* [`02_distributed_systems_consensus_and_consistency_qna.md`](./02_distributed_systems_consensus_and_consistency_qna.md)
  21. CAP Theorem trade-offs with CP and AP real-world systems.
  22. PACELC Theorem extending CAP under normal non-partitioned operation.
  23. Quorum Consensus formula ($R + W > N$) and strict consistency.
  24. Split-Brain scenarios in partitioned clusters and majority quorums ($\lfloor N/2 \rfloor + 1$).
  25. Raft Consensus algorithm: Leader Election, Log Replication, and Safety.
  26. Spectrum of Consistency Models: Linearizable down to Eventual Consistency.
  27. Linearizability (single-operation real-time) vs Serializability (ACID isolation).
  28. Vector Clocks and conflict detection in distributed writes.
  29. Conflict-free Replicated Data Types (CRDTs) and mathematical commutativity.
  30. Erasure Coding (Reed-Solomon $k+m$) vs $3\times$ Replication in object storage.
  31. Client-Side vs Server-Side Service Discovery architecture.
  32. Distributed Correlation IDs and W3C TraceContext header propagation.
  33. Two-Phase Commit (2PC) protocol and coordinator blocking failure modes.
  34. The Saga Pattern: Choreography vs Orchestration for distributed transactions.
  35. Synchronous (REST/gRPC) vs Asynchronous (Kafka/Queues) communication.
  36. Distributed Leader Election using etcd / ZooKeeper ephemeral leases.
  37. Monotonic Read Consistency guarantee.
  38. Gossip Protocol peer-to-peer decentralized convergence.
  39. Lamport Timestamps and logical partial ordering.
  40. Read-Repair in leaderless distributed databases.

### Part 3: Event-Driven Architecture, Streaming, LSM Trees & Batch Processing (Q41 - Q60)

* [`03_event_driven_streaming_and_messaging_qna.md`](./03_event_driven_streaming_and_messaging_qna.md)
  41. Message Queue (RabbitMQ) vs Distributed Commit Log (Kafka) comparison.
  42. Message delivery semantics: At-Most-Once, At-Least-Once, and Exactly-Once.
  43. Designing an Idempotent Consumer using unique idempotency keys.
  44. Transactional Outbox Pattern and Change Data Capture (CDC).
  45. How Kafka achieves extreme throughput: Sequential I/O, Page Cache, and Zero-Copy `sendfile`.
  46. Kafka Consumer Groups and partition rebalancing.
  47. Dead Letter Queues (DLQ) and handling Poison Pill messages.
  48. Log-Structured Merge (LSM) Trees architecture (MemTable, SSTables, WAL).
  49. Why LSM Trees outperform B+Trees for write-heavy workloads.
  50. Bloom Filters in LSM Trees and eliminating redundant disk reads.
  51. Size-Tiered vs Leveled Compaction in LSM stores.
  52. Event Sourcing architecture and snapshotting.
  53. Command Query Responsibility Segregation (CQRS) read/write separation.
  54. Batch Processing (Spark/Hadoop) vs Stream Processing (Flink) matrix.
  55. MapReduce model: Map, Shuffle/Sort, and Reduce phases.
  56. Lambda Architecture vs Kappa Architecture.
  57. Stream Windowing: Tumbling, Hopping, Sliding, and Session windows.
  58. Watermarks and handling late-arriving out-of-order streaming data.
  59. Handling Backpressure via reactive pull-based flow control.
  60. Change Data Capture (CDC) via Debezium and WAL log streaming.

### Part 4: Protocols, Resilience, Security & SRE Patterns (Q61 - Q80)

* [`04_protocols_resilience_and_sre_patterns_qna.md`](./04_protocols_resilience_and_sre_patterns_qna.md)
  61. REST vs GraphQL vs gRPC vs WebSockets vs WebRTC protocol decision matrix.
  62. HTTP/2 binary framing and stream multiplexing vs HTTP/1.1 HoL blocking.
  63. Circuit Breaker Pattern state transitions (Closed, Open, Half-Open).
  64. The Bulkhead Pattern for resource pool isolation.
  65. Exponential Backoff with Full Jitter retry formula (AWS best practice).
  66. Connection Timeout vs Read/Socket Timeout configurations.
  67. Rate Limiting algorithms: Token Bucket vs Leaky Bucket vs Sliding Window.
  68. Implementing an atomic Distributed Rate Limiter with Redis Lua scripts.
  69. Envelope Encryption in Secrets Management (DEK + KEK / KMS).
  70. Backend-For-Frontend (BFF) architectural pattern.
  71. The Strangler Fig Pattern for legacy monolith migration.
  72. Blue-Green vs Canary vs Rolling deployment strategies.
  73. Feature Flags (Toggles) and Trunk-Based Development.
  74. SRE Metrics: Service Level Indicators (SLI), Objectives (SLO), and Agreements (SLA).
  75. Error Budgets and balancing feature velocity with system reliability.
  76. Mutual TLS (mTLS) in Service Meshes for zero-trust network encryption.
  77. Insecure Deserialization attacks and secure schema-validated formats.
  78. BGP Anycast routing vs GeoDNS for global traffic distribution.
  79. CDN edge cache invalidation and cryptographic asset fingerprinting.
  80. Distributed Leaky Bucket rate limiting implementation in Redis.

### Part 5: Top 20 Real-World High-Level System Design Architectures (Q81 - Q100)

* [`05_classic_hld_architectures_and_case_studies_qna.md`](./05_classic_hld_architectures_and_case_studies_qna.md)
  81. Design a Scalable URL Shortener (TinyURL / Bitly).
  82. Design a Social Media News Feed with Celebrity Hybrid Fanout (Twitter / Instagram).
  83. Design a Real-Time Chat & Messaging Platform (WhatsApp / Discord).
  84. Design an E-Commerce Flash Sale & Inventory System with Atomic Redis Lua (Black Friday).
  85. Design a Proximity Service / Location-Based Search with Geohash / Google S2 (Uber / Yelp).
  86. Design a Video Streaming Service with Adaptive Bitrate Streaming (YouTube / Netflix).
  87. Design a Distributed Web Crawler with URL Frontier & Bloom Filters (Google Search).
  88. Design a Collaborative Real-Time Editor with Operational Transformation / CRDT (Google Docs / Figma).
  89. Design a Distributed Unique ID Generator with 64-bit Snowflake allocation (Twitter).
  90. Design a Real-Time Ride-Sharing Matching Engine with Hexagonal H3 spatial grids (Uber / Grab).
  91. Design a Distributed Metrics Monitoring & Alerting System with Gorilla TSDB (Datadog / Prometheus).
  92. Design a Search Autocomplete / Typeahead System with Trie & Min-Heap (Google Search).
  93. Design a Cloud File Storage & Synchronization Service with Chunking & Deduplication (Dropbox).
  94. Design a Webhook Delivery Engine with HMAC Signatures & Exponential Retries (Stripe).
  95. Design a High-Volume Ad Click Event Aggregator with Fraud Detection (Google Ads).
  96. Design a Distributed Lock Manager with Fencing Tokens (Redlock vs ZooKeeper).
  97. Design an Online Payment Gateway & Double-Entry Financial Ledger (Stripe / PayPal).
  98. Design a Live Video Streaming Chat with Room Sharding & Message Throttling (Twitch).
  99. Design a Distributed Web Gateway API Rate Limiter with Local Token Caching (Cloudflare).
  100. Design a Global Notification Service with Multi-Channel Failover (Twilio / Firebase).

---

## 📐 Playbooks & Frameworks

* [`system_design_interview_framework.md`](./system_design_interview_framework.md) — 45-Minute Senior/Staff Interview Playbook and Back-of-the-Envelope formulas.
* [`top_system_design_interview_questions_catalog.md`](./top_system_design_interview_questions_catalog.md) — Quick Recall Catalog & Architecture Cheat Sheet.
