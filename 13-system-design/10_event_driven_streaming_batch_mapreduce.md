# Event-Driven Architecture, Stream Processing, and MapReduce

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Batch Processing (MapReduce)** ek **Mahine Ke Akhir Ka Electricity Bill** hai: Poore 30 din ka data jama hota hai, raat ko ek sath calculate hota hai aur subah bill nikalta hai.
**Stream Processing (Kafka / Flink)** ek **Live Electric Meter Counter** hai: Jaise hi aapne fan on kiya, meter ka pahiya ghoomta hai aur live reading reflect hoti hai (Millisecond real-time event calculation).
**Exactly-Once Processing**: Banking ATM jaisa hai: Chahe network disconnect ho jaye, aapke account se paisa do baar deduct nahi hoga.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Message Queue vs Event Stream**:
   - Queue (RabbitMQ): Messages deleted immediately after worker acknowledgment (ACK).
   - Event Stream (Kafka): Append-only immutable commit log retained on disk for days/months; consumers track their own offsets.
2. **Delivery Semantics**:
   - **At-Most-Once**: Message delivered 0 or 1 time (messages may be lost).
   - **At-Least-Once**: Message delivered 1 or more times (requires consumer idempotency).
   - **Exactly-Once**: Transactional coordination between producer, log, and consumer state (Kafka Transactions + 2-Phase Commit).
3. **Kappa vs Lambda Architecture**:
   - **Lambda**: Parallel Batch layer (Hadoop) for accuracy + Speed layer (Storm) for low latency. High maintenance.
   - **Kappa**: Single Stream processing layer (Flink/Kafka) for all real-time and historical re-processing.

---

## 💻 3. Line-by-Line Commented Code Snippets (Idempotent Consumer Pattern)

```python
# Production Idempotent Kafka Consumer Pattern
def process_payment_event(event: dict, redis_client, db_connection):
    event_id = event["event_id"]
    order_id = event["order_id"]
    amount = event["amount"]

    # Line 7: Atomically set event ID in Redis with 24-hour TTL to verify idempotency
    # SETNX returns 1 if key was set, 0 if already processed!
    is_new = redis_client.set(f"processed_event:{event_id}", "1", nx=True, ex=86400)

    if not is_new:
        print(f"[Duplicate Ignored] Event {event_id} already processed. Skipping.")
        return

    # Line 15: Safe to execute database mutation
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("UPDATE orders SET payment_status = 'PAID' WHERE id = %s", (order_id,))
            db_connection.commit()
            print(f"[Success] Order {order_id} marked as PAID.")
    except Exception as err:
        # Revert Redis key if DB fails so message can be retried safely
        redis_client.delete(f"processed_event:{event_id}")
        raise err
```
