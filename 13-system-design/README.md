# 🏗️ 13 - System Design (High-Level & Low-Level Architecture)

> Comprehensive architectural reference from **The 50 Essential System Design Concepts** to Real-World High-Level Design (HLD), Low-Level Design (LLD), and System Design Interview Problem Catalogs.

---

## 🗺️ Master Curriculum & Module Contents

### 1. 🌟 The 50 System Design Concepts Playbook & PDF Reference
* [**`00_master_50_system_design_concepts.md`**](./00_master_50_system_design_concepts.md)
  - Comprehensive guide covering all 50 fundamental concepts itemized: Database, SQL vs NoSQL, Availability, Reliability, Latency, API Design, REST, Scalability, Load Balancing, Caching, Fault Tolerance, High Availability, CAP Theorem, GraphQL, gRPC, Sharding, Indexing, Leader Election, Consensus, Consistency Models, Event-Driven, Message Queue, Pub/Sub, Denormalization, Secrets Management, Bulkhead, Retry Logic, Timeout, Feature Flags, ACID, Blue-Green Deployment, Canary Release, Erasure Coding, Service Discovery, Sync vs Async, Correlation ID, BFF, Connection Pooling, Monitoring, Alerting, Query Optimization, WebSockets, Cache Stampede, MapReduce, WebRTC, Deserialization, Strangler Pattern, LSM Trees, Batch Processing, and Stream Processing.
* [**`System_Design_Interview_Questions (1).pdf`**](./System_Design_Interview_Questions%20%281%29.pdf)
  - 📕 **Printable & Offline PDF Reference**: Complete 50 System Design Concepts & Interview Questions document. Viewable directly in the web portal or downloadable offline.

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

### 5. Master 100 Interview Question Bank & Frameworks
* [**`interview-questions/README.md`**](./interview-questions/README.md) — 🏗️ **Complete 100-Question Master Curriculum Index & Topic Guide**.
* [**`interview-questions/01_system_design_fundamentals_scale_and_storage_qna.md`**](./interview-questions/01_system_design_fundamentals_scale_and_storage_qna.md) — Questions 1 to 20: Scale, Latency, Storage, Databases, and Caching.
* [**`interview-questions/02_distributed_systems_consensus_and_consistency_qna.md`**](./interview-questions/02_distributed_systems_consensus_and_consistency_qna.md) — Questions 21 to 40: Distributed Systems, Consensus, CAP Theorem, and Consistency.
* [**`interview-questions/03_event_driven_streaming_and_messaging_qna.md`**](./interview-questions/03_event_driven_streaming_and_messaging_qna.md) — Questions 41 to 60: Event-Driven Architecture, Streaming, LSM Trees, and Batch Processing.
* [**`interview-questions/04_protocols_resilience_and_sre_patterns_qna.md`**](./interview-questions/04_protocols_resilience_and_sre_patterns_qna.md) — Questions 61 to 80: Protocols, Resilience, Security, and SRE Patterns.
* [**`interview-questions/05_classic_hld_architectures_and_case_studies_qna.md`**](./interview-questions/05_classic_hld_architectures_and_case_studies_qna.md) — Questions 81 to 100: Top 20 Real-World High-Level System Design Architectures.
* [**`interview-questions/system_design_interview_framework.md`**](./interview-questions/system_design_interview_framework.md) — The 45-Minute Senior/Staff System Design Interview Playbook.
* [**`interview-questions/top_system_design_interview_questions_catalog.md`**](./interview-questions/top_system_design_interview_questions_catalog.md) — Canonical system design interview problem catalog & cheat sheet.
