# System Design Master Interview Bank: Part 4 (Q61 - Q80)

## Protocols, Resilience, Security & SRE Patterns

---

### Q61: Compare Communication Protocols: REST vs GraphQL vs gRPC vs WebSockets vs WebRTC

**Answer:**

| Protocol | Transport | Serialization | Communication Model | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **REST** | HTTP/1.1 or HTTP/2 | JSON / XML | Request / Response (Stateless) | Public CRUD APIs, third-party webhooks. |
| **GraphQL** | HTTP/1.1 or HTTP/2 | JSON | Request / Response (Client specifies fields) | Mobile apps, aggregated dashboards (eliminates over/under-fetching). |
| **gRPC** | HTTP/2 (Multiplexed) | Protocol Buffers (Binary) | Bidirectional streaming, Unary RPC | Internal microservice-to-microservice high-speed communication. |
| **WebSockets** | TCP (Upgraded from HTTP) | Text / Binary | Full-duplex bidirectional persistent socket | Real-time chat, live financial tickers, multiplayer gaming. |
| **WebRTC** | UDP (SRTP / SCTP) | Binary media packets | Peer-to-Peer (P2P) ultra-low latency streaming | Audio/Video calls (Zoom, Google Meet), real-time file sharing. |

---

### Q62: How does HTTP/2 Multiplexing improve upon HTTP/1.1?

**Answer:**

- **HTTP/1.1 Head-of-Line (HoL) Blocking:** Browsers could send only one request per TCP connection at a time. Loading multiple assets required opening multiple parallel TCP connections (limited to 6 per domain).
- **HTTP/2 Multiplexing:**
  - Breaks requests and responses into independent binary frames tagged with a **Stream ID**.
  - Thousands of concurrent requests and responses are interleaved across a **single persistent TCP connection**.
  - A slow request no longer blocks subsequent requests from traveling across the wire.

---

### Q63: How does the Circuit Breaker Pattern work?

**Answer:**

```
                  ┌──────────────────────────────┐
                  │            CLOSED            │ ◄── Initial normal state.
                  │ Requests flow to downstream. │     Traffic flows freely.
                  └──────────────┬───────────────┘
                                 │
                 Failure threshold exceeded (e.g. >50% errors)
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │             OPEN             │ ◄── Fail Fast!
                  │ Fast fail: return fallback   │     Zero network calls to downstream.
                  └──────────────┬───────────────┘
                                 │
                     Sleep window expires (e.g. 10 seconds)
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │          HALF-OPEN           │ ◄── Probe downstream health
                  │ Allow canary trial requests. │
                  └──────┬────────────────┬──────┘
                         │                │
             Canary trials succeed        Canary trials fail
                         │                │
                         ▼                ▼
                     [ CLOSED ]        [ OPEN ]
```

---

### Q64: What is the Bulkhead Pattern?

**Answer:**

- Named after physical watertight bulkheads in ships: if the ship's hull is breached, water is contained inside one compartment, preventing the entire vessel from sinking.
- **In Software:** Partitioning system resources (thread pools, CPU, memory, database connection pools) into isolated compartments:
  - If Service A's dedicated thread pool is exhausted by a slow downstream dependency, Service B and Service C continue operating normally on their independent thread pools without cascading collapse.

---

### Q65: Why is Exponential Backoff with Full Jitter mandatory for Distributed Retries?

**Answer:**

- **Naive Fixed Retry:** If 1,000 clients fail simultaneously due to a brief network blip and retry after exactly 1 second, all 1,000 clients hit the server again at the exact same millisecond, triggering a **Retry Storm (Self-inflicted DDoS)**.
- **Exponential Backoff:** Doubles the wait interval after each failure:
  $$\text{Wait} = \text{base} \times 2^{\text{attempt}}$$
- **Full Jitter (AWS Best Practice):** Randomizes the delay to spread retry attempts evenly across time:
  $$\text{Sleep} = \text{random}(0, \text{Wait})$$

---

### Q66: What is the difference between Connection Timeout and Socket/Read Timeout?

**Answer:**

- **Connection Timeout:** The maximum time the client will wait to establish the initial TCP 3-way handshake with the server (typically set short: 1 to 3 seconds).
- **Socket/Read Timeout:** The maximum time the client will wait for data packets to arrive *after* the connection has been established. If the server is stuck in an infinite loop or hanging query, the read timeout breaks the connection (typically 5 to 30 seconds).

