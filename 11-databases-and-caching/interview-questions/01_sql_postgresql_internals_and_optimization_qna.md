# Databases & Caching Master Interview Bank: Part 1 (Q1 - Q20)
## PostgreSQL Internals, MVCC, Indexing & Query Tuning

---

### Q1: How does Multi-Version Concurrency Control (MVCC) work in PostgreSQL?
**Answer:**
- **The Core Principle:** *"Readers never block writers, and writers never block readers."*
- **Under the Hood (`xmin` and `xmax`):**
  Every table row (tuple) in PostgreSQL contains hidden system columns:
  - `xmin`: The transaction ID (`txid`) that **inserted** the row.
  - `xmax`: The transaction ID that **deleted or updated** the row (set to 0 for active live rows).
- **Updates in PostgreSQL:**
  PostgreSQL **NEVER modifies rows in place**!
  An `UPDATE` marks the old row's `xmax = current_txid` (deleting it logically) and inserts a brand-new row version with `xmin = current_txid`.
- **Visibility:** Each transaction sees a snapshot of rows where `xmin <= my_txid` and (`xmax == 0` or `xmax > my_txid`), preventing dirty reads without taking table locks.

---

### Q2: What are "Dead Tuples" in PostgreSQL and why is VACUUM mandatory?
**Answer:**
- Because updates and deletes do not overwrite disk blocks in place, old superseded row versions remain physically stored on disk as **Dead Tuples**.
- Over time, dead tuples cause **Table Bloat**, degrading sequential scan performance and wasting disk space.
- **`VACUUM` (Standard):**
  Traverses tables, marks space occupied by dead tuples as reusable for future `INSERT`s, and freezes old transaction IDs to prevent **Transaction ID Wraparound**. (Does NOT release space back to the OS).
- **`VACUUM FULL`:**
  Re-writes the entire table into a new disk file from scratch, releasing disk space back to the OS.
  - *Caution:* Takes an **Exclusive Table Lock (`ACCESS EXCLUSIVE`)**, blocking all reads and writes!

---

### Q3: How does Autovacuum work and how do you tune it for high-write tables?
**Answer:**
- **Autovacuum:** Background daemon that monitors dead tuple counts and automatically triggers vacuum and analyze operations:
  $$\text{Threshold} = \text{vacuum\_base\_threshold} + (\text{vacuum\_scale\_factor} \times \text{reltuples})$$
- Default `vacuum_scale_factor` is **0.2 (20%)**.
- **The Problem for Large Tables:** On a 100,000,000 row table, autovacuum won't run until **20,000,000 rows are dead**, causing catastrophic table bloat!
- **Tuning per Table:**
  ```sql
  ALTER TABLE orders SET (
      autovacuum_vacuum_scale_factor = 0.05, -- Trigger after 5% dead rows
      autovacuum_vacuum_cost_limit = 1000     -- Increase I/O budget for vacuum worker
  );
  ```

---

