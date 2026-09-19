# -*- coding: utf-8 -*-
"""
Generator for Core Java 21 & Spring Boot Deep Dive Expansion
Generates:
1. 09-backend-java-springboot/04_java21_virtual_threads_and_structured_concurrency.md
2. 09-backend-java-springboot/05_jvm_garbage_collectors_zgc_g1_tuning.md
3. 09-backend-java-springboot/06_concurrenthashmap_and_thread_safe_collections.md
4. 09-backend-java-springboot/interview-questions/top_java_springboot_interview_questions.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "09-backend-java-springboot", "04_java21_virtual_threads_and_structured_concurrency.md"): """# Java 21 Virtual Threads (Project Loom) & Structured Concurrency

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purane Java mein **Platform Thread (OS Thread)** ek **Badi Luxury Bus** ki tarah hota tha: Bus bohot bhari hoti hai, har bus chalane ke liye 1 MB memory chahiye hoti hai, aur ek city mein 2,000 se zyada bus chalte hi traffic jam ho jata tha (**Thread Exhaustion**). Agar passenger ko bank counter par 5 second wait karna hai, toh poori 1 MB ki bus wahi khadi rehti thi!
Java 21 ke **Virtual Threads (Project Loom)** ek **Lightweight E-Scooter / Metro Ticket** ki tarah hain: E-scooter sirf kuch bytes (1 KB) ki RAM leta hai! Aap ek hi laptop par **10 Lakh (1,000,000) Virtual Threads** chala sakte ho! Jaise hi koi thread database ya network I/O ka wait karta hai, JVM use chupke se side mein park kar deta hai (**Unmount from Carrier Thread**) aur doosre thread ko processor pakda deta hai!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Platform Threads vs Virtual Threads**:
   - **Platform Thread**: 1-to-1 wrapper around an operating system thread. Heavyweight ($\sim 1 \text{ MB}$ stack allocated in OS virtual memory). Max $\sim 5,000$ concurrent threads per JVM.
   - **Virtual Thread**: $M$-to-$N$ user-mode thread managed directly by the JVM runtime. Ultra-lightweight ($\sim 1 \text{ KB}$ initial stack in JVM heap). Millions can run concurrently.
2. **Continuation & Carrier Threads**:
   - Virtual threads run on top of standard platform threads called **Carrier Threads** (backed by a `ForkJoinPool`).
   - When a virtual thread encounters blocking I/O (e.g. `Socket.read()`, `Thread.sleep()`), the JVM **unmounts** the virtual thread from the carrier thread and saves its call stack to the heap. The carrier thread immediately executes another virtual thread!
3. **The Thread Pinning Gotcha (`synchronized`)**:
   - In early Loom builds, blocking inside a `synchronized` block or native JNI call "pinned" the virtual thread to its carrier thread, preventing unmounting.
   - **Remedy**: Replace `synchronized` blocks with `java.util.concurrent.locks.ReentrantLock`.
4. **No More Thread Pools for Virtual Threads**:
   - Never pool virtual threads (`Executors.newFixedThreadPool(100)` is an anti-pattern for virtual threads!).
   - Virtual threads are cheap and disposable: create a new one per task via `Executors.newVirtualThreadPerTaskExecutor()`.
5. **Structured Concurrency**:
   - Treats multiple concurrent subtasks running in different threads as a single unit of work (`StructuredTaskScope`), preventing thread leaks and orphan zombie tasks.

---

## 📊 3. Visual Architecture Diagram

```
                 JAVA 21 VIRTUAL THREAD ARCHITECTURE
                 
   [ 1,000,000 Virtual Threads ] ◄── Lightweight (~1 KB Heap Stack)
          │         │         │
          ▼         ▼         ▼ (JVM Scheduler M:N Mapping)
   ┌───────────────────────────────────────────────┐
   │ ForkJoinPool Carrier Threads (Platform)       │
   │ [ Carrier 1 ]   [ Carrier 2 ]   [ Carrier 3 ] │ ◄── Exactly equals CPU Cores
   └───────────────────────┬───────────────────────┘
                           ▼
             [ Operating System OS Threads ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```java
package com.knowledgebase.threads;

import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.concurrent.StructuredTaskScope;
import java.util.stream.IntStream;

public class VirtualThreadDemo {

