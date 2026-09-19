# ☕ 09 - Core Java 21 & Spring Boot 3 Architecture

> Deep-dive engineering reference for Java 21: Virtual Threads (Project Loom), JVM Generational ZGC, ConcurrentHashMap internals, and Spring Boot 3 enterprise microservices.

---

## 🗂️ Module Contents & Learning Path

### 1. Spring Boot 3 Framework
* [**`01_springboot_architecture_and_jvm.md`**](./01_springboot_architecture_and_jvm.md)
  - Spring Boot IoC Container, Bean lifecycle, auto-configuration, and JVM memory layout.
* [**`02_springboot_security_jwt_oauth2.md`**](./02_springboot_security_jwt_oauth2.md)
  - Spring Security 6 `SecurityFilterChain`, stateless sessions, JWT filter chain, and `@PreAuthorize`.
* [**`03_springboot_microservices_and_resilience4j.md`**](./03_springboot_microservices_and_resilience4j.md)
  - Resilience4j Circuit Breakers (Closed, Open, Half-Open), Retry policies, and OpenTelemetry tracing.

### 2. Core Java 21 Internals
* [**`04_java21_virtual_threads_and_structured_concurrency.md`**](./04_java21_virtual_threads_and_structured_concurrency.md)
  - Virtual Threads (Project Loom) vs Platform OS Threads, carrier threads, unmounting during blocking I/O, and `StructuredTaskScope`.
* [**`05_jvm_garbage_collectors_zgc_g1_tuning.md`**](./05_jvm_garbage_collectors_zgc_g1_tuning.md)
  - JVM Heap memory regions, G1 GC tuning, and Java 21 Generational ZGC with $< 1	ext{ms}$ concurrent pauses.
* [**`06_concurrenthashmap_and_thread_safe_collections.md`**](./06_concurrenthashmap_and_thread_safe_collections.md)
  - `HashMap` bucket treeification (Red-Black Tree threshold 8), `ConcurrentHashMap` fine-grained CAS and bucket locking.

### 3. Senior Interview Suite
* [**`interview-questions/top_java_springboot_interview_questions.md`**](./interview-questions/top_java_springboot_interview_questions.md)
  - Top technical interview questions on Virtual Threads, Bean scopes, `@Transactional` proxy pitfalls, and Spring Boot 3 enhancements.