### Q4: Compare PostgreSQL Index Types: B-Tree vs Hash vs GIN vs GiST vs BRIN.
**Answer:**
| Index Type | Internal Algorithm | Best Used For | Supported Operators |
| :--- | :--- | :--- | :--- |
| **B-Tree** | Balanced multi-way tree | Primary keys, timestamps, numbers, strings | `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `ORDER BY` |
| **Hash** | Hash table | Direct equality checks on large text | `=` only |
| **GIN (Generalized Inverted Index)** | Inverted index (maps components to rows) | Full-text search, JSONB documents, Array columns | `@>`, `?`, `@@` |
| **GiST (Generalized Search Tree)** | Hierarchical spatial R-Tree | Geometric coordinates (PostGIS), IP ranges | `&&` (overlaps), `<@` (contained by) |
| **BRIN (Block Range Index)** | Stores min/max values per disk block range | Massive append-only time-series tables (e.g. 500GB logs) | Range queries on naturally physically sorted data |

---

### Q5: What is a BRIN Index and why is it 99% smaller than a B-Tree?
**Answer:**
- **BRIN (Block Range Index):** Instead of storing an entry for every single row, BRIN summarizes physical disk page ranges (e.g. 128 disk blocks / ~1MB of data), storing only the **minimum and maximum values** found in that range.
- **Size Comparison:**
  On a 100-million row timestamped table:
  - B-Tree Index: **~2.5 Gigabytes**.
  - BRIN Index: **~200 Kilobytes (99.9% smaller!)**.
- **Condition:** Data must be physically ordered on disk (e.g. auto-incrementing IDs or sequential created timestamps).

---

### Q6: How do you read and interpret an `EXPLAIN (ANALYZE, BUFFERS)` execution plan?
**Answer:**
- `EXPLAIN`: Shows the optimizer's estimated execution plan without running the query.
- `EXPLAIN (ANALYZE, BUFFERS)`: **Actually executes the query** and displays real execution statistics:
  1. **Node Type:** `Seq Scan` (Table scan), `Index Scan` (Index read + table lookup), `Index Only Scan` (Covering index - zero table reads), `Bitmap Heap Scan` (Index matches converted to bitmap before heap reads).
  2. **`actual time=0.042..1.210 rows=50`**: Time to first row (0.042ms) and time to finish (1.210ms).
  3. **`Buffers: shared hit=45 read=10`**:
     - `shared hit`: Disk pages read directly from RAM (PostgreSQL shared buffers).
     - `shared read`: Disk pages that had to be read from physical disk storage (expensive I/O!).

---

### Q7: What are Partial Indexes and Expression Indexes in PostgreSQL?
**Answer:**
- **Partial Index:** Indexes only a subset of table rows matching a `WHERE` clause:
  ```sql
  -- Only index pending orders (99% of orders are completed, 1% pending):
  CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'PENDING';
  ```
  - *Benefit:* 90% smaller index size, zero maintenance overhead when updating completed rows.
- **Expression Index:** Indexes the result of a function rather than column values directly:
  ```sql
  CREATE INDEX idx_users_lower_email ON users (LOWER(email));
  -- Speeds up: SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
  ```

---

### Q8: What is Table Partitioning in PostgreSQL (Declarative Partitioning)?
**Answer:**
Divides a single large logical table into smaller physical tables on disk:
1. **Range Partitioning:** Partition by date or numeric ranges (e.g. `orders_2024_q1`, `orders_2024_q2`).
2. **List Partitioning:** Partition by explicit status or country codes (e.g. `users_us`, `users_eu`).
3. **Hash Partitioning:** Partition by modulo hash of a key across $N$ partitions.
- **Partition Pruning:** The query planner inspects the query's `WHERE` clause and skips reading unrelated partition tables completely (`enable_partition_pruning = on`).

---

### Q9: What is Write-Ahead Logging (WAL) and how does WAL Archiving enable Point-In-Time Recovery (PITR)?
**Answer:**
- **WAL:** Every change (INSERT, UPDATE, DELETE) is written **sequentially to an append-only log on disk** before modifying actual table data pages in memory.
- If the server crashes or loses power, PostgreSQL replays the WAL on reboot to restore 100% data consistency without loss.
- **Point-In-Time Recovery (PITR):**
  By continuously archiving completed WAL segment files (16MB files) to cloud object storage (S3), you can restore a base backup taken 3 weeks ago and replay WAL files up to an exact second in time (e.g. 1 second before a rogue `DROP TABLE` occurred!).

---

### Q10: How does Streaming Replication work in PostgreSQL (Physical vs Logical)?
**Answer:**
- **Physical Streaming Replication:**
  The primary server streams raw binary WAL byte changes directly over TCP to standby replicas. Replicas are byte-for-byte exact copies (read-only).
- **Logical Streaming Replication (Publish/Subscribe):**
  Streams decoded relational row mutations (`INSERT`, `UPDATE`, `DELETE`).
  - Allows replicating across different PostgreSQL major versions (v14 to v16).
  - Allows selective replication of specific tables.
  - Powers Change Data Capture (CDC) with Debezium.

---

### Q11: What is Connection Pooling in PostgreSQL and why is PgBouncer essential?
**Answer:**
- In PostgreSQL, every client connection spawns a **dedicated OS backend process (`postgres`)** consuming **5MB to 10MB of private RAM**.
- At 1,000 concurrent direct connections, PostgreSQL crashes due to context-switching overhead and memory starvation.
- **PgBouncer:** A lightweight connection pooler that maintains a pool of 20-50 real backend connections to PostgreSQL, multiplexing thousands of client connections across them with microsecond latency.
- **Modes:** `Session` (connection held for entire client session), `Transaction` (recommended - connection borrowed only for the duration of a transaction).

---

### Q12: How do you handle JSONB indexing in PostgreSQL?
**Answer:**
PostgreSQL supports binary JSON (`JSONB`) with GIN indexes:
```sql
-- Index all keys and values in the JSON document:
CREATE INDEX idx_user_metadata ON users USING GIN (metadata);