    // Line 11: Benchmark: Launching 100,000 Concurrent Virtual Threads
    public static void runMillionVirtualThreads() {
        System.out.println("Starting 100,000 Virtual Threads...");
        long start = System.currentTimeMillis();

        // Line 16: Executor that spawns a fresh virtual thread for every submitted task
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, 100_000).forEach(i -> {
                executor.submit(() -> {
                    // Line 20: Non-blocking sleep: JVM unmounts thread from carrier!
                    Thread.sleep(Duration.ofMillis(1000));
                    return i;
                });
            });
        } // Auto-close waits for all submitted tasks to complete!

        long elapsed = System.currentTimeMillis() - start;
        System.out.println("Finished 100,000 threads in: " + elapsed + " ms");
    }

    // Line 31: Structured Concurrency with StructuredTaskScope (Java 21 Preview)
    public record UserDashboard(String userProfile, String orderHistory) {}

    public static UserDashboard fetchUserDashboardStructured(String userId) throws Exception {
        // Line 35: Structured scope that fails fast if ANY subtask throws an exception
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            
            // Line 38: Fork Subtask 1 (Fetch Profile) on a virtual thread
            StructuredTaskScope.Subtask<String> profileTask = scope.fork(() -> {
                Thread.sleep(200); // Simulate remote REST call
                return "Profile[User=" + userId + ", Tier=Gold]";
            });

            // Line 44: Fork Subtask 2 (Fetch Orders) concurrently on another virtual thread
            StructuredTaskScope.Subtask<String> ordersTask = scope.fork(() -> {
                Thread.sleep(350); // Simulate DB query
                return "Orders[Count=14, Total=$2450]";
            });

            // Line 50: Wait for both forks to complete or fail
            scope.join();
            // Line 52: Propagate exception if either subtask failed
            scope.throwIfFailed();

            // Line 55: Return aggregated result safely
            return new UserDashboard(profileTask.get(), ordersTask.get());
        }
    }
}
```

---

## 🎯 5. The "Interview Pitch"
> "Java 21 Virtual Threads revolutionize backend scalability by decoupling application concurrency from operating system thread limits. Historically, high-throughput microservices had to choose between synchronous thread-per-request architectures—which cap concurrency around a few thousand connections due to the 1MB platform thread stack overhead—or complex, unreadable reactive frameworks like WebFlux/Project Reactor. Virtual Threads deliver the best of both worlds: you write intuitive, readable, sequential synchronous code with standard `try-catch` blocks, while the JVM unmounts virtual threads from carrier threads during blocking socket I/O. This enables a single Spring Boot 3 service on Java 21 to sustain over 50,000 concurrent blocking I/O requests with minimal CPU and memory overhead."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a high-traffic fintech transaction hub running Spring Boot 2 on Java 11, concurrent user traffic during festival promotions peaked at 12,000 concurrent HTTP checkout sessions. The Tomcat thread pool (configured to 500 max threads) saturated immediately, driving request latency from 45ms to 18 seconds and returning `HTTP 503 Service Unavailable`.
- **Task**: Increase concurrent throughput by at least 10x without rewriting 80,000 lines of existing blocking JPA/JDBC business code to reactive WebFlux.
- **Action**: We upgraded the microservice to Java 21 and Spring Boot 3.2. We enabled virtual threads with a single configuration flag: `spring.threads.virtual.enabled=true`. We audited our codebase to replace legacy `synchronized` lock utilities with `ReentrantLock` to prevent thread pinning during PostgreSQL queries, and removed old fixed thread pools.
- **Result**: Supported 25,000 concurrent active checkout sessions with zero 503 errors. Average P99 latency plummeted from 18,000ms to 65ms, memory consumption dropped by 45%, and the entire upgrade was achieved without changing a single line of business logic.
""",

    os.path.join(BASE_DIR, "09-backend-java-springboot", "05_jvm_garbage_collectors_zgc_g1_tuning.md"): """# JVM Memory Architecture & Modern Garbage Collectors: G1 vs ZGC

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
JVM Memory ek **Multi-Floor Building** ki tarah hai:
1. **Young Generation (Eden Space)**: Day-to-day office desk. Har nayi file (Object) desk par banti hai. Zyadatar files 5 minute mein kachra ban jati hain (Short-lived objects).
2. **Old / Tenured Generation**: Basement Archive Room. Jo files saalon tak zinda rehti hain (Singletons, Caches), unhe basement mein permanently shift kar diya jata hai.
**Garbage Collector (Safai Wala)**:
- **G1 GC**: Room ko chote chote square blocks mein baant kar safai karta hai, lekin beech-beech mein thodi der ke liye office ka gate band kar deta hai (**Stop-The-World Pause**).
- **ZGC (Z Garbage Collector)**: Ek **Invisible Stealth Robot** hai jo tab bhi safai karta rehta hai jab office mein log kaam kar rahe hote hain! Pauses are guaranteed to be **under 1 millisecond** chahe aapka heap 16 GB ka ho ya 16 Terabytes ka!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **JVM Memory Regions**:
   - **Heap Memory**: Shared across all threads. Divided into Eden, Survivor 1/2, and Old (Tenured) Generation.
   - **Metaspace**: Stores loaded class metadata in native OS memory (replaces PermGen since Java 8).
   - **Thread Stack**: Private to each thread. Stores method call frames, local primitives, and object references.
2. **G1 GC (Garbage-First)**:
   - Divides heap into equal-sized regions ($\sim 1 \text{ MB} - 32 \text{ MB}$).
   - Tracks which regions contain the most garbage and collects those first ("Garbage-First").
   - Configurable target pause time: `-XX:MaxGCPauseMillis=200`.
3. **Generational ZGC (Java 21 Gold Standard)**:
   - Colored Pointers & Load Barriers: Encodes GC metadata directly into the top bits of reference pointers.
   - Executes Mark, Relocate, and Compact phases **concurrently** with application threads.
   - Pause times are consistently **$< 1 \text{ ms}$**, eliminating GC-induced latency spikes in trading and low-latency systems.

---

## 📊 3. Visual Architecture Diagram

```
                       JVM RUNTIME MEMORY REGIONS
                       
  ┌───────────────────────────────────────────────────────────────┐
  │                        HEAP MEMORY                            │
  │  ┌─────────────────────────┐     ┌─────────────────────────┐  │
  │  │    YOUNG GENERATION     │     │     OLD GENERATION      │  │
  │  │  [Eden] [S0] [S1]       │ ──► │  (Tenured Long-Lived)   │  │
  │  └─────────────────────────┘     └─────────────────────────┘  │
  └───────────────────────────────────────────────────────────────┘
  ┌─────────────────────────────┐   ┌─────────────────────────────┐
  │          METASPACE          │   │      JVM THREAD STACKS      │
  │ (Native OS Off-Heap Memory) │   │ (Thread-Local Stack Frames) │
  └─────────────────────────────┘   └─────────────────────────────┘