---

### Q67: Explain Rate Limiting Algorithms: Token Bucket vs Leaky Bucket vs Sliding Window Counter

**Answer:**

1. **Token Bucket:** Tokens are added to a bucket at a constant refill rate up to bucket capacity. Each request consumes one token.
   - *Advantage:* Allows bursts of traffic up to bucket capacity, while enforcing long-term rate limits. (Used by AWS and Stripe).
2. **Leaky Bucket:** Requests enter a bucket and leak out at a constant, fixed processing rate (FIFO queue).
   - *Advantage:* Perfectly smooths out traffic; eliminates bursts.
3. **Sliding Window Counter:** Divides time into small discrete windows and computes a weighted sum of requests between the previous and current window.
   - *Advantage:* Prevents the boundary burst vulnerability of Fixed Window limiters with minimal memory overhead.

---

### Q68: How do you implement a Distributed Rate Limiter using Redis and Lua?

**Answer:**
Because rate limiting requires checking and incrementing counters across multiple application server instances, the check-and-set operation must be **atomic**.
Executing a **Redis Lua script** runs with single-threaded atomicity:

```lua
-- Atomic sliding window rate limiter:
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = tonumber(redis.call('get', key) or "0")

if current + 1 > limit then
    return 0 -- Rejected
else
    redis.call('incrby', key, 1)
    if current == 0 then
        redis.call('expire', key, tonumber(ARGV[2]))
    end
    return 1 -- Allowed
end
```

---

### Q69: What is Envelope Encryption in Secrets Management (HashiCorp Vault / AWS KMS)?

**Answer:**

- Encrypting large datasets directly with a Master Key is slow and insecure.
- **Envelope Encryption:**
  1. Generate a plaintext **Data Encryption Key (DEK)** locally.
  2. Encrypt the data using the DEK (AES-256-GCM).
  3. Send the DEK to the Key Management Service (KMS), which encrypts the DEK with a **Key Encryption Key (KEK / Master Key)** that never leaves the hardware security module (HSM).
  4. Store the encrypted DEK alongside the ciphertext.
  5. Discard the plaintext DEK from memory.

---

### Q70: What is the Backend-For-Frontend (BFF) Pattern?

**Answer:**

- Instead of having a single monolithic API Gateway serving all client platforms, create **specialized API gateways tailored to specific frontend user interfaces**:
  - `Mobile BFF` (optimized for small screens, low bandwidth, aggregated payloads).
  - `Web Desktop BFF` (richer data schemas, larger payloads).
  - `Third-Party Public BFF` (strict rate limiting and OAuth scopes).
- Decouples frontend development teams and prevents one client platform's needs from polluting universal API contracts.

---

### Q71: What is the Strangler Fig Pattern?

**Answer:**

- A pattern for incrementally migrating a monolithic legacy application to microservices without a risky "big bang" rewrite.
- An API Gateway / Reverse Proxy is placed in front of the legacy monolith.
- As new microservices are built to replace specific domains (e.g., Auth, Inventory), the proxy routes those specific URL paths to the new services while all other traffic continues to the legacy monolith.
- Over time, the legacy monolith is completely "strangled" and decommissioned.

---

### Q72: Compare Deployment Strategies: Blue-Green vs Canary vs Rolling

**Answer:**

- **Blue-Green Deployment:**
  Two identical production environments exist: Blue (active live traffic) and Green (idle). Deploy new version to Green, run smoke tests, and switch router/load balancer traffic from Blue to Green instantly.
  - *Rollback:* Instant (switch router back to Blue).
  - *Cost:* 100% extra infrastructure overhead.
- **Canary Deployment:**
  Route a small percentage of real user traffic (e.g. 5%) to the new version. Monitor telemetry, error rates, and latency for 1 hour. If healthy, gradually ramp up traffic (25% $\to$ 50% $\to$ 100%).
- **Rolling Deployment:**
  Gradually updates pods or instances one by one behind the load balancer until all nodes run the new version. Zero additional infrastructure cost, but multiple versions run concurrently during rollout.

---

