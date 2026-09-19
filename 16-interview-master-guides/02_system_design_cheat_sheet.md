# System Design Master Cheat Sheet (Formulas, Trade-offs & Numbers)

---

## 📊 1. Back-of-the-Envelope Math & Numbers Everyone Should Know
- $1 \text{ Million Requests/day} \approx 12 \text{ Requests/second (QPS)}$.
- $100 \text{ Million Requests/day} \approx 1,200 \text{ QPS}$.
- $1 \text{ Billion Requests/day} \approx 12,000 \text{ QPS}$.
- **Latency Numbers**:
  - L1 Cache reference: $0.5 \text{ ns}$.
  - Main Memory (RAM) reference: $100 \text{ ns}$.
  - Read $1 \text{ MB}$ sequentially from RAM: $250 \text{ µs}$.
  - Read $1 \text{ MB}$ sequentially from SSD: $1 \text{ ms}$.
  - Send packet California to Netherlands & back: $150 \text{ ms}$.

---

## ⚖️ 2. Architectural Trade-offs
- **CAP Theorem**: In the presence of a Network Partition ($P$), choose between Consistency ($C$) or Availability ($A$).
- **PACELC Theorem**: If Partition ($P$), choose $A$ vs $C$; Else ($E$), choose Latency ($L$) vs Consistency ($C$).
- **Cache Invalidation Patterns**:
  - **Cache-Aside**: App reads cache; if miss, reads DB, writes to cache. (Most flexible).
  - **Write-Through**: App writes to cache; cache writes to DB synchronously. (Consistent, higher write latency).
  - **Write-Behind (Write-Back)**: App writes to cache; cache asynchronously writes to DB in batch. (Fast writes, risk of data loss on crash).
