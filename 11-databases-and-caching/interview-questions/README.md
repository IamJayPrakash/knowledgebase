# 🗄️ Databases & Caching Senior & Staff Master Interview Question Bank (60 Questions)

> Comprehensive, production-grade 60-question interview bank covering PostgreSQL internals (MVCC, indexes, vacuum, replication), Redis in-memory architecture (data structures, Redlock, clustering), and MongoDB distributed storage (WiredTiger, ESR indexing, aggregation, sharding).

---

## 📑 Curriculum & Question Bank Structure

```
11-databases-and-caching/interview-questions/
├── 01_sql_postgresql_internals_and_optimization_qna.md ──► Questions 1 to 20
├── 02_redis_caching_and_distributed_systems_qna.md     ──► Questions 21 to 40
├── 03_nosql_mongodb_and_distributed_storage_qna.md    ──► Questions 41 to 60
└── database_indexing_and_caching_questions.md          ──► Quick Refresher
```

---

## 🎯 Master Question Index (1 - 60)

### Part 1: PostgreSQL Internals, MVCC, Indexing & Query Tuning (Q1 - Q20)
* [`01_sql_postgresql_internals_and_optimization_qna.md`](./01_sql_postgresql_internals_and_optimization_qna.md)
  1. Multi-Version Concurrency Control (MVCC) and `xmin` / `xmax` system columns.
  2. Dead tuples, Table Bloat, and standard `VACUUM` vs `VACUUM FULL`.
  3. Autovacuum threshold mathematical formula and per-table tuning.
  4. B-Tree vs Hash vs GIN vs GiST vs BRIN index types comparison.
  5. BRIN (Block Range Index) and 99% index size reduction for time-series.
  6. Reading and interpreting `EXPLAIN (ANALYZE, BUFFERS)` execution plans.
  7. Partial Indexes and Expression Indexes in query optimization.
  8. Table Partitioning (Range, List, Hash) and partition pruning.
  9. Write-Ahead Logging (WAL) and Point-In-Time Recovery (PITR).
  10. Physical vs Logical streaming replication mechanisms.
  11. PostgreSQL connection pooling and why PgBouncer is mandatory.
  12. JSONB indexing with GIN indexes and containment operators.
  13. `SERIALIZABLE` Snapshot Isolation (SSI) vs `REPEATABLE READ`.
  14. Transaction ID Wraparound crisis and aggressive freezing.
  15. `FILLFACTOR` setting and Heap-Only Tuple (HOT) update optimization.
  16. Differences between `DELETE`, `TRUNCATE`, and `DROP`.
  17. Application-level Advisory Locks in distributed coordination.
  18. `shared_buffers` memory configuration and OS kernel page cache.
  19. `work_mem` sizing and avoiding disk-based external merge sorts.
  20. Identifying slow queries using `pg_stat_statements`.

### Part 2: Redis Architecture, In-Memory Internals, Clustering & Redlock (Q21 - Q40)
* [`02_redis_caching_and_distributed_systems_qna.md`](./02_redis_caching_and_distributed_systems_qna.md)
  21. Why single-threaded Redis achieves 100,000+ QPS (I/O multiplexing, epoll).
  22. The 6 core Redis Data Structures and their underlying C implementations.
  23. SkipLists in Redis Sorted Sets (ZSet) and $O(\log N)$ range scans.
  24. The 8 Redis Cache Eviction Policies (`maxmemory-policy`).
  25. Approximated LRU algorithms avoiding linked list pointer overhead.
  26. Redis Persistence: RDB point-in-time snapshots vs AOF append-only log.
  27. Non-blocking AOF Rewrite (`BGREWRITEAOF`) via fork and rewrite buffer.
  28. Implementing Distributed Locks correctly with atomic `SET NX PX` and Lua script.
  29. The Redlock Algorithm across independent masters and Fencing Tokens.
  30. Redis Transactions (`MULTI`, `EXEC`, `WATCH`) vs SQL ACID.
  31. 16,384 Hash Slots in Redis Cluster and zero-downtime resharding.
  32. Hash Tags (`{...}`) enforcing multi-key operations on the same slot.
  33. Redis Sentinel: Monitoring, quorum election, and automatic master failover.
  34. Redis Pub/Sub (ephemeral) vs Redis Streams (durable consumer groups).
  35. Redis Pipelining reducing network RTTs by 98%.
  36. Cache Penetration problem and Bloom Filter mitigations.
  37. Cache Breakdown (hotspot expired) vs Cache Avalanche (jitter solution).
  38. Redis replication and partial resynchronization (PSYNC2).
  39. BigKey dangers and non-blocking asynchronous deletion (`UNLINK`).
  40. Bitmaps and Bitfields for low-memory DAU tracking.

### Part 3: MongoDB Internals, Aggregation, Sharding & Distributed NoSQL (Q41 - Q60)
* [`03_nosql_mongodb_and_distributed_storage_qna.md`](./03_nosql_mongodb_and_distributed_storage_qna.md)
  41. WiredTiger Storage Engine: B-Trees, Snappy compression, document-level locks.
  42. The ESR (Equality, Sort, Range) compound indexing rule.
  43. The 16MB document size limit and GridFS chunking for large files.
  44. Schema Design: Embedding vs Referencing (1-to-few vs 1-to-many vs 1-to-squillions).
  45. The Aggregation Pipeline: `$match`, `$unwind`, `$lookup`, `$group`.
  46. Replica Set high availability, heartbeats, and Raft-like elections.
  47. Write Concerns: `w: 1` vs `w: "majority"` vs `j: true`.
  48. Read Concerns: `"local"` vs `"majority"` vs `"linearizable"`.
  49. Sharding Architecture: `mongos` query router, Config Servers, Shard nodes.
  50. Chunk Splitting (64MB) and the background Balancer migration process.
  51. Monotonically increasing shard keys as an anti-pattern.
  52. MongoDB vs Apache Cassandra architectural comparison.
  53. Snapshot Isolation and multi-document ACID transactions.
  54. TTL (Time-To-Live) index for automatic document expiration.
  55. Covered Queries in MongoDB eliminating document fetches.
  56. `$set` field update vs full document replacement (`replaceOne`).
  57. Read Preferences: `primary`, `secondary`, `nearest`.
  58. Change Streams for real-time reactive event ingestion.
  59. MongoDB Atlas Search with embedded Apache Lucene.
  60. Database profiling and detecting unindexed collection scans (`COLLSCAN`).

---

## ⚡ Quick Refresher
* [`database_indexing_and_caching_questions.md`](./database_indexing_and_caching_questions.md) — Quick Indexing & Caching Refresher.
