# ☕ Java 21 & Spring Boot 3 Senior & Lead Master Interview Question Bank (100 Questions)

> Comprehensive, production-grade 100-question interview bank covering everything from core JVM memory layout, garbage collection (ZGC), multithreading, and Project Loom Virtual Threads to enterprise Spring Boot 3, Spring Security 6, and Microservices.

---

## 📑 Curriculum & Question Bank Structure

```
09-backend-java-springboot/interview-questions/
├── 01_java_core_foundations_jvm_and_memory_qna.md         ──► Questions 1 to 20
├── 02_java_oop_collections_generics_and_exceptions_qna.md ──► Questions 21 to 40
├── 03_java_concurrency_threads_and_virtual_threads_qna.md ──► Questions 41 to 60
├── 04_spring_boot_core_ioc_and_data_qna.md                ──► Questions 61 to 80
├── 05_spring_boot_security_microservices_and_resilience_qna.md ──► Questions 81 to 100
└── top_java_springboot_interview_questions.md              ──► Quick Refresher
```

---

## 🎯 Master Question Index (1 - 100)

### Part 1: Core Java Foundations, JVM Architecture & Memory Management (Q1 - Q20)

* [`01_java_core_foundations_jvm_and_memory_qna.md`](./01_java_core_foundations_jvm_and_memory_qna.md)
  1. Internal architecture of the JVM: ClassLoader, Memory, Engine.
  2. JVM Runtime Data Areas (Heap, Stack, Metaspace, PC, Native).
  3. Tiered JIT Compiler (Interpreter vs C1 vs C2 Server compiler).
  4. Escape Analysis and Scalar Replacement on the Stack.
  5. Proving Java is strictly 100% Pass-by-Value.
  6. Four architectural reasons why `String` is immutable.
  7. String Constant Pool (SCP) and `String.intern()`.
  8. `String` vs `StringBuilder` vs `StringBuffer` comparison.
  9. The contract between `equals()` and `hashCode()`.
  10. The Integer Cache mechanism (`[-128, 127]`).
  11. Generational Hypothesis and Young vs Old space.
  12. G1 (Garbage-First) Collector regions and pause targets.
  13. Java 21 Generational ZGC (sub-millisecond pause times).
  14. `final` vs `finally` vs `finalize()` differences.
  15. The 3 extreme scenarios when a `finally` block fails to execute.
  16. The Diamond Problem and Java 8 interface default methods.
  17. Records in Java 17/21 and boilerplate elimination.
  18. Sealed Classes (`sealed ... permits`) and compile-time hierarchy enforcement.
  19. Pattern Matching for `switch` statements in Java 21.
  20. `Comparable` (natural) vs `Comparator` (custom dynamic) ordering.

### Part 2: OOP, Collections Framework, Generics & Streams (Q21 - Q40)

* [`02_java_oop_collections_generics_and_exceptions_qna.md`](./02_java_oop_collections_generics_and_exceptions_qna.md)
  21. Dynamic Method Dispatch and Metaspace vtables.
  22. Abstract Classes vs Interfaces in Java 21.
  23. `ArrayList` internal array structure and $1.5\times$ growth formula.
  24. `HashMap` hashing, collision buckets, and Red-Black tree conversion.
  25. `ConcurrentHashMap` CAS and fine-grained bucket head locking.
  26. Fail-Fast vs Fail-Safe / Weakly Consistent iterators.
  27. Generics Type Erasure under the hood.
  28. The PECS Principle (Producer Extends, Consumer Super).
  29. Java Exception Hierarchy: Checked vs Unchecked exceptions.
  30. `try-with-resources` and `AutoCloseable` interface.
  31. Java Streams: Intermediate (lazy) vs Terminal (eager) operations.
  32. When to avoid Parallel Streams (`.parallelStream()`).
  33. `map()` vs `flatMap()` stream transformations.
  34. `Optional<T>` best practices and anti-patterns.
  35. `IdentityHashMap` reference equality vs `HashMap`.
  36. `WeakHashMap` and garbage collection of keys.
  37. `BlockingQueue` in producer-consumer multithreading.
  38. `EnumMap` ordinal array indexing performance.
  39. `poll()` vs `remove()` vs `peek()` in Queue.
  40. Functional Interfaces and SAM interface rules.

### Part 3: Concurrency, Threading, Memory Model & Virtual Threads (Q41 - Q60)

