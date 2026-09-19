# Cognizant (CTS) Senior Developer / Architect Interview Guide

> A comprehensive technical preparation guide for Senior Associate, Manager, and Enterprise Solutions Architect interviews at Cognizant Technology Solutions.

---

## 🏢 1. Cognizant Technical Evaluation Process

Cognizant evaluates experienced engineering talent across **Technical Depth, System Resilience, and Enterprise Delivery Governance**:

1. **Round 1 (Hands-On Technical Architecture)**: Microservices patterns, database query plans, concurrency, REST vs Event-Driven paradigms.
2. **Round 2 (System Design & Cloud Security)**: Distributed transactions (Saga), OAuth 2.0 / OIDC security flows, Kafka partitioning, and Kubernetes deployment architectures.
3. **Round 3 (Client Leadership & Project Governance)**: Handling scope creep, technical risk mitigation, cross-cultural client communication, and mentoring junior engineers.

---

## 🎯 2. High-Yield Technical Concepts & Spoken Answer Scripts

### Question 1: How do you handle Distributed Transactions across Microservices? Compare the Saga Pattern with Two-Phase Commit (2PC)
>
> **The Problem**: In a distributed microservices architecture, a single business transaction (e.g., placing an e-commerce order) spans multiple independent services: `OrderService`, `PaymentService`, and `InventoryService`. Each service has its own private database. How do you maintain data consistency without centralized locking?

**The Spoken Pitch (Say Exactly This):**
> *"In modern distributed systems, Two-Phase Commit (2PC) is considered an anti-pattern for high-scale microservices. 2PC uses a centralized coordinator to execute `Prepare` and `Commit` phases across databases; this locks resources across the network, creates severe latency bottlenecks, and introduces a single point of failure (if the coordinator crashes mid-commit, databases hang in locked limbo).
>
> Instead, we implement the **Saga Pattern**, which breaks a distributed transaction into a series of localized ACID transactions. Each local transaction updates its own database and emits an event or message to trigger the next step.
> Crucially, every step must have an accompanying **Compensating Transaction** that semantically rolls back changes if a subsequent step fails.
>
> We choose between two coordination styles:
>
> 1. **Choreography**: Decentralized. Services listen to Kafka events directly (`OrderCreated` $\to$ Payment listens $\to$ emits `PaymentApproved` $\to$ Inventory listens). Best for simple 2–3 step workflows with few services.
> 2. **Orchestration**: Centralized coordinator (e.g. Temporal, AWS Step Functions, or a dedicated Saga orchestrator). A single orchestrator sends commands to services and tracks state. Best for complex enterprise workflows with branching logic and clear audit requirements."*

---

### Question 2: Explain the OAuth 2.0 Authorization Code Grant with PKCE Flow
>
> **Interviewer:** *"How do you secure modern Single Page Applications (React/Angular) and mobile apps communicating with backend REST APIs?"*

- **Why Implicit Grant is Deprecated**: The legacy Implicit Flow returned access tokens directly in the URL fragment hash, exposing tokens to browser history leakage and malicious browser extensions.
- **Authorization Code Flow with PKCE (Proof Key for Code Exchange)**:
  1. **Code Verifier & Challenge**: The client generates a high-entropy cryptographic random string (`code_verifier`) and computes its SHA-256 hash (`code_challenge`).
  2. **Authorization Request**: The browser redirects to the Identity Provider (Auth0, Okta, Keycloak):
     `GET /authorize?response_type=code&client_id=app&code_challenge=...&code_challenge_method=S256`
  3. **User Authentication**: User logs in and consents. IdP redirects back to the SPA with a short-lived one-time `authorization_code`.
  4. **Token Exchange**: The SPA makes a backend POST request to the IdP, sending the code AND the plain `code_verifier`:
     `POST /token (code + code_verifier)`
  5. **Verification**: The IdP hashes the `code_verifier` and verifies that it matches the original `code_challenge`. Once verified, it issues the short-lived JWT Access Token and Refresh Token.
  6. This mathematically prevents authorization code interception attacks even on public untrusted clients.

---

### Question 3: What is the difference between an Index Seek and an Index Scan in SQL?

- **Index Seek**:
  - The database engine traverses the B-Tree index from root to leaf node using binary search based on search predicates (`WHERE user_id = 4921`).
  - Extremely fast ($O(\log N)$ page accesses). Retrieves only the exact matching data pages.
- **Index Scan**:
  - The database engine scans through every single leaf page of the index sequentially from start to finish ($O(N)$).
  - Occurs when:
    1. The query predicate does not match the leading column of a composite index (`WHERE last_name = 'Smith'` on an index created as `(first_name, last_name)`).
    2. The query applies a function to the column: `WHERE UPPER(email) = 'TEST@TEST.COM'` (prevents B-Tree index traversal unless a functional/expression index exists).
    3. The query uses a leading wildcard: `WHERE name LIKE '%tech'`.
- *Performance Goal*: Always design covering composite indexes to convert Index Scans into Index Seeks.

---

### Question 4: How do you design Microservices for Fault Tolerance using Resilience4j / Polly?

- **Circuit Breaker**: Trips open when downstream failure rate exceeds a threshold (e.g. 50%), returning a cached fallback immediately to prevent thread exhaustion.
- **Bulkhead Pattern**: Isolates connection pools and thread executors by client or service so that slow responses from Service A cannot starve threads needed to serve Service B.
- **Rate Limiting**: Enforces Token Bucket algorithm to protect backend services from denial-of-service traffic spikes.
- **Retry with Exponential Backoff + Jitter**: Re-attempts transient 503/429 errors while adding random jitter to prevent thundering herd spikes.

---

## 💼 3. STAR Technical Case Study: Multi-Tier Retail Platform Modernization

- **Situation**: A major North American retailer's monolithic e-commerce application crashed for 6 hours during a flash Thanksgiving promotion, resulting in \$4.5M in lost sales. Cognizant was brought in to stabilize the architecture.
- **Task**: Serve as Technical Lead to eliminate single points of failure and modernize the order processing and inventory pipeline to handle 15,000 orders/minute.
- **Action**:
  1. Decomposed the monolithic checkout into autonomous Spring Boot microservices deployed on Azure Kubernetes Service (AKS).
  2. Implemented the **Saga Orchestrator Pattern** using Azure Service Bus to coordinate payment, inventory deduction, and shipping notification.
  3. Replaced synchronous inventory table locking with a Redis Distributed Lock and Lua scripts, reducing lock contention latency by 94%.
  4. Added Resilience4j circuit breakers and connection pool bulkheads on all third-party payment gateways.
- **Result**: The modernized platform supported the subsequent Black Friday sale with **100% uptime at 18,200 orders/minute**, P95 checkout latency dropped from **4,200ms to 120ms**, and the solution was recognized as an internal Cognizant Enterprise Excellence benchmark.