```

---

## 💻 4. Line-by-Line Commented Code Snippets & Production Flags

```bash
# Line 1: Modern Production JVM Configuration for Low-Latency Spring Boot (Java 21)
java \
  -XX:+UseZGC \                               # Enable modern Z Garbage Collector
  -XX:+ZGenerational \                        # Enable Generational ZGC in Java 21 (Huge throughput boost!)
  -Xms8g -Xmx8g \                             # Fix initial and maximum heap size to prevent resizing pauses
  -XX:+AlwaysPreTouch \                       # Pre-fault all heap pages into physical RAM at startup
  -XX:+UseNUMA \                              # Enable Non-Uniform Memory Access optimization for multi-socket CPUs
  -Xlog:gc*,gc+phases=debug:file=/var/log/app/gc.log:time,uptime,pid:filecount=5,filesize=100M \ # Structured GC logs
  -jar payment-service.jar
```

```java
package com.knowledgebase.jvm;

public class MemoryLeakAntiPattern {

    // ANTI-PATTERN: Unbounded static collection retaining heap references
    // private static final List<byte[]> leakedBuffers = new ArrayList<>();

    // GOLD STANDARD: Using WeakReference or Bounded Caffeine Cache
    public static void safeCachingPattern() {
        System.out.println("Allocating short-lived objects in Eden Space...");
        for (int i = 0; i < 1000; i++) {
            // Allocated in Eden space; collected during rapid Minor GC with near-zero overhead
            String temp = "request_id_" + i;
        }
    }
}
```

---

## 🎯 5. The "Interview Pitch"
> "JVM memory is partitioned into the Heap for dynamic object allocation, Metaspace in native memory for class definitions, and Thread Stacks for execution frames. For garbage collection, while G1 GC has long been the enterprise standard balancing throughput with configurable pause targets like 200ms, Java 21 stabilizes Generational ZGC. Generational ZGC separates young and old objects while leveraging colored pointers and concurrent load barriers. It performs marking, evacuation, and compaction concurrently with worker threads, guaranteeing maximum pause times under 1 millisecond regardless of whether the heap is 4GB or 1TB. For SLA-sensitive low-latency systems, Generational ZGC is the undisputed standard."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A real-time payments settlement microservice with a 12 GB heap running on G1 GC suffered intermittent 1,200ms Stop-The-World (STW) pauses during high-frequency settlement sweeps. Upstream payment aggregator gateways interpreted these pauses as connection timeouts, triggering erroneous duplicate transfer retries.
- **Task**: Eliminate GC pause spikes above 100ms and reduce transaction failure rates to zero.
- **Action**: We captured GC telemetry using `-Xlog:gc*` and identified that humongous object allocations during batch reporting triggered G1 full concurrent evacuation failures. We tuned JVM flags by switching to Java 21 Generational ZGC (`-XX:+UseZGC -XX:+ZGenerational`), pinned heap size with `-Xms12g -Xmx12g`, and added `-XX:+AlwaysPreTouch`.
- **Result**: Max GC pause time collapsed from 1,200ms to an imperceptible 0.45ms (a 99.96% latency reduction). P99.9 API response times stabilized at 12ms, and zero timeout-induced transaction duplicates occurred.
""",

    os.path.join(BASE_DIR, "09-backend-java-springboot", "06_concurrenthashmap_and_thread_safe_collections.md"): """# Java Collections Deep Dive: HashMap vs ConcurrentHashMap Internals

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Plain HashMap** ek bina security guard wali dukan jaisa hai: Agar ek customer saman utha raha hai aur doosra customer usi shelf par naya saman thos raha hai, toh pura shelf toot kar bikhar sakta hai (**Infinite Loop / Data Corruption in Multithreading**).
**`Hashtable` (Purana Java 1.0)** dukan ke bahar **Bada Lohe Ka Phatak** laga deta hai: Ek baar mein sirf ek hi customer dukan ke andar ja sakta hai, chahe dukan mein 100 aisle khali hon! (Extreme lock contention).
**`ConcurrentHashMap`** ek **Smart Supermarket** ki tarah hai: Aisle 1 par biscuit khareedne wala aur Aisle 5 par sabzi lene wala dono ek sath bina kisi ladai ke saman le sakte hain! Sirf usi specific bucket par lock lagta hai jahan do log ek hi item ko chhoote hain (**Fine-Grained Bucket-Level Locking via CAS & Synchronized Node**)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **HashMap Internal Storage**:
   - Backed by an array of `Node<K, V>[] table` (Buckets).
   - Index calculated as: `index = (n - 1) & hash(key)`.
   - Default capacity: 16, Load factor: 0.75. Resizes to double ($32$) when elements exceed threshold ($16 \times 0.75 = 12$).
2. **Java 8 Treeification Threshold**:
   - When a bucket's linked list length exceeds **8** and table capacity is $\ge 64$, the bucket linked list converts into a **Red-Black Tree** (`TreeNode`).
   - Worst-case lookup time improves from $O(N)$ to $O(\log N)$, defending against Hash Collision DoS attacks.
3. **`ConcurrentHashMap` in Java 8+**:
   - Removed Java 7's heavy `Segment[]` locking array.
   - **Reads (`get`)**: 100% lock-free using volatile memory semantics on node values (`volatile V val`).
   - **Writes (`put`)**:
     - If the bucket is empty, it writes the node using lock-free **CAS (Compare-And-Swap)**.
     - If the bucket has collisions, it locks **only the head node** of that specific bucket using `synchronized(node)`. Other buckets remain fully concurrent!

---

## 📊 3. Visual Architecture Diagram

```
             CONCURRENTHASHMAP FINE-GRAINED LOCKING
             
   Bucket Array:
   [ 0 ] ──► CAS Write (Lock-Free!) ──► [ Node A ]
   [ 1 ] ──► (Empty)
   [ 2 ] ──► synchronized(Head Node) ──► [ Head ] ──► [ Node B ] ──► [ Node C ]
              (Locks ONLY Bucket 2! Bucket 0, 1, 3 remain 100% accessible!)
   [ 3 ] ──► Red-Black Tree (O(log N))
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```java
package com.knowledgebase.collections;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

public class HighThroughputMetricsStore {

    // Line 9: Thread-safe high-concurrency map
    private final ConcurrentHashMap<String, LongAdder> endpointCounters = new ConcurrentHashMap<>();

    // Line 12: Atomic increment without lock contention using LongAdder
    public void recordEndpointHit(String endpoint) {
        // computeIfAbsent is executed atomically by ConcurrentHashMap
        endpointCounters.computeIfAbsent(endpoint, k -> new LongAdder()).increment();
    }

    // Line 18: Retrieve current count safely
    public long getCount(String endpoint) {
        LongAdder adder = endpointCounters.get(endpoint);
        return adder != null ? adder.sum() : 0L;
    }

    // Line 24: Atomic CAS update demonstration with compute()
    public void updateAccountBalance(ConcurrentHashMap<String, Double> balances, String accountId, double delta) {
        // Atomically recalculates new value without race conditions
        balances.compute(accountId, (key, currentBalance) -> {
            if (currentBalance == null) {
                return delta;
            }
            return currentBalance + delta;
        });
    }
}
```

