# PostgreSQL Declarative Table Partitioning and Streaming Replication

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

Table Partitioning ek **Mega Office File Cabinet** ki tarah hai:
Agar saare 10 saal ke bill ek hi vishal bori mein fek doge, toh 2026 ka bill dhoondne mein ghanton lag jayenge. Partitioning mein aap har saal ka alag drawer bana dete ho: `orders_2024`, `orders_2025`, `orders_2026`. Jab query aati hai `WHERE year = 2026`, toh Postgres baki 9 drawers ko chhoota bhi nahi hai (**Partition Pruning**)!
Streaming Replication **Photocopy Machine Sync** jaisa hai: Main office (Primary) par jo bhi entry hoti hai, photocopy telegraph se branch office (Replica) par turant chhap jati hai (**WAL Streaming**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Partitioning Methods**:
   - **Range**: By dates or numeric IDs (`PARTITION BY RANGE (created_at)`).
   - **List**: By explicit categorical keys (`PARTITION BY LIST (country_code)`).
   - **Hash**: Distributes rows uniformly across partitions (`PARTITION BY HASH (user_id)`).
2. **Partition Pruning**: The query planner excludes irrelevant partition tables from the query plan during planning or execution (`enable_partition_pruning = on`).
3. **Physical Streaming Replication**:
   - Uses Write-Ahead Logging (WAL).
   - Primary streams WAL records to Standby over TCP.
   - Standby continuously applies WAL changes to maintain an exact byte-for-byte read replica.
4. **Synchronous vs Asynchronous Replication**:
   - Asynchronous: Primary commits locally immediately; near-zero latency, but small risk of replication lag data loss during primary crash.
   - Synchronous: Primary waits for at least one replica to write WAL before acknowledging client. Zero data loss (RPO = 0), but higher commit latency.

---

## 💻 3. Line-by-Line Commented Code Snippets

```sql
-- Line 1: Create partitioned parent table
CREATE TABLE audit_logs (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at) -- Partition key MUST be included in Primary Key!
) PARTITION BY RANGE (created_at);

-- Line 10: Create individual partition for January 2026
CREATE TABLE audit_logs_2026_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2026-02-01 00:00:00+00');

-- Line 15: Create partition for February 2026
CREATE TABLE audit_logs_2026_02 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-02-01 00:00:00+00') TO ('2026-03-01 00:00:00+00');

-- Line 20: Partition Pruning verification
-- Query planner scans ONLY audit_logs_2026_01, skipping all other partitions!
EXPLAIN SELECT * FROM audit_logs 
WHERE created_at >= '2026-01-15' AND created_at <= '2026-01-20';
```
