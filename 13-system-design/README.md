# 🏗️ 13 - System Design (High-Level & Low-Level Architecture)

> Comprehensive architectural reference from **The 50 Essential System Design Concepts** to Real-World High-Level Design (HLD), Low-Level Design (LLD), and System Design Interview Problem Catalogs.

---

## 🗺️ Master Curriculum & Module Contents

### 1. 🌟 The 50 System Design Concepts Playbook
* [**`00_master_50_system_design_concepts.md`**](./00_master_50_system_design_concepts.md)
  - Comprehensive guide covering all 50 fundamental concepts itemized: Database, SQL vs NoSQL, Availability, Reliability, Latency, API Design, REST, Scalability, Load Balancing, Caching, Fault Tolerance, High Availability, CAP Theorem, GraphQL, gRPC, Sharding, Indexing, Leader Election, Consensus, Consistency Models, Event-Driven, Message Queue, Pub/Sub, Denormalization, Secrets Management, Bulkhead, Retry Logic, Timeout, Feature Flags, ACID, Blue-Green Deployment, Canary Release, Erasure Coding, Service Discovery, Sync vs Async, Correlation ID, BFF, Connection Pooling, Monitoring, Alerting, Query Optimization, WebSockets, Cache Stampede, MapReduce, WebRTC, Deserialization, Strangler Pattern, LSM Trees, Batch Processing, and Stream Processing.

### 2. Distributed Systems Foundations
* [**`07_distributed_systems_primitives_consensus_cap_sharding.md`**](./07_distributed_systems_primitives_consensus_cap_sharding.md)
  - CAP Theorem, PACELC Theorem, Raft Consensus, Quorum, and Consistent Hashing with Virtual Nodes (Python implementation).
* [**`08_resilience_and_stability_patterns.md`**](./08_resilience_and_stability_patterns.md)
  - Bulkhead Pattern, Timeouts, Exponential Backoff with Full Jitter, and Cache Stampede mitigation (XFetch algorithm).
* [**`09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md`**](./09_communication_protocols_rest_graphql_grpc_webrtc_websockets.md)
  - Detailed comparison of REST, GraphQL, gRPC, WebSockets, and WebRTC protocols with serialization trade-offs.
* [**`10_event_driven_streaming_batch_mapreduce.md`**](./10_event_driven_streaming_batch_mapreduce.md)
  - Message Queues vs Event Streams (Kafka vs RabbitMQ), Delivery Semantics, Lambda vs Kappa, and Idempotent Consumers.
* [**`11_observability_deployments_bluegreen_canary.md`**](./11_observability_deployments_bluegreen_canary.md)
  - Correlation IDs, Distributed Tracing, Metrics, Alerts, Blue-Green Deployments, and Canary Releases.

### 3. High-Level Design (HLD) Case Studies
* [**`01_hld_url_shortener_tinyurl.md`**](./01_hld_url_shortener_tinyurl.md) — TinyURL / Bitly scalable URL shortening with Base62 encoding and Key Generation Service.
* [**`02_hld_whatsapp_realtime_chat.md`**](./02_hld_whatsapp_realtime_chat.md) — WhatsApp real-time messaging, WebSockets, Presence servers, and Cassandra message store.
* [**`03_hld_netflix_video_streaming.md`**](./03_hld_netflix_video_streaming.md) — Netflix global video streaming, Transcoding pipelines, HLS/DASH chunking, and Open Connect CDN.
* [**`04_hld_uber_ride_matching_spatial_indexing.md`**](./04_hld_uber_ride_matching_spatial_indexing.md) — Uber real-time ride matching with Uber H3 hexagonal spatial indexing.

### 4. Low-Level Design (LLD) & Object-Oriented Patterns
* [**`05_lld_parking_lot_system.md`**](./05_lld_parking_lot_system.md) — Scalable multi-floor parking lot system with Factory and Strategy design patterns in Python.
* [**`06_lld_distributed_rate_limiter.md`**](./06_lld_distributed_rate_limiter.md) — Token Bucket and Sliding Window rate limiting algorithms implemented in Python.

### 5. Interview Preparation & Question Catalogs
* [**`interview-questions/system_design_interview_framework.md`**](./interview-questions/system_design_interview_framework.md) — The master 4-step structural interview playbook.
* [**`interview-questions/top_system_design_interview_questions_catalog.md`**](./interview-questions/top_system_design_interview_questions_catalog.md) — Canonical system design interview problems: Distributed Snowflake ID Generator, Distributed Key-Value Store (Dynamo-style), Scalable Notification System, and Distributed Web Crawler.