---

## 🎯 5. The "Interview Pitch"
> "In Java collections, `HashMap` is non-thread-safe and can enter corrupted states under concurrent mutations. Java 8 introduced treeification, converting hash collision buckets from linked lists to Red-Black Trees once a bucket exceeds 8 entries, safeguarding lookup performance at $O(\log N)$. For concurrent environments, `ConcurrentHashMap` abandons the coarse segment-locking of Java 7 in favor of fine-grained bucket-level synchronization. Read operations are entirely lock-free via volatile field reads. Write operations insert into empty buckets using lock-free hardware CAS primitives and synchronize solely on the individual bucket head node when collisions occur, delivering near-linear throughput scaling across CPU cores."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: An authentication gateway stored active user rate-limiting token buckets in a standard `Collections.synchronizedMap(new HashMap<>())`. Under 8,000 requests/second, JVM thread dumps showed 140 worker threads in `BLOCKED (on object monitor)` state waiting on the single map lock, causing latency to spike to 2,400ms.
- **Task**: Eliminate lock contention and reduce rate-limiter latency to under 1ms.
- **Action**: We refactored the map to `ConcurrentHashMap<String, TokenBucket>`. To eliminate locking during atomic counter increments, we wrapped values in `LongAdder` and used `computeIfAbsent()` for thread-safe instantiation.
- **Result**: Thread contention dropped to 0%, CPU utilization fell from 94% to 22%, and rate-limiting check latency dropped from 2,400ms to 0.08ms under identical load.
""",

    os.path.join(BASE_DIR, "09-backend-java-springboot", "interview-questions", "top_java_springboot_interview_questions.md"): """# Top Java & Spring Boot Senior Interview Questions

