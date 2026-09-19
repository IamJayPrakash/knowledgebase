# Databases & Caching Master Interview Bank: Part 3 (Q41 - Q60)

## MongoDB Internals, Aggregation, Sharding & Distributed NoSQL

---

### Q41: How does MongoDB's WiredTiger Storage Engine work internally?

**Answer:**

- Since MongoDB 3.2, **WiredTiger** is the default storage engine.
- **Key Architecture Components:**
  1. **B-Tree Structure:** Uses standard B-Trees on disk for fast random reads and writes.
  2. **WiredTiger Internal Cache:** Allocates $\approx 50\%$ of (RAM - 1GB) for uncompressed in-memory document data.
  3. **Compression:** Compresses collections using **Snappy** (balanced speed/compression) or **zlib** on disk, saving up to 70% disk space compared to uncompressed BSON.
  4. **Checkpoints & Journaling:** Creates checkpoints every 60 seconds. A Write-Ahead Journal logs mutations in between checkpoints to guarantee crash durability.
  5. **Document-Level Concurrency:** Provides fine-grained **document-level locking** using optimistic concurrency control, allowing simultaneous writes to different documents in the same collection without lock contention.

---

### Q42: What is the ESR (Equality, Sort, Range) Indexing Rule in MongoDB?

**Answer:**
The gold standard rule for constructing compound indexes in MongoDB:
$$\text{Compound Index Order:} \quad \mathbf{E} \text{quality} \longrightarrow \mathbf{S} \text{ort} \longrightarrow \mathbf{R} \text{ange}$$

1. **Equality (E):** Columns tested for exact matches (`status: "ACTIVE"`) go **first**. They filter down the index scan space immediately.
2. **Sort (S):** Columns specified in `sort({ createdAt: -1 })` go **second**. If placed before Range, MongoDB can traverse the index in sorted order, **completely eliminating in-memory blocking sorts (`SORT` stage in explain)**.
3. **Range (R):** Columns with inequality filters (`age: { $gt: 21 }`, `$in`, `$gte`) go **last**. (Placing a range filter before a sort prevents the index from satisfying the sort order).

```javascript
// Query:
db.orders.find({ status: "PAID", total: { $gt: 100 } }).sort({ createdAt: -1 });

// Optimal Compound Index following ESR:
db.orders.createIndex({
  status: 1,     // [E]quality
  createdAt: -1, // [S]ort
  total: 1       // [R]ange
});
```

---

### Q43: What is the 16MB Document Size Limit in MongoDB and how do you design around it?

**Answer:**

- **The Limit:** A single BSON document cannot exceed **16 Megabytes**.
  - Enforced to prevent memory bloat, keep RAM cache efficient, and prevent network transmission stalls.
- **Design Workarounds:**
  1. **Subset Pattern:** Store only recent data (e.g. latest 10 reviews) inside the main product document; store full reviews in a separate collection.
  2. **GridFS:** For files $> 16\text{MB}$ (images, PDFs, videos), MongoDB provides **GridFS**, which automatically splits the file into small **255 KB chunks** stored in two collections: `fs.files` (metadata) and `fs.chunks` (binary data).

---

### Q44: When should you Embed vs Reference in MongoDB Document Schema Design?

**Answer:**

| Relationship | Recommended Design | Example |
| :--- | :--- | :--- |
| **One-to-Few** ($< 100$ items) | **Embed** directly inside the parent document. | User with multiple shipping addresses. |
| **One-to-Many** ($100 - 10,000$ items) | **Reference** via parent or child IDs. | E-commerce Order with line items. |
| **One-to-Squillions** ($> 10,000$ items) | **Reference with Parent-Pointer** in child documents. | IoT sensor logs pointing back to `device_id`. |

---

### Q45: Explain the MongoDB Aggregation Pipeline and its core stages

**Answer:**

- A framework for data processing modeled on data-processing pipelines (records pass through multi-stage transformations):
  - **`$match`**: Filters documents (always place first to utilize indexes and reduce dataset volume).
  - **`$project`**: Selects, renames, and computes new fields.
  - **`$unwind`**: Deconstructs an array field from the input document to output a document for each element.
  - **`$group`**: Groups documents by an `_id` key and applies accumulators (`$sum`, `$avg`, `$push`).
  - **`$lookup`**: Performs a left outer join to an unsharded collection in the same database.
  - **`$sort`**, **`$skip`**, **`$limit`**: Pagination and ordering.

