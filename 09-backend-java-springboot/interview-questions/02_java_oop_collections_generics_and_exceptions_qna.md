# Java 21 & Spring Boot Master Interview Bank: Part 2 (Q21 - Q40)
## OOP, Collections Framework, Generics & Streams

---

### Q21: How does Dynamic Method Dispatch work under the hood in the JVM?
**Answer:**
- **Dynamic Dispatch:** The mechanism by which a call to an overridden method is resolved at runtime rather than compile time.
- **Under the Hood (vtable / Virtual Method Table):**
  - When the JVM loads a class into **Metaspace**, it creates a **vtable** for that class.
  - The vtable is an array of memory pointers to the actual bytecode implementations of virtual methods.
  - If a subclass overrides `speak()`, its vtable pointer for `speak()` points to the subclass's code; if it does not override, it points to the parent's code.
  - At runtime, invoking `animal.speak()` does not search class hierarchies; it performs an instant $O(1)$ indexed lookup into the vtable!

---

### Q22: What are the differences between Abstract Classes and Interfaces in Java 21?
**Answer:**
| Dimension | Abstract Class | Interface |
| :--- | :--- | :--- |
| **State / Fields** | Can have instance variables with state (mutable/non-final). | Fields are **implicitly `public static final`** constants only. |
| **Inheritance** | Single inheritance only (`extends OneClass`). | Multiple inheritance supported (`implements A, B, C`). |
| **Constructors** | **Has constructors** (called by subclass `super()`). | **Zero constructors**; cannot be instantiated. |
| **Method Types** | Abstract, concrete, final, static, private. | Abstract, `default`, `static`, `private` (Java 9+ helper methods). |
| **Design Intent** | "Is-a" relationship sharing state and core blueprint. | "Can-do" capability or contract (e.g. `Serializable`, `Comparable`). |

---

### Q23: How does `ArrayList` work internally, and what is its resizing formula?
**Answer:**
- `ArrayList` is backed by a dynamically resizing contiguous array (`Object[] elementData`).
- **Initial Capacity:** Default capacity is **10** (allocated lazily on the first `add()` invocation).
- **Growth Resizing Formula:**
  When full, it allocates a new array sized at **$1.5\times$ original capacity** using bitwise right-shift:
  $$\text{newCapacity} = \text{oldCapacity} + (\text{oldCapacity} \gg 1)$$
  - *Example:* $10 \to 15 \to 22 \to 33 \dots$
  - Elements are copied from old array to new array using optimized C-level memory copy `System.arraycopy()`.
  - **Amortized Time Complexity:** $O(1)$ append; $O(N)$ worst-case resize.

---

### Q24: How does `HashMap` work internally in Java 8+? Explain Bucket Treeification.
**Answer:**
`HashMap` is an array of `Node<K,V>` buckets (default initial capacity = 16, load factor = 0.75):
1. **Hashing & Index Calculation:**
   $$\text{hash} = \text{key.hashCode()} \oplus (\text{hash} \gg 16)$$
   $$\text{index} = (n - 1) \ \& \ \text{hash}$$
   Bitwise AND replaces expensive modulo `%`.
2. **Collision Resolution:**
   - Keys with matching bucket indices form a linked list.
3. **Bucket Treeification (Java 8+):**
   - If the number of collided elements in a single bucket reaches **`TREEIFY_THRESHOLD = 8`** AND total map capacity $\ge 64$, the linked list is transformed into a balanced **Red-Black Tree (`TreeNode`)**.
   - Improves worst-case search complexity from $O(N)$ down to **$O(\log N)$**, mitigating HashDoS security attacks!
   - If deletions drop tree size to **`UNTREEIFY_THRESHOLD = 6`**, it converts back to a linked list.

---

### Q25: How does `ConcurrentHashMap` achieve thread safety without locking the entire map?
**Answer:**
- **In Java 7:** Used **Segment Locks** (ReentrantLock on 16 distinct segments).
- **In Java 8+:** Completely eliminated segments:
  1. **Lock-Free Reads:** `get()` operations are 100% lock-free (uses `volatile` value pointers).
  2. **CAS (Compare-And-Swap) for Empty Buckets:** If a bucket is empty, `put()` inserts the first node using hardware-level atomic CAS without acquiring any locks!
  3. **Fine-Grained Synchronized Bucket Head Locking:** If a collision occurs (bucket is not empty), it locks **only the head node of that specific bucket** using `synchronized(node)`.
  4. Concurrent operations on different buckets proceed simultaneously with zero contention.

