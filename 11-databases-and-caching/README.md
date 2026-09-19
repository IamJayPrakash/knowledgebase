# 🗄️ 11 - Databases, Relational Storage & Caching

> Enterprise reference for PostgreSQL (MVCC, Partitioning), Redis (Data Structures, Distributed Locks), and MongoDB (Indexing, Aggregation).

---

## 🗂️ Module Contents & Learning Path

### 1. PostgreSQL Relational Database
* [**`sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md`**](./sql-postgresql/01_postgresql_mvcc_indexing_query_tuning.md)
  - Multi-Version Concurrency Control (`xmin`/`xmax`), Autovacuum, Partial Indexes, and `EXPLAIN (ANALYZE, BUFFERS)`.
* [**`sql-postgresql/02_postgresql_partitioning_and_replication.md`**](./sql-postgresql/02_postgresql_partitioning_and_replication.md)
  - Declarative table partitioning (Range, List, Hash), partition pruning, and WAL physical streaming replication.

### 2. Redis High-Performance Cache & Distributed Locks
* [**`redis-caching/01_redis_data_structures_and_eviction_policies.md`**](./redis-caching/01_redis_data_structures_and_eviction_policies.md)
  - Strings, Hashes, Sorted Sets, `maxmemory-policy` (LRU vs LFU), and sliding window rate limiting.
* [**`redis-caching/02_redis_distributed_locking_and_pubsub.md`**](./redis-caching/02_redis_distributed_locking_and_pubsub.md)
  - Atomic distributed locking (Redlock, `SET NX PX`), Lua script verification, and Pub/Sub.

### 3. MongoDB NoSQL Document Store
* [**`nosql-mongodb/01_mongodb_architecture_indexing_sharding.md`**](./nosql-mongodb/01_mongodb_architecture_indexing_sharding.md)
  - WiredTiger storage engine, ESR compound indexing rule, and sharded cluster architectures.
* [**`nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md`**](./nosql-mongodb/02_mongodb_aggregation_pipeline_mastery.md)
  - Multi-stage Aggregation pipelines (`$match`, `$unwind`, `$lookup`, `$group`).

### 4. Master 60 Interview Question Bank
* [**`interview-questions/README.md`**](./interview-questions/README.md) — 🗄️ **Complete 60-Question Master Curriculum Index & Topic Guide**.
* [**`interview-questions/01_sql_postgresql_internals_and_optimization_qna.md`**](./interview-questions/01_sql_postgresql_internals_and_optimization_qna.md) — Questions 1 to 20: PostgreSQL Internals, MVCC, Indexing, and Query Tuning.
* [**`interview-questions/02_redis_caching_and_distributed_systems_qna.md`**](./interview-questions/02_redis_caching_and_distributed_systems_qna.md) — Questions 21 to 40: Redis Architecture, In-Memory Internals, Clustering, and Redlock.
* [**`interview-questions/03_nosql_mongodb_and_distributed_storage_qna.md`**](./interview-questions/03_nosql_mongodb_and_distributed_storage_qna.md) — Questions 41 to 60: MongoDB Internals, Aggregation, Sharding, and Distributed NoSQL.
* [**`interview-questions/database_indexing_and_caching_questions.md`**](./interview-questions/database_indexing_and_caching_questions.md) — Quick Indexing & Caching Refresher.
