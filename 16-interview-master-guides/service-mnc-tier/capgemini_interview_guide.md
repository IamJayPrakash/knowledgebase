# Capgemini Senior Technical Consultant / Lead Architect Interview Guide

> A definitive, high-yield preparation guide tailored for Senior Developer, Technical Lead, and Enterprise Solutions Consultant roles at Capgemini.

---

## 🏢 1. Capgemini Interview Process & Evaluation Rubric

Capgemini's technical assessment for Senior / Lead grades (Consultant, Senior Consultant, Manager) focuses heavily on **Enterprise Reliability, Cloud-Native Architecture, and Client Consulting**:

1. **Round 1 (Core Technical & Code Quality)**: Deep dive into Java 17/21 or Full-Stack Node/React, SOLID principles, Concurrency, and Design Patterns.
2. **Round 2 (Enterprise Microservices & Cloud Architecture)**: Spring Boot 3 / Microservices, Kafka event-driven pipelines, AWS/Azure cloud infrastructure, and Database tuning.
3. **Round 3 (Managerial & Client Consulting)**: Technical governance, Agile estimation, handling difficult enterprise stakeholders, and incident management.

---

## 🎯 2. High-Frequency Technical Concepts & Spoken Answer Scripts

### Question 1: How do you design and enforce Idempotency in Enterprise REST APIs?
> **The Problem**: A client makes a payment request (`POST /api/v1/payments`). The request succeeds on the backend, but a network blip prevents the response from reaching the mobile client. The client's retry logic fires a second request, potentially charging the customer twice.

**The Spoken Pitch (Say Exactly This):**
> *"In enterprise microservices, we enforce idempotency on state-modifying requests (POST/PATCH) using the **Idempotency-Key Pattern**:
> 1. The client generates a unique UUID `Idempotency-Key` and attaches it as an HTTP header: `Idempotency-Key: 7b9e1e24-4f2a-...`.
> 2. When the API Gateway receives the request, it executes an atomic `SET key status:IN_PROGRESS NX EX 120` in Redis.
> 3. If Redis returns `0` (key already exists), the gateway knows a duplicate request is underway. It immediately returns `HTTP 409 Conflict` or waits for the cached response.
> 4. Once the downstream payment processor completes the transaction, the backend updates the Redis key with the final JSON response payload and a 24-hour TTL: `SET key {"status":"COMPLETED", "txId":"tx_102"} EX 86400`.
> 5. Any subsequent retries with the same idempotency key return the cached completed JSON response with `HTTP 200 OK` without touching the payment processor, mathematically guaranteeing that payments are executed exactly once."*

---

### Question 2: Explain SOLID Principles with Concrete Enterprise Architecture Examples
> **Interviewer:** *"Walk me through the SOLID principles and how you enforce them in code reviews."*

- **S - Single Responsibility Principle (SRP)**:
  - *Violation*: An `OrderService` that validates shopping carts, calculates taxes, updates inventory, generates PDF invoices, and sends emails.
  - *Fix*: Decouple into `OrderValidationService`, `TaxCalculationService`, `InvoiceGenerator`, and an asynchronous event emitter for notifications.
- **O - Open/Closed Principle (OCP)**:
  - Software entities should be open for extension, but closed for modification.
  - *Enterprise Example*: Implementing payment gateways. Use a `PaymentProcessor` interface. Adding a new gateway (e.g. Apple Pay) involves adding a new class `ApplePayProcessor implements PaymentProcessor` without modifying existing `StripeProcessor` or `PayPalProcessor` code.
- **L - Liskov Substitution Principle (LSP)**:
  - Derived classes must be substitutable for their base classes without breaking correctness.
  - *Classic Pitfall*: Subclassing `ReadOnlyRepository` from `WritableRepository` and throwing `UnsupportedOperationException` in `save()` violates LSP.
- **I - Interface Segregation Principle (ISP)**:
  - Clients should not be forced to depend on interfaces they do not use. Prefer small, role-specific interfaces (`Readable`, `Closeable`, `Serializable`) over "fat" god-interfaces.
- **D - Dependency Inversion Principle (DIP)**:
  - High-level modules should not depend on low-level modules; both should depend on abstractions.
  - *Enterprise Example*: Controllers depend on an interface `UserRepository`, not on a concrete `PostgreSqlUserRepository` or MongoDB client, enabling seamless database migrations and mock unit testing.

---

### Question 3: How does JVM Memory Management differ between G1 GC and Generational ZGC?
- **G1 GC (Garbage-First)**:
  - Divides heap into 2,048 equal-sized regions.
  - Targets user-configured pause times (e.g., `-XX:MaxGCPauseMillis=200`).
  - Compacts the most fragmented ("garbage-first") regions first. Pause times scale with heap size and can reach 50–200ms on 32GB+ heaps.
- **Generational ZGC (Java 21)**:
  - Scalable low-latency garbage collector engineered for heaps from megabytes to 16 Terabytes.
  - Performs almost all heavy GC phases (marking, relocation, reference processing) **concurrently with application threads**.
  - Guarantees max pause times of **less than 1 millisecond**, regardless of heap size.
  - *Production Recommendation*: For high-throughput low-latency microservices on Java 21, use `-XX:+UseZGC -XX:+ZGenerational`.

---

### Question 4: How do you design an Event-Driven Architecture with Apache Kafka to guarantee Exactly-Once Processing?
1. **Producer Side**:
   - Enable `enable.idempotence=true`. The Kafka broker assigns a Producer ID (PID) and tracks sequence numbers per partition, transparently de-duplicating retry network packets.
   - Use Kafka Transactions (`beginTransaction()`, `commitTransaction()`) for atomic multi-partition writes.
2. **Broker Side**:
   - Set `acks=all` (ensures all in-sync replicas acknowledge write) and `min.insync.replicas=2`.
3. **Consumer Side**:
   - Consume messages and store processed offsets in the destination database within the *same local ACID database transaction* (the **Transactional Consumer Pattern**), or use deterministic idempotent upserts (`INSERT ... ON CONFLICT DO UPDATE`).

---

## 💼 3. STAR Consulting Case Study: Legacy Monolith Modernization

- **Situation**: A major European banking client engaged Capgemini to modernize a 12-year-old monolithic loan origination system that took 3 days to approve personal loans and suffered recurring 4-hour outages during batch updates.
- **Task**: Lead a team of 8 consultants to re-architect loan processing into a cloud-native microservices architecture on AWS with zero regulatory compliance disruption.
- **Action**:
  1. Decomposed the monolith using Domain-Driven Design (DDD) into 3 bounded contexts: `CustomerKYC`, `CreditScoring`, and `Disbursement`.
  2. Applied the Strangler Fig Pattern using AWS API Gateway to incrementally route 10% of traffic to the new Spring Boot microservices.
  3. Implemented asynchronous event-driven communication via AWS MSK (Managed Kafka) to process credit scoring asynchronously.
  4. Deployed with Spring Boot 3 on Amazon EKS using AWS Graviton instances, backed by Aurora PostgreSQL.
- **Result**: Loan approval turnaround dropped from **3 days to 4 minutes**. System availability rose to **99.99%**, cloud operational infrastructure costs decreased by **42%**, and the client renewed the multimillion-dollar multi-year consulting engagement.