---

### Q26: What is the difference between Fail-Fast and Fail-Safe Iterators?
**Answer:**
- **Fail-Fast Iterators (`ArrayList`, `HashMap`, `HashSet`):**
  - Track a modification counter `modCount`.
  - If the collection is structurally modified (added/removed) while iterating via any method other than the iterator's own `iterator.remove()`, it immediately throws **`ConcurrentModificationException`**.
- **Fail-Safe / Weakly Consistent Iterators (`CopyOnWriteArrayList`, `ConcurrentHashMap`):**
  - Operates on a snapshot or cloned copy of the collection or iterates weakly consistent views.
  - Never throws `ConcurrentModificationException` when modified concurrently.

---

### Q27: What is Generics Type Erasure in Java?
**Answer:**
- Generics were introduced in Java 5 to provide compile-time type safety.
- **Type Erasure:** To maintain backwards binary compatibility with pre-Java 5 bytecode, the Java compiler **erases all generic type parameters** during compilation.
  - `List<String>` and `List<Integer>` both compile to raw `List` in `.class` bytecode.
  - Type checks and explicit casts are inserted automatically by the compiler.
  - *Implication:* You cannot do `new T()`, `new T[10]`, or `instanceof List<String>` at runtime.

---

### Q28: Explain the PECS Principle in Java Generics (Producer Extends, Consumer Super).
**Answer:**
Governs when to use `? extends T` vs `? super T` wildcards:
- **Producer Extends (`<? extends T>`):**
  If a parameterized type represents an entity that **produces / outputs data** (you read from it), use `extends`.
  - *Rule:* You can read `T` objects out of it, but you **cannot write/add** anything into it (except `null`).
- **Consumer Super (`<? super T>`):**
  If a parameterized type represents an entity that **consumes / inputs data** (you write to it), use `super`.
  - *Rule:* You can write `T` objects into it, but reading only returns `Object`.

```java
// Collections.copy(List<? super T> dest, List<? extends T> src)
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    for (T item : src) { // src produces T
        dest.add(item);  // dest consumes T
    }
}
```

---

### Q29: Explain the Java Exception Hierarchy: Checked vs Unchecked.
**Answer:**
```
                           Throwable
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
          Error                               Exception
    (Fatal JVM Failures)                          │
    - OutOfMemoryError              ┌─────────────┴─────────────┐
    - StackOverflowError            ▼                           ▼
                             RuntimeException            Checked Exceptions
                             (Unchecked)                 - IOException
                             - NullPointerException      - SQLException
                             - IllegalArgumentException  - ClassNotFoundException
```

- **Checked Exceptions:** Subclasses of `Exception` (excluding `RuntimeException`). Checked at compile time; methods **must** handle them via `try-catch` or declare them via `throws`. Represent recoverable external failures.
- **Unchecked Exceptions:** Subclasses of `RuntimeException` and `Error`. Not checked at compile-time. Represent programming logic bugs (null dereferences, illegal arguments, array bounds).

---

### Q30: How does `try-with-resources` work and what is `AutoCloseable`?
**Answer:**
- Introduced in Java 7 to eliminate manual resource cleanup boilerplate in `finally` blocks.
- Any object implementing **`java.lang.AutoCloseable`** or `java.io.Closeable` can be instantiated inside the `try (...)` statement:
  ```java
  try (var br = new BufferedReader(new FileReader("file.txt"))) {
      return br.readLine();
  } // Automatically calls br.close() even if an exception is thrown!
  ```
- **Suppressed Exceptions:** If both the `try` block and the `close()` method throw exceptions, the primary exception is thrown and the close exception is preserved on it via `e.getSuppressed()`.

---

### Q31: How do Java Streams work? Intermediate vs Terminal operations.
**Answer:**
A Stream is a sequence of elements supporting sequential and parallel aggregate operations:
- **Intermediate Operations (Lazy Evaluation):**
  Return a new Stream (`filter()`, `map()`, `sorted()`, `distinct()`). They do **not execute** until a terminal operation is invoked.
- **Terminal Operations (Eager Execution):**
  Traverse the pipeline, produce a final non-stream result, and close the stream (`collect()`, `forEach()`, `reduce()`, `count()`).
- **Loop Fusion:** The JVM optimizes the stream pipeline into a single pass over the elements, processing each element through all intermediate stages together.

