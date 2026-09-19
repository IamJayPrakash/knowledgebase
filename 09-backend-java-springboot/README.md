# ☕ 09 - Core Java 21 & Spring Boot 3 Enterprise Master Curriculum

> Complete, structured engineering guide from **Java Newbie Fundamentals to Advanced Java 21 High-Concurrency Internals & Enterprise Spring Boot 3 Architecture**.

---

## 🗺️ Module Contents & Learning Path

### Level 1: 🐣 Core Java Foundations (Newbie ➡️ Experienced)
* [**`01_java_fundamentals_jvm_primitives_and_pass_by_value.md`**](./01_java_fundamentals_jvm_primitives_and_pass_by_value.md)
  - Compilation to bytecode (`javac`), JVM ClassLoader, Bytecode Verifier, Tiered JIT (C1/C2), 8 Primitive types vs Wrapper classes, Integer Cache (`[-128, 127]`), and the proof that Java is strictly Pass-by-Value.
* [**`02_java_strings_memory_string_pool_stringbuilder.md`**](./02_java_strings_memory_string_pool_stringbuilder.md)
  - String immutability rationale, String Constant Pool (SCP) in Heap, `String.intern()`, `StringBuilder` vs `StringBuffer`, the `equals()` & `hashCode()` contract, and Java 9+ Compact Strings (`byte[]`).
* [**`03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md`**](./03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md)
  - The 4 OOP Pillars in Java, Method Overloading (compile-time) vs Overriding (runtime dynamic method dispatch via Metaspace vtable), Abstract Classes vs Interfaces, Java 8/9 default/private interface methods, and `final` mechanics.
* [**`04_java_collections_framework_list_set_queue_map.md`**](./04_java_collections_framework_list_set_queue_map.md)
  - Java Collections Framework (JCF) architecture: `ArrayList` ($1.5\times$ resizing) vs `LinkedList`, `HashSet` vs `TreeSet`, `ArrayDeque` vs `PriorityQueue` (min-heap), `HashMap` bucket treeification (Red-Black Tree after 8 colliding keys), and Fail-Fast vs Fail-Safe iterators.
* [**`05_java_generics_wildcards_and_type_erasure.md`**](./05_java_generics_wildcards_and_type_erasure.md)
  - Type parameters, Bounded type parameters, The PECS Principle (**Producer Extends, Consumer Super**), and Type Erasure under the hood with compiler-generated bridge methods.
* [**`06_java_exception_handling_and_try_with_resources.md`**](./06_java_exception_handling_and_try_with_resources.md)
  - `Throwable` hierarchy (`Error` vs `Exception`), Checked vs Unchecked (`RuntimeException`), `try-catch-finally` flow, Java 7+ `try-with-resources` with `AutoCloseable`, and suppressed exceptions.
* [**`07_java_modern_features_streams_lambdas_records_sealed.md`**](./07_java_modern_features_streams_lambdas_records_sealed.md)
  - Functional Interfaces (`Predicate`, `Function`, `Consumer`, `Supplier`), Stream API lazy pipelines, immutable `record` types, `sealed` classes & interfaces, and Java 21 exhaustive `switch` pattern matching.

### Level 2: 🚀 Advanced Java 21 High-Concurrency Internals
* [**`08_concurrenthashmap_and_thread_safe_collections.md`**](./08_concurrenthashmap_and_thread_safe_collections.md)
  - `ConcurrentHashMap` fine-grained CAS (Compare-And-Swap) for empty buckets and synchronized bucket head locking, `CopyOnWriteArrayList`, and thread-safe queues.
* [**`09_jvm_garbage_collectors_zgc_g1_tuning.md`**](./09_jvm_garbage_collectors_zgc_g1_tuning.md)
  - JVM Heap memory regions (Eden, Survivor, Tenured), Metaspace, G1 GC tuning, and Java 21 Generational ZGC ($< 1\text{ms}$ concurrent pause times).
* [**`10_java21_virtual_threads_and_structured_concurrency.md`**](./10_java21_virtual_threads_and_structured_concurrency.md)
  - Virtual Threads (Project Loom) vs Platform OS Threads, carrier threads ($M:N$ mapping), unmounting during blocking I/O, and `StructuredTaskScope`.

### Level 3: 🏗️ Enterprise Spring Boot 3 Microservices
* [**`11_springboot_architecture_and_jvm.md`**](./11_springboot_architecture_and_jvm.md)
  - Spring Boot IoC Container, Bean lifecycle, auto-configuration, and JVM memory layout.
* [**`12_springboot_security_jwt_oauth2.md`**](./12_springboot_security_jwt_oauth2.md)
  - Spring Security 6 `SecurityFilterChain`, stateless sessions, JWT filter chain, and `@PreAuthorize`.
* [**`13_springboot_microservices_and_resilience4j.md`**](./13_springboot_microservices_and_resilience4j.md)
  - Resilience4j Circuit Breakers (Closed, Open, Half-Open), Retry policies, and OpenTelemetry distributed tracing.

---

## 📂 Senior Interview Suite
* [**`interview-questions/top_java_springboot_interview_questions.md`**](./interview-questions/top_java_springboot_interview_questions.md)
  - Top technical interview questions on Virtual Threads, Bean scopes, `@Transactional` proxy pitfalls, and Spring Boot 3 enhancements.
