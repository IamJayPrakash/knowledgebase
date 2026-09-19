# Java 21 & Spring Boot Master Interview Bank: Part 3 (Q41 - Q60)

## Concurrency, Threading, Memory Model & Virtual Threads (Loom)

---

### Q41: Explain the Java Thread Lifecycle and 6 Thread States

**Answer:**

```
                  ┌──────────────┐
                  │     NEW      │ (new Thread())
                  └──────┬───────┘
                         │ .start()
                         ▼
                  ┌──────────────┐
           ┌────► │   RUNNABLE   │ ◄────┐
           │      └──────┬───────┘      │
Acquires lock            │              │ Notified / Time elapsed
           │             ▼              │
    ┌──────────┐  ┌──────────────┐  ┌──────────────┐
    │ BLOCKED  │  │   WAITING    │  │TIMED_WAITING │
    └──────────┘  └──────────────┘  └──────────────┘
 (Waiting for       (.wait(),        (sleep(ms),
  monitor lock)     .join())         .wait(ms))
                         │
                  Method completes / uncaught exception
                         │
                         ▼
                  ┌──────────────┐
                  │  TERMINATED  │
                  └──────────────┘
```

---

### Q42: What is the difference between `synchronized` and `ReentrantLock`?

**Answer:**

| Feature | `synchronized` (Keyword) | `ReentrantLock` (Class) |
| :--- | :--- | :--- |
| **Acquisition** | Implicit block scope; releases automatically on block exit. | Explicit `lock.lock()` and mandatory `finally { lock.unlock(); }`. |
| **Non-blocking Try** | ❌ No. Thread blocks indefinitely. | ✅ Yes. `lock.tryLock()` or `lock.tryLock(timeout, unit)`. |
| **Fairness Guarantee** | ❌ No. Non-fair (barging). | ✅ Yes. Can configure fair ordering: `new ReentrantLock(true)`. |
| **Interruptibility** | ❌ Cannot be interrupted while blocked. | ✅ Yes. `lock.lockInterruptibly()` responds to interruption. |
| **Condition Variables** | Single wait-set (`wait()`, `notify()`). | Multiple independent conditions (`lock.newCondition()`). |

---

### Q43: What does the `volatile` keyword do in Java? Explain the Java Memory Model (JMM)

**Answer:**
Modern multi-core CPUs cache variables in local L1/L2 CPU caches.
Without `volatile`, updates made by Thread 1 in CPU Core 1's cache may not be flushed to main RAM, remaining invisible to Thread 2 running on CPU Core 2.

- **`volatile` guarantees two properties:**
  1. **Visibility:** Writes to a volatile variable are immediately flushed to main memory; reads always bypass CPU caches and read directly from main RAM.
  2. **Instruction Reordering Prevention:** Inserts hardware **Memory Barriers** preventing the JIT compiler and CPU from reordering instructions across the volatile read/write barrier (**Happens-Before Relationship**).
- *Limitation:* `volatile` does **NOT guarantee atomicity**! `count++` on a volatile variable is still three non-atomic operations (read, increment, write) and will suffer race conditions.

---

### Q44: How do `AtomicInteger` and Atomic classes work without locks?

**Answer:**

- Atomic classes (`AtomicInteger`, `AtomicReference`, `LongAdder`) achieve lock-free thread safety using **hardware-level CAS (Compare-And-Swap)** instructions (e.g. `cmpxchg` in x86 assembly).
- **The CAS Loop:**

  ```java
  public final int incrementAndGet() {
      int current;
      int next;
      do {
          current = get(); // Read current volatile value
          next = current + 1;
      } while (!compareAndSet(current, next)); // Atomic CPU instruction!
      return next;
  }
  ```

- If another thread modified the value in the background, CAS fails and the loop retries instantly without suspending the thread or incurring OS context-switching overhead.

---

### Q45: What is the ABA Problem in CAS and how does `AtomicStampedReference` solve it?

**Answer:**

- **ABA Problem:** Thread 1 reads value $A$. Thread 2 changes $A \to B \to A$. Thread 1 executes CAS, observes value is still $A$, and assumes nothing changed, which can corrupt node pointers in lock-free linked lists.
- **Solution:** **`AtomicStampedReference<V>`** pairs the object reference with an integer version stamp / sequence counter:
  `(Reference: A, Stamp: 1) -> (B, 2) -> (A, 3)`.
  CAS checks both reference equality AND stamp equality.

---

### Q46: What is the difference between `CountDownLatch` and `CyclicBarrier`?

**Answer:**