---

### Q32: When should you NOT use Parallel Streams (`.parallelStream()`)?
**Answer:**
Parallel streams use the shared JVM-wide **`ForkJoinPool.commonPool()`**. Avoid parallel streams when:
1. **I/O Bound Operations:** Making network calls or DB queries in parallel streams blocks threads in the global common pool, starving other parts of the application.
2. **Small Collections ($N < 10,000$):** Thread scheduling and splitting overhead exceeds the cost of a sequential loop.
3. **Operations that rely on Order or State:** `findFirst()`, `limit()`, or operations mutating shared variables.

---

### Q33: What is the difference between `map()` and `flatMap()` in Java Streams?
**Answer:**
- **`map(Function<T, R>)`**: One-to-One mapping. Transforms each element of type `T` into an element of type `R`:
  `Stream<List<String>> -> Stream<Integer>`
- **`flatMap(Function<T, Stream<R>>)`**: One-to-Many mapping with flattening. Transforms each element into a Stream, and then **flattens the nested streams into a single consolidated stream**:
  `List<List<String>> -> flatMap(List::stream) -> Stream<String>`

---

### Q34: What is `Optional<T>` and what are the best practices for using it?
**Answer:**
- A container object designed to represent the presence or absence of a non-null value, eliminating explicit `null` checks and preventing `NullPointerException`.
- **Best Practices:**
  1. **Use as Return Types ONLY:** Ideal for method returns where a result might be absent (`userRepository.findById(id)`).
  2. **Do NOT use for fields or parameters:** `Optional` is not `Serializable`, adding unnecessary heap object wrapper overhead.
  3. **Avoid `.get()` without checking:** Always prefer `.orElse()`, `.orElseGet(() -> expensive())`, or `.orElseThrow()`.

---

### Q35: What is the difference between `IdentityHashMap` and standard `HashMap`?
**Answer:**
- **`HashMap`**: Uses `equals()` to compare keys and `hashCode()` to find bucket index.
- **`IdentityHashMap`**: Uses **Reference Equality (`==`)** to compare keys and `System.identityHashCode(k)` to find bucket index. Two keys are considered equal if and only if they reference the identical memory address (`k1 == k2`).

---

### Q36: What is a `WeakHashMap` and how does it prevent memory leaks?
**Answer:**
- `WeakHashMap` stores keys as **`WeakReference`**.
- If a key object has no other strong references outside the map, the Garbage Collector reclaims the key on the next GC cycle, and the entry is automatically purged from the map.
- **Use Case:** Canonical object caching, metadata attachments.

---

### Q37: How does `BlockingQueue` work in producer-consumer multithreading?
**Answer:**
- Thread-safe queue supporting flow control operations:
  - `put(e)`: Inserts element, **blocking the producer thread** if the queue is full.
  - `take()`: Retrieves element, **blocking the consumer thread** if the queue is empty.
- Standard implementations: `ArrayBlockingQueue` (bounded array), `LinkedBlockingQueue` (optionally bounded linked nodes).

---

### Q38: What is `EnumMap` and why is it faster than `HashMap`?
**Answer:**
- A specialized `Map` implementation designed exclusively for keys of an `enum` type.
- Under the hood, it is represented as a **compact contiguous Java array (`Object[] vals`)** indexed by the enum's natural ordinal integer (`enum.ordinal()`).
- Incurs **zero hash calculations, zero hash collisions, and zero linked list overhead**. Operations run at direct array indexing speeds.

---

### Q39: What is the difference between `poll()`, `remove()`, and `peek()` in Java Queue?
**Answer:**
- **`peek()`**: Inspects element at the head of the queue without removing it. Returns `null` if queue is empty.
- **`poll()`**: Retrieves and removes head of queue. Returns `null` if queue is empty.
- **`remove()`**: Retrieves and removes head of queue. Throws `NoSuchElementException` if queue is empty.

---

### Q40: What are Functional Interfaces and `@FunctionalInterface` annotation?
**Answer:**
- An interface that contains **exactly one abstract method (SAM)**.
- Can contain any number of `default` or `static` methods.
- Can be implemented via **Lambda Expressions** (`() -> ...`) or **Method References** (`String::toUpperCase`).
- Built-in Core Interfaces: `Predicate<T>` (tests boolean), `Function<T, R>` (transforms), `Consumer<T>` (void action), `Supplier<T>` (produces value).
