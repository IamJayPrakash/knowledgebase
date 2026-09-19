# Top System Design High-Frequency Interview Problems Catalog

---

## 1. Design a Distributed Unique ID Generator (Twitter Snowflake)

### Requirements & Constraints:
- 64-bit numeric IDs.
- Globally unique, roughly time-sorted, capable of generating 10,000+ IDs per second per node.

### Snowflake 64-Bit Structure:
```
  [ 1 Bit: Sign (0) ] 
  [ 41 Bits: Timestamp in Milliseconds (Epoch offset provides ~69 years) ] 
  [ 10 Bits: Machine / Datacenter Node ID (Supports 1024 distinct nodes) ] 
  [ 12 Bits: Per-Node Sequence Counter (Supports 4096 IDs per ms per node) ]
```

### Python Implementation:
```python
import time

class SnowflakeIDGenerator:
    def __init__(self, node_id: int, epoch: int = 1704067200000):
        self.node_id = node_id # 0 - 1023
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1

    def generate_id(self) -> int:
        now = int(time.time() * 1000)
        if now < self.last_timestamp:
            raise Exception("Clock moved backwards! Refusing to generate ID.")

        if now == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF # 12 bits max (4095)
            if self.sequence == 0:
                # Sequence exhausted for this millisecond, wait for next ms
                while now <= self.last_timestamp:
                    now = int(time.time() * 1000)
        else:
            self.sequence = 0

        self.last_timestamp = now

        # Construct 64-bit ID using bit-shifting
        snowflake_id = (
            ((now - self.epoch) << 22) |
            (self.node_id << 12) |
            self.sequence
        )
        return snowflake_id

generator = SnowflakeIDGenerator(node_id=7)
print("Generated Snowflake ID:", generator.generate_id())
```

---

## 2. Design a Distributed Key-Value Store (Dynamo Style)
- **Data Partitioning**: Consistent Hashing with virtual nodes.
- **Replication**: Sloppy Quorum and Hinted Handoff ($N=3, R=2, W=2$).
- **Conflict Resolution**: Vector Clocks and Read Repair.
- **Node Failure Detection**: Gossip Protocol.

---

## 3. Design a Scalable Notification System
- **Scale**: 100 Million notifications per day.
- **Components**:
  - API Gateway -> Rate Limiter -> Notification Ingestion Service -> Kafka Message Topic (Priority: Critical vs Bulk) -> Notification Worker Pool -> Third-Party Providers (APNs for iOS, FCM for Android, Twilio for SMS, SendGrid for Email).
  - User Preference Cache in Redis (DND hours, opted-out categories).

---

## 4. Design a Distributed Web Crawler
- **Scale**: 1 Billion web pages per month.
- **Components**:
  - URL Frontier (Priority Queue + Politeness Queue with Hostname hashing).
  - DNS Cache (Pre-resolved hostnames).
  - HTML Fetcher & Parser.
  - Content Seen Detector (Fingerprinting via SimHash to eliminate duplicate pages).
  - URL Filter (`robots.txt` compliance).
