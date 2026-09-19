# System Design Master Interview Bank: Part 5 (Q81 - Q100)

## Top 20 Real-World High-Level System Design Architectures

---

### Q81: Design a Scalable URL Shortener (TinyURL / Bitly)

**Architecture & Key Decisions:**

1. **Capacity Estimation:** 500M new URLs/month. Read-to-write ratio = 10:1. Total URLs in 5 years = 30 Billion.
2. **Short URL Encoding:**
   - Base62 characters: `[0-9, a-z, A-Z]`.
   - Length 7 characters provides $62^7 \approx 3.5 \text{ Trillion}$ combinations (sufficient for 500 years).
3. **Collision-Free Generation via Key Generation Service (KGS):**
   - Hashing MD5/SHA-256 of the long URL requires collision resolution.
   - Better approach: A standalone **Key Generation Service (KGS)** pre-generates 7-character Base62 strings in memory and stores them in two tables: `unused_keys` and `used_keys`.
   - Application servers grab a batch of 1,000 keys from KGS into memory, eliminating DB locks on write.
4. **Data Store:** NoSQL Key-Value Store (DynamoDB / Cassandra) or MongoDB. Schema: `short_key (PK), original_url, user_id, created_at, expires_at`.
5. **Caching & Redirect:** Redis cache holds top 20% most accessed URLs. Return HTTP 301 (Permanent Redirect) for CDN caching or HTTP 302 (Temporary) for analytics tracking.

---

### Q82: Design a Social Media News Feed (Twitter / Instagram)

**Architecture & Key Decisions:**

1. **Fanout on Write (Push Model):**
   - When a user posts a tweet, find all followers and inject the `tweet_id` into each follower's pre-computed Redis timeline list.
   - *Advantage:* Instant read latency ($O(1)$ read from Redis).
   - *Flaw:* Celebrity problem (Justin Bieber with 100M followers requires 100M Redis list writes, freezing the ingestion pipeline).
2. **Fanout on Read (Pull Model):**
   - Timeline is generated dynamically when the user requests their feed by querying tweets from all followed accounts and merge-sorting by timestamp.
   - *Advantage:* Fast write latency.
   - *Flaw:* Extremely slow read latency for users following thousands of accounts.
3. **The Hybrid Solution (Production Standard):**
   - Standard users ($< 25,000$ followers) use **Fanout on Write**.
   - Celebrities / VIPs ($> 25,000$ followers) use **Fanout on Read**.
   - When a normal user loads their feed, their pre-computed timeline is merged with recent tweets from the celebrities they follow.

---

### Q83: Design a Real-Time Chat & Messaging Platform (WhatsApp / Discord)

**Architecture & Key Decisions:**

1. **Connection Layer:** Statefull **WebSocket Gateway** clusters maintaining persistent TCP connections with online users.
2. **User Session Registry:** Distributed Redis cluster mapping `user_id -> gateway_server_ip`.
3. **Message Routing Flow:**
   - User A sends message to Gateway 1.
   - Gateway 1 queries Redis: finds User B is connected to Gateway 4.
   - Gateway 1 forwards message to Gateway 4 via internal gRPC/Kafka.
   - Gateway 4 pushes message over User B's active WebSocket.
4. **Offline Messages:** If User B is offline, message is stored in Cassandra / DynamoDB. When User B reconnects, the client queries for messages since the last received message ID.
5. **Message Status Progression:** Sent (single tick - saved to server) $\to$ Delivered (double grey ticks - received by client device) $\to$ Read (blue ticks - opened in viewport).

---

### Q84: Design an E-Commerce Flash Sale & Inventory System (Black Friday / Flipkart Big Billion Days)

**Architecture & Key Decisions:**

1. **The Core Challenge:** 1,000,000 users attempting to purchase 1,000 items simultaneously without overselling or crashing the database.
2. **Layer 1: Static Edge Caching:** Product details page cached at CDN with 0ms origin load.
3. **Layer 2: Edge Rate Limiting:** Drop automated bot traffic and duplicate click spam at API Gateway.
4. **Layer 3: In-Memory Atomic Inventory Reservation:**
   - Storing inventory in PostgreSQL with `SELECT FOR UPDATE` causes massive lock contention and database connection timeouts.
   - Store inventory in a **Redis Cluster using Lua scripts**:

     ```lua
     local stock = tonumber(redis.call('get', KEYS[1]))
     if stock > 0 then
       redis.call('decr', KEYS[1])
       return 1 -- Success
     else
       return 0 -- Sold out!
     end
     ```