- **`CountDownLatch`:**
  - One or more threads wait until a counter decrements to zero (`latch.countDown()`, `latch.await()`).
  - **Single-use only:** Once the count reaches zero, it **cannot be reset**.
- **`CyclicBarrier`:**
  - A synchronization point where a fixed set of threads must **all wait for each other** to arrive before proceeding (`barrier.await()`).
  - **Reusable (Cyclic):** Automatically resets to its initial count after the barrier is tripped, ideal for iterative parallel algorithms.

---

### Q47: How does `Semaphore` work?

**Answer:**

- A `Semaphore` controls access to a shared resource by maintaining a set of **permits**:
  - `semaphore.acquire()`: Grabs a permit; blocks if no permits are available.
  - `semaphore.release()`: Returns a permit back to the semaphore.
- **Use Case:** Limiting concurrency, implementing rate limiters, capping max concurrent calls to an expensive external service (e.g. max 10 concurrent connections).

---

### Q48: Explain `ThreadPoolExecutor` parameters and Sizing Formulas

**Answer:**

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    corePoolSize,       // Minimum active worker threads
    maximumPoolSize,    // Surge capacity limit
    keepAliveTime, unit,// Idle time before terminating surplus threads
    workQueue,          // Task buffer (LinkedBlockingQueue / ArrayBlockingQueue)
    threadFactory,      // Thread naming factory
    rejectedHandler     // Rejection policy when queue is full
);
```

**Thread Pool Sizing Formulas:**

1. **For CPU-Bound Tasks:**
   $$\text{Threads} = \text{CPU Cores} + 1$$
   (Adding more threads than cores causes thrashing and context switching).
2. **For I/O-Bound Tasks (Database queries, HTTP calls):**
   $$\text{Threads} = \text{CPU Cores} \times \left(1 + \frac{\text{Wait Time}}{\text{Compute Time}}\right)$$
   (If wait time is 90% and compute time is 10%, a 4-core machine can run $4 \times (1 + 9) = 40$ threads).

---

### Q49: What are the 4 Rejected Execution Policies in `ThreadPoolExecutor`?

**Answer:**
When both the task queue is full AND worker thread count has reached `maximumPoolSize`:

1. **`AbortPolicy` (Default):** Throws `RejectedExecutionException`.
2. **`CallerRunsPolicy`:** Forces the calling thread (e.g. HTTP request thread) to execute the task itself, applying natural **backpressure** and slowing down submissions.
3. **`DiscardPolicy`:** Silently drops the rejected task without error.
4. **`DiscardOldestPolicy`:** Discards the unhandled task at the head of the work queue and retries executing the new task.

---

### Q50: How do you detect and analyze Deadlocks in production Java applications?

**Answer:**

- **Detection Tools:**
  1. Generate a **Thread Dump**: `jstack <pid> > threaddump.txt` or `jcmd <pid> Thread.print`.
  2. Inspect the bottom of the dump: the JVM automatically runs cycle detection and outputs:
     `Found 1 deadlock. Thread-1 waiting to lock <0x01> held by Thread-2; Thread-2 waiting to lock <0x02> held by Thread-1`.
- **Prevention (Global Lock Ordering):**
  Always acquire multiple locks in a strict, globally consistent order across all classes (e.g. always acquire Lock A before Lock B).

---

### Q51: How does `CompletableFuture` enable non-blocking asynchronous composition?

**Answer:**
`CompletableFuture` represents a future result and provides monadic functional composition:

- `supplyAsync(() -> fetchUser())`: Submits task to `ForkJoinPool`.
- `.thenApply(user -> user.getEmail())`: Transforms result when available.
- `.thenCompose(email -> fetchOrders(email))`: Flattens dependent async calls (flatMap).
- `.thenCombine(otherFuture, (res1, res2) -> merge(res1, res2))`: Combines two independent parallel async tasks.
- `.exceptionally(ex -> fallback)`: Asynchronous error recovery.

---

### Q52: What is Java 21 Project Loom and why are Platform Threads limited?

**Answer:**

- **Platform OS Threads (Traditional Java):**
  - Thin 1-to-1 wrappers around OS kernel threads.
  - **High Cost:** Each OS thread allocates **1 MB of reserved virtual memory for its stack** and context-switching requires kernel privilege switches.
  - A server crashes with OutOfMemoryError after allocating ~5,000 to 10,000 OS threads.
- **Virtual Threads (Project Loom - Java 21):**
  - Ultra-lightweight JVM-managed user-mode threads ($M:N$ scheduling).
  - **Tiny Cost:** Stack is stored on the Java Heap and starts at **a few hundred bytes**, expanding dynamically!
  - A single JVM can comfortably run **1,000,000+ concurrent Virtual Threads** on commodity hardware!

---

### Q53: How does Carrier Thread Unmounting work in Virtual Threads?

**Answer:**

- Virtual Threads run on top of a small pool of underlying OS Platform Threads called **Carrier Threads** (default: number of CPU cores).
- **Non-blocking Continuation:**
  1. When code on a Virtual Thread initiates a blocking I/O operation (e.g., `socket.read()`, JDBC query, or `Thread.sleep()`), the JVM intercepts the call.
  2. The Virtual Thread's call frame is **unmounted from the carrier thread** and saved into heap memory.
  3. The Carrier Thread is immediately free to run other Virtual Threads!
  4. When the OS I/O completes, the JVM schedules the Virtual Thread to mount onto any available Carrier Thread and resume execution seamlessly.

---

### Q54: What is Thread Pinning in Virtual Threads and how do you avoid it?

**Answer:**

- **Thread Pinning:** Occurs when a Virtual Thread executes a blocking operation while holding a native monitor lock, preventing it from unmounting from its Carrier Thread. The underlying OS thread remains stuck!
- **Primary Causes:**
  1. Executing a blocking call inside a **`synchronized` block or method**.
  2. Executing a blocking call inside a **C/C++ native method (JNI)**.
- **Solution:** Replace `synchronized` blocks that guard I/O with **`ReentrantLock`**, which does NOT pin the carrier thread in Java 21!

---

### Q55: Why should you NEVER pool Virtual Threads?

**Answer:**

- Traditional thread pools (`Executors.newFixedThreadPool`) exist because OS threads are expensive to create and destroy.
- Virtual Threads are so lightweight that **creating a Virtual Thread is as cheap as allocating a plain Java object**.
- **Best Practice:** Create a new Virtual Thread per task and let it terminate upon task completion:

  ```java
  // ✅ IDIOMATIC JAVA 21:
  try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
      executor.submit(() -> handleRequest(req));
  }
  ```

---

### Q56: What is Structured Concurrency in Java 21 (Preview)?

**Answer:**

- Treats multiple concurrent tasks running in different threads as a **single unit of work**, ensuring that if one subtask fails, all other sibling tasks are automatically cancelled, eliminating thread leaks.
- Uses `StructuredTaskScope`:

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<User> user = scope.fork(() -> fetchUser());
    Supplier<Order> order = scope.fork(() -> fetchOrder());

    scope.join();           // Wait for both
    scope.throwIfFailed();  // Propagate error if either fails

    return new Response(user.get(), order.get());
} // Auto-cancels if parent exits!
```

