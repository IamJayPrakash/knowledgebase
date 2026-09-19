# Distributed Systems Primitives: CAP Theorem, Raft Consensus, and Consistent Hashing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

**CAP Theorem**: Socho do dost hain (Server A aur Server B). Beech ka telephone taar toot gaya (**Network Partition**). Ab agar ek customer Server A par aakar balance update karta hai, toh ya toh Server A update accept karega lekin Server B ko nahi pata hoga (**Availability jeeti, Consistency haari - AP**), ya fir Server A customer ko mana kar dega: "Phone line kharab hai, transaction cancelled!" (**Consistency jeeti, Availability haari - CP**)!
**Consistent Hashing**: Ek **Gol Ring (Round Dining Table)** ki tarah hai. Jab naya dost khane par aata hai, toh sabko apni kursi chhod kar nayi jagah nahi baithna padta; sirf ek padosi ki plate se thoda sa khana share hota hai!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **CAP Theorem in Reality**:
   - Network partitions ($P$) are inevitable in physical distributed networks (switch failures, fiber cuts).
   - Therefore, system design is a choice between **CP** (Consistent under Partition) and **AP** (Available under Partition).
   - CA (Consistent + Available without Partition) cannot exist across physical networks.
2. **PACELC Theorem**:
   - Expands CAP: **If Partition ($P$)**: choose Availability ($A$) vs Consistency ($C$); **Else ($E$)**: choose Latency ($L$) vs Consistency ($C$).
3. **Consensus Algorithms (Raft)**:
   - Three roles: Leader, Follower, Candidate.
   - Leader handles all client writes, appends log entries, and broadcasts `AppendEntries` RPCs.
   - Quorum rule: Requires majority $\lfloor N/2
floor + 1$ acknowledgments to commit.
4. **Consistent Hashing**:
   - Maps both servers and keys onto a $2^{32} - 1$ hash ring.
   - Adding or removing a server node only relocates $K/N$ keys on average.
   - **Virtual Nodes (vnodes)**: Distribute each physical server across 100-256 virtual points on the ring, guaranteeing uniform data distribution.

---

## 📊 3. Visual Architecture Diagram

```
                 CONSISTENT HASHING VIRTUAL NODE RING
                 
                         [ Server A (v1) ]
                            0 / 2^32-1
                           /           |
         [ Server C (v2) ]             [ Server B (v1) ]
                 |                             |
                 |      KEY HASH PLACEMENT     |
                 |      key1 ──► Server B      |
                 |      key2 ──► Server C      |
                 |                             |
         [ Server B (v2) ]             [ Server A (v2) ]
                           |           /
                         [ Server C (v1) ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets (Python Consistent Hashing)

```python
import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, replicas: int = 100):
        # Line 6: Number of virtual nodes per physical node
        self.replicas = replicas
        # Line 8: Sorted list of virtual node hashes on the ring
        self.ring = []
        # Line 10: Hash -> Physical node name map
        self.hash_to_node = {}

    def _hash(self, key: str) -> int:
        # Generate 32-bit integer hash from MD5 digest
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16) & 0xFFFFFFFF

    def add_node(self, node: str):
        # Line 17: Place multiple virtual nodes across the ring
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            vnode_hash = self._hash(vnode_key)
            bisect.insort(self.ring, vnode_hash)
            self.hash_to_node[vnode_hash] = node

    def remove_node(self, node: str):
        # Remove all virtual replicas of node
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            vnode_hash = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, vnode_hash)
            if idx < len(self.ring) and self.ring[idx] == vnode_hash:
                del self.ring[idx]
                del self.hash_to_node[vnode_hash]

    def get_node(self, key: str) -> str:
        if not self.ring:
            return None

        # Line 37: Hash the target key and binary search the clockwise successor node
        key_hash = self._hash(key)
        idx = bisect.bisect_right(self.ring, key_hash)

        # If key_hash is beyond the last node, wrap around to index 0 (Ring behavior)
        if idx == len(self.ring):
            idx = 0

        return self.hash_to_node[self.ring[idx]]

# Verification:
ring = ConsistentHashRing(replicas=150)
ring.add_node("cache-node-1")
ring.add_node("cache-node-2")
ring.add_node("cache-node-3")

print("Routing user_101:", ring.get_node("user_101"))
print("Routing user_102:", ring.get_node("user_102"))
```

---

## 🎯 5. The "Interview Pitch"
>
> "In distributed data systems, Consistent Hashing is the cornerstone of horizontal data partitioning and caching tiers. Unlike traditional modular hashing (`hash(key) % N`) where adding a single server invalidates $100\%$ of mapped keys and causes a devastating cache stampede, consistent hashing places both nodes and keys on a circular hash space. Adding or removing a node relocates only $K/N$ keys. We assign virtual nodes to each physical server to eliminate hot-spotting and ensure uniform key distribution across asymmetric hardware."