5. **Layer 4: Async Order Processing:** Successful Redis reservations emit an order event to a Kafka queue. Background workers pull orders from Kafka and persist to PostgreSQL at a steady, sustainable write rate.
6. **Payment Timeout:** If payment is not completed within 15 minutes, an event triggers stock increment back to Redis.

---

### Q85: Design a Proximity Service / Location-Based Search (Uber / Yelp)

**Architecture & Key Decisions:**

1. **The Spatial Problem:** Finding businesses within radius $R$ of latitude/longitude coordinates $(\text{lat}, \text{lng})$ requires 2D spatial indexing. Standard B-Trees are 1-dimensional.
2. **Spatial Indexing Options:**
   - **Geohash:** Hierarchical spatial index that encodes 2D lat/lng into a Base32 string. Prefix matching allows finding nearby bounding boxes (e.g. `dr5ru` is adjacent to `dr5rv`).
   - **QuadTree:** Tree structure where each internal node has exactly 4 children (NW, NE, SW, SE). Nodes subdivide when the number of locations in a region exceeds a threshold (e.g. 100).
   - **Google S2:** Maps the Earth sphere onto a cube divided into 30 hierarchical cell levels using Hilbert Space-Filling Curves. (Used by Uber).
3. **Storage:** Read-heavy data (places) stored in PostgreSQL with **PostGIS extension**; real-time moving driver coordinates stored in Redis Geospatial (`GEOADD` / `GEORADIUS`).

---

### Q86: Design a Video Streaming Service (YouTube / Netflix)

**Architecture & Key Decisions:**

1. **Video Ingestion & Transcoding Pipeline:**
   - User uploads master video file to Cloud Object Storage (S3 / GCS).
   - Ingestion service splits video into small 2-second to 10-second chunks.
   - Distributed worker cluster transcodes chunks into multiple formats (MP4, WebM) and resolutions (360p, 720p, 1080p, 4K) using ffmpeg.
2. **Adaptive Bitrate Streaming (ABR):**
   - Transcoder generates manifest files: **HLS (`.m3u8`)** and **DASH (`.mpd`)**.
   - Client video player continuously monitors network bandwidth. If network degrades, the player smoothly switches to requesting 480p chunks without buffering.
3. **Global CDN Edge Caching:** Popular videos (80/20 rule) are cached at regional CDN PoP edges directly inside Internet Service Provider (ISP) datacenters (Netflix Open Connect).

---

### Q87: Design a Distributed Web Crawler (Google / Search Engine)

**Architecture & Key Decisions:**

1. **URL Frontier:** Priority Queue of URLs to crawl. Enforces **Politeness** (not overwhelming any single host) via domain queues and delay timers.
2. **DNS Resolver Cache:** Local in-memory DNS caching to avoid repeating expensive DNS queries for millions of URLs.
3. **HTML Fetcher & Parser:** Asynchronous headless browsers executing JavaScript and extracting anchor links.
4. **Duplicate Content Detection:** **SimHash / MinHash** algorithms compute 64-bit fingerprint of webpage text to detect near-duplicate pages.
5. **URL Seen Filter:** Massive distributed **Bloom Filter** to verify whether a URL has already been crawled in $O(1)$ time without database queries.

---

### Q88: Design a Collaborative Real-Time Document Editor (Google Docs / Figma)

**Architecture & Key Decisions:**

1. **The Concurrency Problem:** Multiple users typing simultaneously at different positions in the same document without overwriting each other's edits.
2. **Operational Transformation (OT - Google Docs):**
   - Centralized server orders all operations.
   - Operations (Insert, Delete, Retain) are transformed against concurrent operations based on character offset indices before applying.
3. **Conflict-Free Replicated Data Types (CRDT - Figma / Modern Docs):**
   - Peer-to-peer decentralized model.
   - Assigns unique, fractional position identifiers to every character/node (e.g., LSEQ / Yjs).
   - Operations commute mathematically without requiring a central coordinator.
4. **Transport:** WebSockets over TLS with client-side local optimistic echo rendering.

---

### Q89: Design a Distributed Unique ID Generator (Twitter Snowflake)

**Architecture & Key Decisions:**

1. **Requirements:** 64-bit integer (fits in `BIGINT`), globally unique, monotonically roughly time-ordered, capable of generating $> 100,000\text{ IDs/sec}$.
2. **Snowflake 64-Bit Bit Allocation:**

   ```
   1 bit: Sign bit (always 0)
   41 bits: Epoch Timestamp in milliseconds (Provides 69 years of unique IDs)
   5 bits: DataCenter ID (0 - 31)
   5 bits: Worker Node ID (0 - 31)
   12 bits: Local Sequence Number (0 - 4095 per millisecond per node)
   ```