```javascript
// Calculate total revenue per customer for completed orders:
db.orders.aggregate([
  { $match: { status: "COMPLETED" } },
  { $group: { _id: "$customerId", totalSpent: { $sum: "$total" }, orderCount: { $sum: 1 } } },
  { $sort: { totalSpent: -1 } },
  { $limit: 10 }
]);
```

---

### Q46: How does MongoDB Replica Set High Availability work?

**Answer:**

- A Replica Set is a group of `mongod` instances maintaining the same dataset (typically 3 nodes: 1 Primary + 2 Secondaries).
- **Primary:** Receives all write operations. Writes to internal **`oplog` (Operations Log)**.
- **Secondaries:** Continuously replicate the `oplog` and apply changes to their local data.
- **Automatic Failover:**
  If the Primary fails or loses contact for $> 10$ seconds, Secondaries conduct a **Raft-like election**. The secondary with the highest `priority` and most up-to-date `oplog` is elected as the new Primary.

---

### Q47: What are MongoDB Write Concerns (`w: 1` vs `w: "majority"`)?

**Answer:**
Controls the level of acknowledgment requested from MongoDB for a write operation:

- **`w: 1`:** Acknowledges write as soon as the **standalone Primary** has written the change to its memory.
  - *Risk:* If the Primary crashes before replicating to Secondaries, the write is **permanently rolled back and lost**!
- **`w: "majority"` (Production Standard):**
  Acknowledges write ONLY after a **strict majority of replica set members** have written the change. Guarantees that even if the primary crashes, the elected new primary will have the write.
- **`j: true` (Journaling):** Acknowledges write only after it has been flushed to the on-disk Write-Ahead Journal.

---

### Q48: What are MongoDB Read Concerns (`"local"`, `"majority"`, `"linearizable"`)?

**Answer:**
Controls the consistency and isolation of data read from replica sets:

- **`"local"` (Default):** Returns data from the queried node immediately. Does NOT verify if data has been committed to a majority (risk of reading dirty/rolled-back data).
- **`"majority"`:** Returns data committed to a majority of replica set nodes. Eliminates dirty reads; will never be rolled back.
- **`"linearizable"`:** Strictly prevents stale reads. The Primary verifies with a majority of members in real-time that it is still the legitimate leader before returning, guaranteeing real-time external consistency.

---

### Q49: Diagram and explain MongoDB Sharding Architecture

**Answer:**

```
           [ Client Application ]
                     │
                     ▼
          [ mongos Query Router ] ◄──── Pulls cluster routing metadata
           (Stateless load balancer)          │
                     │                        │
     ┌───────────────┼───────────────┐        ▼
     │               │               │   [ Config Server Replica Set ]
     ▼               ▼               ▼   (Stores shard key ranges & routing)
[ Shard 1 ]     [ Shard 2 ]     [ Shard 3 ]
(Replica Set)   (Replica Set)   (Replica Set)
```

1. **`mongos` Router:** Stateless proxy that routes queries directly to the appropriate shard.
2. **Config Servers:** A 3-node replica set storing cluster metadata, chunk distribution mappings, and shard key ranges.
3. **Shard Nodes:** Individual replica sets holding partitioned subsets of data.

---

### Q50: What is Chunk Splitting and Balancing in MongoDB Sharding?

**Answer:**

- Data in a sharded collection is organized into contiguous ranges called **Chunks** (default chunk size: 64MB).
- **Chunk Splitting:** When a chunk reaches 64MB, `mongos` automatically splits it into two smaller chunks. (Splitting is a purely metadata operation; no data moves).
- **Balancer:** A background process running on the Config Server Primary. If the difference in chunk counts between shards exceeds a migration threshold, the balancer migrates chunks from overloaded shards to underloaded shards across the network.

---

### Q51: What is a Monotonically Increasing Shard Key and why is it an Anti-Pattern?

**Answer:**

- **Example:** Sharding by `_id` (ObjectId containing timestamp) or `createdAt`.
- **The Hotspot Flaw:** Because every new document has a higher timestamp than previous documents:
  - **100% of all write operations are routed to the single shard** holding the max range chunk!
  - All other shards sit completely idle.
  - The balancer is forced into constant, expensive background chunk migrations.
- **Fix:** Use a **Hashed Shard Key** (`createIndex({ _id: "hashed" })`) or a compound shard key with high cardinality prefix.

