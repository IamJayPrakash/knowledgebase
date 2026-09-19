# System Design Master Interview Bank: Part 2 (Q21 - Q40)
## Distributed Systems, Consensus, CAP Theorem & Consistency

---

### Q21: Explain the CAP Theorem with concrete real-world examples.
**Answer:**
The **CAP Theorem (Brewer's Theorem)** states that a distributed data store can simultaneously provide at most two of the following three guarantees in the presence of a **Network Partition (P)**:

```
                          Consistency (C)
                               /\
                              /  \
                             /    \
                 RDBMS /    /      \  Spanner /
               CockroachDB /   CA   \ HBase
                          / (No Part) \
                         /             \
      Availability (A) ─────────────────── Partition Tolerance (P)
                          DynamoDB / Cassandra
                                (AP)
```

1. **Consistency (Linearizability):** Every read receives the most recent write or an error.
2. **Availability:** Every non-failing node returns a non-error response (without guarantee that it contains the most recent write).
3. **Partition Tolerance:** The system continues to operate despite arbitrary network dropped packets or node partitions.

**The Reality:** In distributed physical networks, network partitions are inevitable. Therefore, the choice is strictly between:
- **CP (Consistency over Availability):** Reject requests or return an error if a quorum cannot be reached (e.g., Banking, Stock Exchange, Google Spanner).
- **AP (Availability over Consistency):** Accept reads and writes on partitioned nodes and resolve inconsistencies later via eventual consistency (e.g., Shopping Cart, DNS, Social media feed).

---

### Q22: What is the PACELC Theorem and why was it created?
**Answer:**
The CAP theorem only applies when there is an active network partition ($P$). In normal operating conditions (99.9% of the time), there is no partition.
The **PACELC Theorem** (Daniel Abadi) extends CAP:
- **If Partition (P):** Trade-off between **Availability (A)** and **Consistency (C)**.
- **Else (E):** Trade-off between **Latency (L)** and **Consistency (C)**.

**System Classifications:**
- **PC/EC (e.g., Spanner, CockroachDB):** During partitions, favors Consistency; in normal operation, favors Consistency (paying higher Latency for cross-datacenter two-phase commits).
- **PA/EL (e.g., Cassandra, DynamoDB):** During partitions, favors Availability; in normal operation, favors low Latency (using asynchronous replica writes).

---

### Q23: What is the Quorum Consensus Formula ($R + W > N$)?
**Answer:**
In leaderless distributed databases (e.g., DynamoDB, Apache Cassandra):
- $N$ = Number of replication nodes.
- $W$ = Number of replicas that must acknowledge a write before it is considered successful.
- $R$ = Number of replicas that must be queried before returning a read result.

**Strong Consistency Condition:**
$$R + W > N$$
- By the Pigeonhole Principle, there is guaranteed to be **at least one overlapping node** that participated in both the latest write and the read.
- **Example ($N = 3$):** If $W = 2$ and $R = 2$, then $R + W = 4 > 3$. The read is guaranteed to see the latest write!
- **Sloppy Quorum & Hinted Handoff:** If network partitions prevent reaching quorum, nodes temporarily accept writes on behalf of unreachable peers and replay them when connectivity restores.

---

### Q24: What is a Split-Brain scenario in a distributed cluster and how do you prevent it?
**Answer:**
- **Split-Brain:** Occurs when a network partition cuts a cluster into two disconnected halves, and each half believes the other has died, resulting in **two nodes declaring themselves Leader**.
- Both leaders accept conflicting writes simultaneously, corrupting persistent data.
- **Prevention (Strict Quorum Rule):**
  A leader can only be elected or accept writes if it commands a **Strict Majority**:
  $$\text{Quorum} = \left\lfloor \frac{N}{2} \right\rfloor + 1$$
  - Clusters always require an **odd number of nodes** (3, 5, or 7).
  - In a 5-node cluster, Quorum is 3. A partition can only create a minority partition (2 nodes) and a majority partition (3 nodes). Only the majority partition can elect a leader, preventing dual-leader scenarios.

---

### Q25: How does the Raft Consensus Algorithm work?
**Answer:**
Raft breaks consensus into three clear sub-problems:
1. **Leader Election:**
   - Nodes start as **Followers**. If a follower stops receiving heartbeats within a randomized election timeout (150ms - 300ms), it transitions to **Candidate**, increments its `term`, votes for itself, and broadcasts `RequestVote`.
   - The first candidate to receive votes from a majority of nodes becomes **Leader**.
2. **Log Replication:**
   - Client sends a command to the Leader.
   - Leader appends command to its local log and sends `AppendEntries` RPC to followers.
   - When a majority of followers acknowledge writing to their logs, the leader commits the entry and responds to the client.
3. **Safety Guarantee:** A candidate can only win an election if its log is at least as up-to-date as any other node in the majority quorum.

---

### Q26: Explain the spectrum of Consistency Models from Strong to Weak.
**Answer:**
```
[ Strict / Linearizable ] ──► Every read sees the latest globally ordered write instantly.
         │
[ Sequential Consistency ] ──► Operations follow a valid global interleaving preserving program order.
         │
[ Causal Consistency ]   ──► Causally related writes are seen in order; concurrent writes in any order.
         │
[ Read-Your-Own-Writes ] ──► A user always sees updates made by themselves.
         │
[ Monotonic Reads ]      ──► Successive reads by a user never observe older states than previously read.
         │
[ Eventual Consistency ] ──► Replicas will converge to identical values if no new updates occur.
```

---

### Q27: What is Linearizability and how does it differ from Serializability?
**Answer:**
- **Linearizability (Concurrency/Distributed Systems):** A guarantee on single-object reads and writes in real-time. Every read must observe the effect of the most recent write that completed in real-world wall-clock time.
- **Serializability (Database Transactions):** An isolation guarantee on multi-operation transactions (ACID "I"). Guarantees that concurrent transactions execute with outcomes equivalent to running them serially in some order, but places **no constraints on real-time ordering**.
- **Strict Serializability (External Consistency):** The holy grail combining both guarantees (e.g. Google Spanner using TrueTime GPS/atomic clocks).

---

### Q28: What are Vector Clocks and how do they detect write conflicts?
**Answer:**
- Physical wall-clock timestamps drift due to clock skew (NTP inaccuracies).
- A **Vector Clock** is an array of logical counters, one per node: $V = [c_1, c_2, \dots, c_n]$.
- Every time a node modifies data, it increments its own counter: $V[\text{self}] = V[\text{self}] + 1$.
- **Conflict Detection:**
  - Event $A$ happened-before Event $B$ ($A < B$) if every counter in $V_A \le V_B$ and at least one counter is strictly less.
  - If neither $V_A \le V_B$ nor $V_B \le V_A$, the writes occurred concurrently: a **conflict exists** that must be resolved (e.g., via CRDTs or application-level merges like Git conflict resolution).

---

### Q29: What are CRDTs (Conflict-free Replicated Data Types)?
**Answer:**
- **CRDT:** A data structure designed to be replicated across multiple nodes without requiring central coordination or distributed locks.
- Concurrent updates can be made independently on any node; nodes exchange updates and merge them using mathematical operations that are **Commutative, Associative, and Idempotent**:
  $$\text{Merge}(A, B) = \text{Merge}(B, A)$$
- **Use Cases:** Collaborative document editing (Google Docs, Figma), distributed shopping carts, distributed counters (Redis HyperLogLog).

---

### Q30: What is Erasure Coding and how does it compare to 3x Replication in Object Storage?
**Answer:**
- **$3\times$ Replication:** Stores 3 identical copies of every file across different racks/datacenters.
  - *Storage Overhead:* **200% overhead (300% total data)**.
- **Erasure Coding (Reed-Solomon $k + m$):**
  - Breaks a file into $k$ data chunks and computes $m$ parity chunks (Total = $k + m$ chunks stored on different nodes).
  - The original file can be completely reconstructed from **any $k$ chunks**.
  - *Example (10 data chunks + 4 parity chunks):* Can survive the loss of **any 4 storage disks simultaneously**, with only **40% storage overhead** (compared to 200% for replication)!
  - *Trade-off:* High CPU/network reconstruction cost during node failures.

---

### Q31: What is Service Discovery and how does Client-Side vs Server-Side Discovery compare?
**Answer:**
In dynamic cloud/Kubernetes environments, microservice IP addresses change constantly due to autoscaling, rollouts, and node terminations.
- **Client-Side Service Discovery (e.g. Netflix Eureka / Ribbon):**
  Client queries a Service Registry (Consul, Eureka), receives available IP addresses, and performs local client-side load balancing.
  - *Pros:* Direct connection without intermediate network proxy hop.
  - *Cons:* Couples client code with language-specific discovery libraries.
- **Server-Side Service Discovery (e.g. Kubernetes Service / AWS ALB):**
  Client sends request to a stable virtual IP or DNS name. The platform proxy/load balancer routes traffic to a healthy pod.
  - *Pros:* Language-agnostic; clean decoupling.
  - *Cons:* Additional network proxy hop.

---

### Q32: What is a Distributed Correlation ID and how does W3C TraceContext propagate it?
**Answer:**
- **Correlation ID (Trace ID):** A unique identifier (UUID) assigned to a request at the edge API Gateway.
- As the request traverses microservices, queues, and databases, this ID is passed along in HTTP headers (e.g., `X-Correlation-ID` or standard `traceparent`).
- Every service logs the ID in structured JSON logs.
- **W3C TraceContext Standard:**
  Format: `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
  (`version - trace_id - parent_span_id - trace_flags`).
- Allows centralized log analytics engines (Datadog, OpenTelemetry, Jaeger) to reconstruct the exact end-to-end distributed execution span.

---

### Q33: What is the Two-Phase Commit (2PC) Protocol and what are its major failure modes?
**Answer:**
A distributed algorithm that coordinates all participating database nodes to commit or abort a transaction atomically:
1. **Prepare Phase:** Coordinator asks all participants: "Can you commit?". Participants acquire local locks, write undo/redo logs, and vote YES or NO.
2. **Commit Phase:** If all vote YES, Coordinator broadcasts COMMIT. If any votes NO, Coordinator broadcasts ROLLBACK.
- **Failure Modes:**
  1. **Blocking Protocol:** If the Coordinator crashes after participants vote YES, participants are left hanging indefinitely holding row locks, causing connection pool exhaustion.
  2. **High Latency:** Requires multiple network round-trips with synchronous distributed lock contention.

---

### Q34: What is the Saga Pattern and when should you choose Choreography vs Orchestration?
**Answer:**
The **Saga Pattern** manages distributed transactions across microservices as a sequence of local transactions:
- If a local transaction fails, the Saga executes **Compensating Transactions** to undo preceding changes in reverse order.
- **Choreography (Event-Driven):**
  - Services publish and listen to domain events over Kafka/RabbitMQ without a central coordinator.
  - *Pros:* Highly decoupled, simple for 2-3 services.
  - *Cons:* Difficult to track workflow state; cyclic event loop risks.
- **Orchestration (Central Coordinator):**
  - A dedicated orchestrator service (e.g., Temporal, AWS Step Functions) commands each service what to do and tracks state.
  - *Pros:* Centralized visibility, easy to debug and test.

---

### Q35: What is Synchronous vs Asynchronous Communication and what are the trade-offs?
**Answer:**
- **Synchronous (REST / gRPC):** Client blocks and waits for immediate server response.
  - *Pros:* Simple request/response semantics; instant feedback.
  - *Cons:* Cascading failure risk; temporal coupling (both services must be online simultaneously).
- **Asynchronous (Message Queues / Kafka):** Producer sends message to broker and continues without waiting for consumer processing.
  - *Pros:* Temporal decoupling, load leveling / buffer absorption, high resilience.
  - *Cons:* Eventual consistency, complex debugging, out-of-order delivery handling required.

---

### Q36: How does Distributed Leader Election work using etcd or ZooKeeper?
**Answer:**
- **Ephemeral Leases with Heartbeats:**
  1. Competing nodes attempt to create a unique distributed key (e.g., `/services/master/leader`) with an ephemeral lease (e.g., 5 seconds).
  2. Exactly one node succeeds using atomic Compare-And-Swap (`CAS`). That node is elected Leader.
  3. The leader sends periodic heartbeats to renew the lease.
  4. If the leader crashes, the lease expires, the ephemeral key is automatically deleted, and followers receive a watch notification to compete for the next election.

---

### Q37: What is Monotonic Read Consistency?
**Answer:**
- A consistency model guaranteeing that if a user reads a value at timestamp $T$, all subsequent reads by that user will observe that value or a newer value, never an older state.
- **Scenario Prevented:** A user reads comments, refreshes, hits a replica that is 5 seconds behind, and observes comments that were visible a second ago disappear!

---

### Q38: What is Gossip Protocol and where is it used?
**Answer:**
- A peer-to-peer decentralized communication protocol modeled after epidemic disease spreading.
- Nodes periodically choose random peer nodes and exchange cluster state metadata (membership, heartbeats, node health).
- Convergence is exponential: information spreads across an $N$-node cluster in $O(\log N)$ rounds.
- **Used by:** Apache Cassandra (cluster membership & node failure detection), Consul, DynamoDB.

---

### Q39: What is Lamport Timestamp and how does it define partial ordering?
**Answer:**
- A simple logical clock counter maintained by each process.
- **Algorithm:**
  1. Increment local clock before executing any local event: $C = C + 1$.
  2. When sending a message, include local clock timestamp $C$.
  3. When receiving a message with timestamp $C_{msg}$, set local clock:
     $$C_{\text{local}} = \max(C_{\text{local}}, C_{msg}) + 1$$
- Provides a strict **partial ordering** of events without relying on physical synchronized clocks.

---

### Q40: What is Read-Repair in Distributed Databases?
**Answer:**
- In leaderless systems (Cassandra), when a client performs a read with $R > 1$, the coordinator node queries $R$ replicas.
- If the coordinator discovers that 2 replicas return Version 5 and 1 replica returns an older Version 4:
  1. It returns the latest Version 5 to the client immediately.
  2. It sends an asynchronous **Read-Repair** write in the background to update the stale replica to Version 5.