3. **Throughput:** $4,096 \text{ IDs/millisecond/node} \approx 4.096 \text{ Million IDs/sec}$ per node with zero network lock contention!
4. **Clock Drift Protection:** If physical clock jumps backward (NTP sync), the generator pauses or rejects requests until the clock catches up to the previous timestamp.

---

### Q90: Design a Real-Time Ride-Sharing Matching Engine (Uber / Grab)

**Architecture & Key Decisions:**

1. **Driver Location Ingestion:** Drivers emit GPS location every 4 seconds. Handled by a high-throughput Netty / Go WebSocket gateway.
2. **Spatial Partitioning (Uber H3):** Earth is divided into hexagonal grid cells of varying resolutions.
3. **In-Memory Location Index:** Hexagon cells hold sets of available `driver_ids` in Redis.
4. **Matchmaking Engine:**
   - Rider requests pickup at coordinate $(\text{lat}, \text{lng})$.
   - Engine finds the rider's H3 hexagon and searches expanding concentric rings of neighboring hexagons.
   - Filters candidate drivers by status (`AVAILABLE`), rating, and vehicle class.
   - Emits match offer to the closest driver via WebSocket with a 15-second acceptance timer.

---

### Q91: Design a Distributed Metrics Monitoring & Alerting System (Datadog / Prometheus)

**Architecture & Key Decisions:**

1. **Metrics Collection:** Push vs Pull model. (Prometheus pulls metrics from `/metrics` endpoints; StatsD pushes UDP packets).
2. **Time-Series Database (TSDB):**
   - Writes are 99% append-only time-series data: `(metric_name, labels, timestamp, value)`.
   - Uses Gorilla time-series compression (delta-of-delta timestamp encoding and XOR floating-point compression) reducing 16 bytes down to 1.37 bytes per sample.
3. **Downsampling & Retention Policy:** Raw metrics kept for 7 days $\to$ downsampled to 1-minute rollups for 30 days $\to$ 1-hour rollups for 1 year.
4. **Alert Manager:** Evaluates alerting rules against incoming metrics stream and dispatches notifications (PagerDuty, Slack).

---

### Q92: Design a Search Typeahead / Autocomplete System (Google Search)

**Architecture & Key Decisions:**

1. **Core Data Structure:** **Trie (Prefix Tree)** stored in RAM.
   - Each Trie node stores the character and pre-computes the **Top 5 most frequent search queries** starting with that prefix.
2. **Offline Aggregation Pipeline:**
   - Query logs stream through Kafka into Spark/Flink jobs.
   - Computes query frequency counts using a sliding window.
   - Reconstructs a fresh Trie snapshot and pushes to read-only memory caches weekly.
3. **Edge Optimization:** Caching top search prefixes at browser local storage and CDN edge servers.

---

### Q93: Design a Cloud File Storage & Synchronization Service (Dropbox / Google Drive)

**Architecture & Key Decisions:**

1. **Block-Level Chunking:** Files are split into fixed 4MB chunks.
2. **Content-Addressable Storage (CAS):** Each chunk is hashed using SHA-256 (`chunk_hash`).
   - Enables **Global Deduplication**: If multiple users upload the same 4GB operating system ISO, the file is stored in S3 exactly once.
3. **Delta Sync:** When a user modifies a 100MB file, only the modified 4MB chunks are uploaded over the network.
4. **Metadata DB:** Relational DB (PostgreSQL) tracks user file directory trees, permissions, versions, and lists of chunk hashes.

---

### Q94: Design a Webhook Delivery Engine (Stripe / GitHub)

**Architecture & Key Decisions:**

1. **The Challenge:** Delivering millions of HTTP POST notifications to third-party customer servers that may be down, slow, or misconfigured.
2. **Queue Architecture:** Kafka queues partition events by `customer_id` to guarantee in-order delivery per tenant.
3. **Security:** Every webhook request includes an **HMAC-SHA256 signature** in headers (`X-Signature`) computed with customer's secret key to prevent spoofing.
4. **Resilience & Exponential Retry Schedule:**
   - Retries failed deliveries with exponential backoff: Immediate $\to$ 5m $\to$ 30m $\to$ 2h $\to$ 24h.
   - Circuit breakers trip on endpoints with persistent 5xx errors to prevent tying up worker threads.

---

### Q95: Design a High-Volume Ad Click Event Aggregator (Click Fraud Detection)