---

## 1. What is the difference between Virtual Threads and Platform Threads in Java 21?
- **Platform Threads**: Direct 1:1 mappings to OS kernel threads. Heavy ($\sim 1 \text{ MB}$ stack), expensive context switching, limited to $\sim 5,000$ concurrent threads per JVM.
- **Virtual Threads**: Managed by the JVM runtime in user-space. Lightweight ($\sim 1 \text{ KB}$ heap memory), run on top of carrier threads, unmounted during blocking I/O, allowing millions of concurrent threads.

---

## 2. Explain Spring Bean Scopes and Thread-Safety.
- **Singleton** (Default): Exactly one instance per Spring IoC container. **Not thread-safe** if it holds mutable instance variables! Must be stateless.
- **Prototype**: A fresh new instance created every time the bean is requested.
- **Request**: Scoped to the lifecycle of a single HTTP request (Web apps).
- **Session**: Scoped to an HTTP Session.

---

## 3. How does `@Transactional` work in Spring Boot, and what causes it to fail silently?
- **How it works**: Uses Spring AOP dynamic proxies. The proxy intercepts the method call, opens a database transaction, invokes the target method, and commits upon completion (or rolls back on `RuntimeException`).
- **Common Failure Scenarios**:
  - **Self-Invocation**: Calling a `@Transactional` method from another method within the **same class** (`this.doWork()`) bypasses the Spring AOP proxy; transactions are completely ignored!
  - **Checked Exceptions**: By default, transactions roll back **only** for unchecked exceptions (`RuntimeException` and `Error`). Checked exceptions (`Exception`) commit unless specified: `@Transactional(rollbackFor = Exception.class)`.
  - **Non-Public Methods**: Applying `@Transactional` to `private` or `protected` methods is ignored by default proxies.

---

## 4. What is the difference between `@Controller` and `@RestController`?
- `@Controller`: Traditional Spring MVC annotation used for returning HTML view templates (JSP, Thymeleaf).
- `@RestController`: Convenience annotation combining `@Controller` and `@ResponseBody`. Automatically serializes returned objects into JSON/XML HTTP response bodies.

---

## 5. What are the key enhancements of Spring Boot 3 over Spring Boot 2?
- Requires **Java 17 baseline** (supports Java 21 Virtual Threads natively).
- Upgraded to **Jakarta EE 10** (namespace changed from `javax.*` to `jakarta.*`).
- Native compilation via **GraalVM Native Image** support for sub-second startup and low memory footprints.
- Observability overhaul with **Micrometer Tracing** and OpenTelemetry integration.
"""
}

def main():
    print(f"Generating {len(FILES)} Core Java 21 & Spring Boot deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Core Java 21 & Spring Boot generation complete!")

if __name__ == "__main__":
    main()