### Q73: What are Feature Flags and how do they enable Trunk-Based Development?

**Answer:**

- **Feature Flags (Feature Toggles):** Conditional statements in code that enable or disable features dynamically at runtime based on configuration queried from Redis, LaunchDarkly, or Unleash.
- **Benefits:**
  1. Decouples code deployment from feature release (code is deployed dark/dormant).
  2. Instant kill-switch in production without needing a code redeploy or rollbacks.
  3. Enables A/B testing and targeted canary beta testing by user ID or geography.

---

### Q74: What is the difference between SLI, SLO, and SLA in SRE?

**Answer:**

- **SLI (Service Level Indicator):** A quantifiable metric of service performance observed in real-time (e.g., "P99 latency of `/checkout` is 45ms" or "Error rate is 0.02%").
- **SLO (Service Level Objective):** A target reliability goal set by engineering and product teams (e.g., "99.9% of `/checkout` requests must respond in < 100ms over a 30-day rolling window").
- **SLA (Service Level Agreement):** A legally binding business contract with external customers defining penalties, refunds, or service credits if the service fails to meet agreed thresholds (e.g., "If availability drops below 99.5%, customer receives a 20% billing credit").

---

### Q75: What is an Error Budget?

**Answer:**
$$\text{Error Budget} = 100\% - \text{SLO}$$

- For a 99.9% SLO, the Error Budget is **0.1% of allowable failures or downtime**.
- **The SRE Balance:**
  - If the Error Budget is intact: Product teams are encouraged to ship fast, innovate, and deploy features aggressively.
  - If the Error Budget is exhausted: Feature releases are frozen, and engineering effort is redirected 100% toward stability, bug fixes, and infrastructure hardening.

---

### Q76: What is mTLS (Mutual TLS) and why is it used in Service Meshes?

**Answer:**

- Standard TLS only authenticates the server to the client.
- **mTLS (Mutual TLS):** Both the client and the server authenticate each other using X.509 digital certificates.
- In Service Meshes (Istio, Linkerd), sidecar Envoy proxies handle mTLS transparently between microservices, enforcing Zero-Trust network security and automatic wire encryption across cluster nodes.

---

### Q77: What is Deserialization Vulnerability and how do attackers exploit it?

**Answer:**

- **Insecure Deserialization:** Occurs when an application accepts serialized objects (Java serialization, Python `pickle`, PHP serialize) from untrusted user input without validation.
- Attackers craft serialized payloads with malicious gadget chains that execute arbitrary code (RCE) on the server when the object is reconstituted in memory.
- **Defense:** Never deserialize untrusted inputs using native runtime serializers; use strict schema-validated data formats like JSON, Protocol Buffers, or Avro.

---

### Q78: What is DNS Anycast and GeoDNS?

**Answer:**

- **GeoDNS:** Resolves domain names to different server IP addresses based on the geographic location of the client's DNS resolver.
- **BGP Anycast:** Multiple geographically separated server locations announce the **exact same IP address** via Border Gateway Protocol (BGP). Routers automatically send the user's traffic to the topologically closest server, minimizing latency and providing native DDoS resilience.

---

### Q79: What is Content Delivery Network (CDN) Cache Invalidation?

**Answer:**

- CDNs cache static assets and dynamic API responses at edge Point of Presence (PoP) locations close to users.
- **Invalidation Techniques:**
  1. **Purge by URL / Tag:** Explicit API call to CDN to invalidate cached objects.
  2. **Cache-Busting (Fingerprinting):** Appending a cryptographic content hash to the asset file name (`bundle.a89f7b.js`). Allows setting `Cache-Control: public, max-age=31536000, immutable`, eliminating invalidation needs completely.

---

### Q80: What is Distributed Rate Limiting via Leaky Bucket with Redis?

**Answer:**
Instead of a simple counter, the Leaky Bucket algorithm models traffic as a bucket with a hole:

- Requests fill the bucket.
- A background process or lazy computation drains the bucket at a constant rate based on elapsed time:
  $$\text{CurrentWater} = \max(0, \text{PreviousWater} - \text{LeakRate} \times \Delta t)$$
- If $\text{CurrentWater} + \text{Cost} \le \text{Capacity}$, allow the request; otherwise, drop or reject with HTTP 429.