**Architecture & Key Decisions:**

1. **Scale:** 100,000 clicks/sec. Financial advertisers must be billed accurately without double-counting click fraud.
2. **Ingestion Layer:** Load balancers distribute clicks to stateless API servers emitting to Kafka topics partitioned by `ad_id`.
3. **Click Deduplication (Sliding Window):**
   - Distributed Redis Bloom filter rejects identical clicks (same `user_id` and `ad_id` within 1 minute).
4. **Real-Time Stream Aggregation:** Apache Flink aggregates valid clicks into 1-minute tumbling windows and flushes counts to ClickHouse / Cassandra for advertiser dashboards.

---

### Q96: Design a Distributed Lock Manager (Redlock vs ZooKeeper/etcd)

**Architecture & Key Decisions:**

1. **Redis Redlock:**
   - Client attempts to acquire lock across $N$ independent Redis master nodes (e.g. 5 nodes) using `SET resource_name my_random_value NX PX 30000`.
   - Lock is acquired if client gets lock on majority ($\ge 3$) nodes within a timeout.
   - *Criticism (Martin Kleppmann):* Clock jumps and GC pauses can invalidate the lock while client continues executing.
2. **Fencing Tokens (Safe Solution):**
   - The lock server returns a monotonically increasing integer **fencing token** ($1, 2, 3$).
   - Persistent storage rejects any write that arrives with a fencing token lower than the highest token previously observed.

---

### Q97: Design an Online Payment Gateway & Financial Ledger System (Stripe / PayPal)

**Architecture & Key Decisions:**

1. **Two-Phase Payment Flow:**
   - **Authorize:** Reserves funds on customer's credit card.
   - **Capture:** Transfers funds after order fulfillment.
2. **Strict Idempotency:** Client must supply an `Idempotency-Key` header with every payment request. Checked in Redis/Postgres before touching bank rails.
3. **Double-Entry Bookkeeping:**
   - Money is never "updated" or overwritten.
   - Every transaction consists of equal and offsetting **Debit** and **Credit** ledger entries:
     $$\sum \text{Debits} = \sum \text{Credits}$$
   - Implemented using immutable append-only relational tables with ACID serializable transactions.

---

### Q98: Design a Live Video Streaming Chat (Twitch / YouTube Live with 10M Viewers)

**Architecture & Key Decisions:**

1. **The Broadcast Fanout Problem:** If a creator has 1,000,000 concurrent viewers and chat messages flow at 1,000 messages/sec, sending every message to every viewer requires 1 Billion socket writes/sec (impossible for standard WebSockets).
2. **Chat Room Sharding:**
   - The single live chat room is divided into virtual sub-rooms (e.g., 100 sub-rooms).
   - Viewers are randomly distributed across sub-rooms.
3. **Sampling & Rate Limiting:**
   - User messages are rate-limited (1 message per 30 seconds per user).
   - During massive surges, chat servers **sample messages** (e.g., broadcasting only 1 out of 10 messages) to match human visual reading speed (~10-20 messages/sec max).

---

### Q99: Design a Distributed Web Gateway API Rate Limiter (Cloudflare / Kong)

**Architecture & Key Decisions:**

1. **Multi-Tier Rate Limiting:**
   - **Tier 1 (Edge CDN):** BGP Anycast and WAF drop known DDoS IPs, volumetric SYN floods, and blacklisted user agents.
   - **Tier 2 (Gateway Layer):** Distributed Token Bucket backed by Redis cluster enforcing tenant API limits (e.g., 1,000 requests/minute).
2. **Local Token Caching (Reducing Redis Round-Trips):**
   - Application gateway pods grab batches of 50 tokens from Redis into local memory.
   - Decrements local memory tokens; only hits Redis when local quota runs low, reducing Redis network overhead by 98%.

---

### Q100: Design a Global Notification Service (Twilio / Firebase Cloud Messaging)

**Architecture & Key Decisions:**

1. **Multi-Channel Delivery:** Orchestrates Push (APNS, FCM), SMS (Twilio, Sinch), and Email (SendGrid, SES).
2. **User Preferences & Quiet Hours:**
   - Database stores user notification preferences, language, and quiet hours (e.g., no push notifications between 10 PM and 7 AM in user's local timezone).
3. **Priority Queues:**
   - Dedicated Kafka topics: `high_priority` (OTPs, fraud alerts) vs `low_priority` (marketing promotions).
4. **Provider Failover:** If Twilio returns 5xx or SMS delivery rate drops below 90%, the service automatically switches traffic to Sinch in real-time.
