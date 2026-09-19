# 🏗️ System Design Interview Questions & Case Studies Index

> A categorized index of **HLD System Design Case Studies, LLD Object-Oriented Problems, and Real-Time Architectures** for Senior Tech Lead & SDE-2/3 Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific system design interview questions in this folder (e.g., `01_hld_chat_application.md`, `02_lld_parking_lot.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. High-Level Design (HLD) Real-World Case Studies
- [ ] `hld_url_shortener_tinyurl.md` — Design TinyURL (100M URLs, 1B reads/day, Base62 encoding, KGS, Caching).
- [ ] `hld_realtime_chat_app_whatsapp.md` — Design WhatsApp / Slack (WebSockets, Message Storage, Read Receipts, Presence).
- [ ] `hld_distributed_rate_limiter.md` — Design a distributed Rate Limiter (Token Bucket, Redis Sliding Window, Multi-region API Gateway).
- [ ] `hld_distributed_notification_system.md` — Design a Notification System sending Emails, SMS, and Push notifications at scale (Kafka, Rate Limiters, Provider fallbacks).
- [ ] `hld_llm_streaming_rag_system.md` — Design an Enterprise Streaming RAG Platform (Document Ingestion, Hybrid Search, Vector DB Sharding, SSE).

### 2. Low-Level Design (LLD) Machine Coding Problems
- [ ] `lld_parking_lot_system.md` — Design a Multi-Level Parking Lot system applying SOLID principles and Strategy pattern.
- [ ] `lld_rate_limiter.md` — Design a Rate Limiter class with extensible strategies (Token Bucket vs Leaky Bucket).
- [ ] `lld_pub_sub_system.md` — Design an in-memory Publisher-Subscriber messaging library with concurrency locks.

### 3. Deep-Dive Trade-off & Failure Scenario Questions
- [ ] `scenario_db_sharding_hotspot.md` — Resolving a database shard hotspot caused by non-uniform hash keys.
- [ ] `scenario_cache_stampede_thundering_herd.md` — How to protect downstream DBs from cache stampede during high-traffic cache invalidations.