---

### Q52: What is the difference between MongoDB and Apache Cassandra?

**Answer:**

| Dimension | MongoDB | Apache Cassandra |
| :--- | :--- | :--- |
| **Data Model** | JSON-like BSON Documents (Flexible schema). | Wide-Column Family (CQL with strict typed schema). |
| **Cluster Topology** | **Master-Slave / Primary-Secondary** (Single primary per shard accepts writes). | **Masterless / Peer-to-Peer** (Every node is identical; any node accepts writes). |
| **Consensus** | Raft-like election with strong consistency on Primary. | Tunable Quorum ($R + W > N$) over Eventual Consistency. |
| **Storage Engine** | WiredTiger B-Trees. | **LSM Trees** (Optimized for massive append-only write throughput). |
| **Query Flexibility** | Rich aggregation, nested arrays, secondary indexes. | Primary Key lookup & partition key equality only; no joins. |

---

### Q53: How does MongoDB prevent "Phantom Reads" in Multi-Document Transactions?

**Answer:**

- Since MongoDB 4.0, multi-document ACID transactions are supported across replica sets and sharded clusters.
- MongoDB uses **Snapshot Isolation**:
  When a transaction starts, it reads from a global WiredTiger snapshot.
  Concurrent writes are isolated until commit. If two concurrent transactions attempt to modify the same document, the second transaction fails with a **Write Conflict** and must be retried by the client.

---

### Q54: What is the TTL (Time-To-Live) Index in MongoDB?

**Answer:**

- Automatically deletes documents after a specified duration:

  ```javascript
  // Auto-delete session documents 3600 seconds (1 hour) after createdAt:
  db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });
  ```

- A background thread runs every 60 seconds, finds expired documents, and purges them without application code intervention.

---

### Q55: What is a Covered Query in MongoDB?

**Answer:**

- A query that can be satisfied **entirely from the index tree** without examining any actual documents from disk.
- **Requirements:**
  1. All fields in the query predicate exist in the index.
  2. All fields in the returned projection exist in the index.
  3. The `_id` field is explicitly excluded in the projection: `{ _id: 0, status: 1 }`.

---

### Q56: What is the difference between `$set` and full document replacement?

**Answer:**

- **`db.collection.replaceOne({ id: 1 }, { name: "Bob" })`**: Wipes the entire existing document, replacing it with only `{ name: "Bob" }` (deleting all other unmentioned fields).
- **`db.collection.updateOne({ id: 1 }, { $set: { name: "Bob" } })`**: Mutates only the `name` field in-place, leaving all other existing fields completely untouched.

---

### Q57: What is Read Preference in MongoDB (`primary`, `secondary`, `nearest`)?

**Answer:**
Determines which replica set node routes incoming read queries:

1. **`primary` (Default):** All reads go to Primary. Guarantees strict consistency.
2. **`primaryPreferred`:** Reads from Primary; falls back to Secondary if Primary is down.
3. **`secondary`:** Reads strictly from Secondaries (offloads read traffic, but risks replication lag).
4. **`nearest`:** Reads from the node with the lowest network ping latency (ideal for multi-region geo-distributed apps).

---

### Q58: How do Change Streams work in MongoDB?

**Answer:**

- Allows applications to listen to real-time data changes across collections, databases, or clusters without polling:

  ```javascript
  const changeStream = db.collection('orders').watch();
  changeStream.on('change', (next) => {
    console.log('Order changed:', next.operationType, next.fullDocument);
  });
  ```

- Backed by the internal replica set `oplog`, providing reliable real-time event streaming for notifications and caching invalidation.

---

### Q59: What is MongoDB Atlas Search?

**Answer:**

- Integrates an embedded **Apache Lucene** search engine directly alongside the WiredTiger storage engine.
- Provides full-text fuzzy search, autocomplete, faceted filtering, and BM25 relevance scoring without running a separate Elasticsearch cluster.

---

### Q60: How do you identify missing indexes in MongoDB using Profiler?

**Answer:**

1. Enable database profiling: `db.setProfilingLevel(1, { slowms: 100 })` (logs operations taking $> 100\text{ms}$).
2. Query `system.profile` collection:

   ```javascript
   db.system.profile.find({ planSummary: "COLLSCAN" }).sort({ ts: -1 });
   ```

   Documents with **`planSummary: "COLLSCAN"`** represent full table collection scans scanning thousands of documents, indicating a missing index!
