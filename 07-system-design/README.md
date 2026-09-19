# 🏗️ System Design Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **HLD Distributed Systems to LLD Object-Oriented Patterns & LLM System Architectures** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for System Design.
- Create single concept files inside `07-system-design/` (e.g., `01_hld_caching_strategies.md`) as you learn and add your notes, architecture diagrams, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. High-Level Design (HLD) Fundamentals
- [ ] `01_scalability_load_balancing.md` — Vertical vs Horizontal Scaling, Load Balancer Layer 4 (TCP/UDP) vs Layer 7 (HTTP), Round Robin, Weighted Round Robin, Least Connections, IP Hash.
- [ ] `02_api_gateway_and_rate_limiting.md` — API Gateway responsibility (Auth, SSL Termination, Reverse Proxy), Rate Limiting Algorithms (Token Bucket, Leaky Bucket, Fixed Window Counter, Sliding Window Log, Sliding Window Counter).
- [ ] `03_caching_patterns_and_redis.md` — Caching Strategies (Cache-Aside, Write-Through, Write-Back, Read-Through), Eviction Policies (LRU, LFU, TTL), Redis Cluster & Sentinel setup, Cache stampede (Thundering herd) mitigation.
- [ ] `04_message_queues_kafka_vs_rabbitmq.md` — Asynchronous Messaging, Apache Kafka architecture (Topics, Partitions, Consumer Groups, Commit Log) vs RabbitMQ (Exchanges, Queues, Routing Keys), At-least-once vs Exactly-once delivery.

### 2. Database Design & Distributed Data
- [ ] `05_cap_and_pacelc_theorems.md` — CAP Theorem (Consistency, Availability, Partition Tolerance), PACELC Theorem (Latency vs Consistency tradeoff during normal operation), Eventual Consistency.
- [ ] `06_database_sharding_and_consistent_hashing.md` — Horizontal Sharding strategies (Range-based, Hash-based), Consistent Hashing algorithm with Virtual Nodes, Database Replication (Active-Passive vs Active-Active).

### 3. Low-Level Design (LLD) & Object-Oriented Design
- [ ] `07_solid_principles_with_examples.md` — Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion with real-world TypeScript/Python implementations.
- [ ] `08_gang_of_four_design_patterns.md` — Creational (Factory, Singleton, Builder), Structural (Adapter, Decorator, Proxy), Behavioral (Strategy, Observer, Command, Chain of Responsibility).
- [ ] `09_lld_case_studies.md` — LLD Parking Lot, LLD Rate Limiter, LLD Snake & Ladders, LLD Notification System.

### 4. LLM & GenAI System Design
- [ ] `10_scalable_rag_system_architecture.md` — Designing enterprise multi-tenant RAG (Document Ingestion pipeline, Vector Indexing, Hybrid Search, Real-Time SSE Streaming, Auth isolation).
- [ ] `11_llm_api_rate_limiter_and_gateway.md` — Designing a Proxy Gateway for LLM API providers with Token-Bucket rate limiting, fallback provider routing, and cost tracking.

---

## 💡 High-Yield Senior Interview Questions Pointers

1. **How does Consistent Hashing minimize data movement during database node scaling?**
   * *Answer Pointer:* Traditional hash `hash(key) % N` remaps almost 100% of keys when $N$ changes. Consistent Hashing maps keys and nodes onto a circular ring ($0$ to $2^{32}-1$). Adding or removing a node only reassigns keys in the immediate hash neighbor range ($k/N$ keys), leaving all other node assignments intact.
2. **What is the difference between Cache-Aside and Write-Through caching?**
   * *Answer Pointer:* In Cache-Aside, the application handles DB reads/writes directly, updating the cache on misses. In Write-Through, the application writes directly to the cache, and the cache synchronously writes to the underlying DB before confirming success.
3. **How do you design a real-time streaming response system for an LLM chat application?**
   * *Answer Pointer:* Use Server-Sent Events (SSE) or WebSockets over HTTP/2. The backend receives tokens incrementally from the LLM provider stream (vLLM / OpenAI API) and pushes chunked payloads to the frontend over a persistent HTTP connection.
