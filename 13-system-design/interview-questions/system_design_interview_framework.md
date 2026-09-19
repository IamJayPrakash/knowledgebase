# Master System Design Interview Framework (The 4-Step Playbook)

---

## 🎯 The 4-Step Structural Playbook

### Step 1: Requirements Clarification & Scope (5-7 Minutes)
- **Functional Requirements**: 3 core user journeys (e.g. "User can shorten URL", "User is redirected to original URL", "Analytics tracking").
- **Non-Functional Requirements**: High availability vs Strong consistency (CAP Theorem), latency target (P99 < 50ms), throughput (Read:Write ratio).
- **Scale Estimations (Back of the Envelope)**: DAU, Read QPS, Write QPS, Storage per year, Network Bandwidth.

### Step 2: High-Level Architecture & API Design (10-12 Minutes)
- Define clean REST / gRPC API contracts.
- Draw main components: Client -> DNS/CDN -> API Gateway / Load Balancer -> Application Services -> Caching Layer -> Primary/Replica Databases.

### Step 3: Deep Dive into Core Bottlenecks (15-20 Minutes)
- Partitioning/Sharding strategy (Hash vs Range).
- Caching policies (Cache-Aside, Write-Through, LRU).
- Fault tolerance, replication lag, and split-brain scenarios.

### Step 4: Wrap-Up, Resilience & Bottleneck Resolution (5 Minutes)
- Single Point of Failure (SPOF) audit.
- Rate limiting, Circuit Breakers, and DDoS mitigation.
- Monitoring, SLIs, and SLOs (Prometheus/Grafana).