* [`03_java_concurrency_threads_and_virtual_threads_qna.md`](./03_java_concurrency_threads_and_virtual_threads_qna.md)
  41. Java Thread Lifecycle and 6 Thread States.
  42. `synchronized` monitor locks vs `ReentrantLock` features.
  43. The `volatile` keyword, visibility, and memory barriers.
  44. `AtomicInteger` lock-free operations and hardware CAS.
  45. The ABA Problem and `AtomicStampedReference`.
  46. `CountDownLatch` (single-use) vs `CyclicBarrier` (reusable).
  47. `Semaphore` permit acquisition and rate limiting.
  48. `ThreadPoolExecutor` parameters and CPU/IO sizing formulas.
  49. Four Rejected Execution Policies (`Abort`, `CallerRuns`, `Discard`, `DiscardOldest`).
  50. Deadlock detection via thread dumps (`jstack`) and prevention.
  51. `CompletableFuture` non-blocking async composition.
  52. Java 21 Project Loom: Platform Threads vs Virtual Threads.
  53. Carrier Thread unmounting and continuations.
  54. Thread Pinning in Virtual Threads (`synchronized` vs `ReentrantLock`).
  55. Why Virtual Threads should never be pooled.
  56. Structured Concurrency in Java 21 (`StructuredTaskScope`).
  57. Scoped Values (`ScopedValue<T>`) replacing `ThreadLocal`.
  58. `Thread.sleep()` vs `Object.wait()` lock holding.
  59. `ThreadLocal` memory leaks in pooled application servers.
  60. `LongAdder` cell striping performance under high contention.

### Part 4: Spring Boot Core, IoC Container, AOP & Spring Data JPA (Q61 - Q80)

* [`04_spring_boot_core_ioc_and_data_qna.md`](./04_spring_boot_core_ioc_and_data_qna.md)
  61. Complete Spring Bean Lifecycle phases.
  62. Why Field Injection is an architectural anti-pattern.
  63. Spring Bean Scopes and prototype injection into singletons.
  64. Spring Boot Auto-Configuration and `@ConditionalOn...` evaluation.
  65. Spring AOP Dynamic Proxies (JDK Dynamic vs CGLIB).
  66. Why `@Transactional` self-invocation fails.
  67. `@Transactional` Propagation Types (`REQUIRED`, `REQUIRES_NEW`, `NESTED`).
  68. Default Rollback Rules of `@Transactional` (checked vs unchecked).
  69. Hibernate First-Level Cache vs Second-Level Cache.
  70. Hibernate Dirty Checking and automatic update generation.
  71. Solving the JPA N+1 Query Problem (`@EntityGraph`, `JOIN FETCH`).
  72. `FetchType.LAZY` vs `FetchType.EAGER` performance trade-offs.
  73. `LazyInitializationException` causes and clean resolution.
  74. Optimistic Locking (`@Version`) vs Pessimistic Locking (`FOR UPDATE`).
  75. Spring Data JPA Auditing (`@EnableJpaAuditing`).
  76. `BeanFactory` vs `ApplicationContext` capabilities.
  77. `@Async` and configuring custom `ThreadPoolTaskExecutor`.
  78. `@Controller` vs `@RestController` serialization.
  79. Jackson polymorphic type deserialization (`@JsonTypeInfo`).
  80. Spring Boot Actuator production operational endpoints.

### Part 5: Spring Security 6, Microservices, Resilience4j & Production Ops (Q81 - Q100)

* [`05_spring_boot_security_microservices_and_resilience_qna.md`](./05_spring_boot_security_microservices_and_resilience_qna.md)
  81. Spring Security 6 Filter Chain architecture.
  82. Configuring a modern stateless `SecurityFilterChain`.
  83. Why CSRF protection is disabled in stateless REST APIs.
  84. Method-Level Security with `@PreAuthorize` and SpEL.
  85. Enabling Java 21 Virtual Threads in Spring Boot 3.2+.
  86. Resilience4j Circuit Breaker integration and fallback methods.
  87. Spring Cloud Gateway non-blocking Netty architecture.
  88. Kafka Consumer Idempotency in Spring Boot (`@KafkaListener`).
  89. Distributed Tracing with Micrometer Tracing and OpenTelemetry.
  90. Spring WebFlux (Reactive) vs Spring MVC + Virtual Threads (Java 21).
  91. Graceful Shutdown configuration in Spring Boot.
  92. `SecurityContextHolder` storage strategies.
  93. Securing Actuator endpoints in production.
  94. Centralized external configuration with Spring Cloud Config.
  95. Multi-stage deployment with Spring `@Profile`.
  96. Preventing SQL Injection in Spring Data JPA.
  97. Distributed session management with Spring Session Redis.
  98. `@Mock` (pure unit) vs `@MockBean` (context integration).
  99. Testcontainers vs H2 In-Memory DB for testing.
  100. Tuning Spring Boot applications for extreme production throughput.

---

## ⚡ Quick Refresher

* [`top_java_springboot_interview_questions.md`](./top_java_springboot_interview_questions.md) — High-frequency senior interview question summary.