-- Query using containment operator (@>):
SELECT * FROM users WHERE metadata @> '{"role": "admin", "verified": true}';
```
The GIN index creates an inverted index of every path and scalar value, allowing arbitrary nested JSON searches in $O(\log N)$ time.

---

### Q13: What is the difference between `SERIALIZABLE` and `REPEATABLE READ` isolation levels in PostgreSQL?
**Answer:**
- **`REPEATABLE READ`:** Uses snapshot isolation. Guarantees that queries within the transaction only see data committed before the transaction started. Eliminates Dirty Reads and Non-Repeatable Reads, but is vulnerable to **Write Skew**.
- **`SERIALIZABLE` (SSI - Serializable Snapshot Isolation):**
  Tracks read-write dependencies across transactions (siREAD locks in memory). If a dependency cycle is detected (risk of non-serializable outcome), PostgreSQL aborts one transaction with `ERROR: could not serialize access due to concurrent update`.

---

### Q14: What is the "Transaction ID Wraparound" crisis in PostgreSQL?
**Answer:**
- PostgreSQL transaction IDs (`txid`) are 32-bit unsigned integers, providing ~4.2 billion IDs.
- If a database executes $> 2 \text{ Billion}$ transactions without freezing old IDs, transaction IDs wrap around: past transactions suddenly appear to have occurred in the future, rendering **historical data invisible**!
- **Defense:** Autovacuum automatically performs **Aggressive Freezing** (marking old `xmin` as frozen). If autovacuum is disabled or blocked, PostgreSQL halts all write operations to protect data integrity.

---

### Q15: How does the `FILLFACTOR` setting optimize update-heavy tables (HOT Updates)?
**Answer:**
- By default, PostgreSQL packs table pages to 100% capacity (`FILLFACTOR = 100`).
- Updating a row forces PostgreSQL to write the new tuple to a different disk page, requiring updates to all secondary indexes.
- **Heap-Only Tuple (HOT) Optimization:**
  Setting `FILLFACTOR = 80` leaves 20% empty space on each disk page.
  When a row is updated, the new version fits on the **exact same disk page**, eliminating secondary index updates completely and cutting write I/O by 50%!

---

### Q16: What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?
**Answer:**
- **`DELETE FROM table WHERE ...`:** DML operation. Logs individual row deletions in WAL, triggers foreign key constraints and triggers, and generates dead tuples. Slow for large datasets.
- **`TRUNCATE table`:** DDL operation. De-allocates the underlying data file disk blocks immediately by creating an empty replacement file. Bypasses row-level WAL logging and triggers; instant execution ($O(1)$).
- **`DROP TABLE table`:** DDL operation. Completely removes the table definition, data files, indexes, and constraints from the database catalog.

---

### Q17: What are Advisory Locks in PostgreSQL?
**Answer:**
- Application-level locks managed by the database engine using arbitrary 64-bit integers:
  `SELECT pg_advisory_lock(12345);`
- **Advantage:** Unlike row locks (`SELECT FOR UPDATE`), Advisory Locks do not lock physical table rows and can be acquired even if no table exists.
- Ideal for distributed leader election, cross-node scheduling, and preventing duplicate batch cron jobs.

---

### Q18: What is the `shared_buffers` configuration parameter in PostgreSQL?
**Answer:**
- Dictates how much dedicated RAM memory PostgreSQL reserves for caching shared data pages.
- **Recommendation:** Typically set to **25% of total system RAM** (e.g. 16GB on a 64GB machine).
- Unlike other databases, PostgreSQL relies heavily on the **Linux OS Kernel Page Cache** for the remaining memory rather than allocating 80% to `shared_buffers`.

---

### Q19: What is `work_mem` and how does it prevent disk-based sorts?
**Answer:**
- Specifies the amount of RAM memory allocated for internal sorting operations (`ORDER BY`, `DISTINCT`) and hash tables (`Hash Join`) **per operation per query**.
- If a sort operation exceeds `work_mem`, PostgreSQL falls back to a **disk-based external merge sort**, which is orders of magnitude slower.
- *Caution:* `work_mem` is allocated per query node; if 100 concurrent queries each run 4 sorts, memory consumption can be $400 \times \text{work\_mem}$!

---

### Q20: How do you identify slow queries in PostgreSQL using `pg_stat_statements`?
**Answer:**
Enable `pg_stat_statements` extension in `postgresql.conf`:
```sql
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```
Instantly highlights the top queries consuming the most cumulative CPU and disk I/O across the entire database server.
