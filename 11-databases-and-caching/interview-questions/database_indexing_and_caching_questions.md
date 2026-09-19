# Top Database & Caching Senior Interview Questions

---

## 1. What is the difference between Clustered and Non-Clustered Indexes?
- **Clustered Index**: Determines the physical order of data rows stored on disk. A table can have **only one** clustered index (e.g. Primary Key in MySQL InnoDB).
- **Non-Clustered Index**: A separate data structure (B-Tree) containing sorted index columns and a pointer (RowID or Primary Key value) back to the actual data row in the clustered table.

---

## 2. Explain the Cache Penetration, Cache Breakdown, and Cache Avalanche problems.
- **Cache Penetration**: Queries request keys that do **not exist in either cache or database**. Every request hits the DB.
  - *Fix*: Cache null values with short TTL, or deploy a Bloom Filter at the gateway.
- **Cache Breakdown**: A single super-hot key expires, and thousands of concurrent requests hit the database simultaneously.
  - *Fix*: Distributed mutex locking (Redlock) or background asynchronous pre-fetching before expiry.
- **Cache Avalanche**: A massive number of cached keys expire at the exact same second, causing the database to crash under sudden load.
  - *Fix*: Add random jitter (e.g. TTL + random(1, 300) seconds) to expiry times.

---

## 3. What is Database Connection Pooling and why is it required?
- Opening a TCP connection to PostgreSQL or MySQL requires a 3-way TCP handshake, TLS negotiation, process/thread allocation, authentication verification, and memory structure initialization (taking 20-100ms per connection).
- Connection pooling maintains a pool of pre-authenticated active connections (e.g. HikariCP in Spring Boot, PgBouncer in Postgres). Applications borrow connections in under 1ms and return them upon query completion.