---

### Q57: What are Scoped Values (JEP 446) and why do they replace `ThreadLocal`?

**Answer:**

- `ThreadLocal` has significant flaws with Virtual Threads:
  1. Unbounded memory footprint when millions of virtual threads allocate thread-local maps.
  2. Mutability allows code anywhere to alter thread context unpredictably.
- **Scoped Values (`ScopedValue<T>`):**
  - Immutable data bound to a lexical execution scope.
  - Automatically cleaned up when the scope exits; zero memory leaks and highly optimized for millions of virtual threads.

---

### Q58: What is the difference between `Thread.sleep()` and `Object.wait()`?

**Answer:**

- **`Thread.sleep(ms)`**: Puts the current thread to sleep for a specified duration. **Does NOT release any monitor locks** held by the thread.
- **`object.wait()`**: Must be called from inside a `synchronized(object)` block. **Releases the object monitor lock immediately**, allowing other waiting threads to acquire the lock and call `.notify()`.

---

### Q59: What is `ThreadLocal` and how does it cause Memory Leaks in Application Servers?

**Answer:**

- Provides thread-isolated variables (each thread accessing `threadLocal.get()` has its own independent copy).
- **The Memory Leak:**
  In Tomcat/Spring Boot, threads are pooled and reused across thousands of HTTP requests.
  If a thread sets a value in `ThreadLocal` and fails to call `threadLocal.remove()`, the object remains in the pooled thread's `threadLocals` map indefinitely, preventing classloaders from unloading and leaking megabytes of memory.

---

### Q60: How does `LongAdder` outperform `AtomicLong` under high contention?

**Answer:**

- Under heavy concurrent writes (e.g. 64 threads incrementing simultaneously), `AtomicLong` suffers severe performance degradation because all 64 threads compete on a single memory address via CAS, resulting in continuous failed retry loops.
- **`LongAdder` (Cell Striping):**
  - Maintains an array of counter cells.
  - Threads increment different cells based on their thread hash, eliminating contention.
  - The final sum is computed by summing across all cells on demand (`sum()`).
