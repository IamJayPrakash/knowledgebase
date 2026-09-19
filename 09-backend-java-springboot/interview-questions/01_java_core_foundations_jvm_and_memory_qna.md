# Java 21 & Spring Boot Master Interview Bank: Part 1 (Q1 - Q20)
## Core Java Foundations, JVM Architecture & Memory Management

---

### Q1: Diagram and explain the internal architecture of the JVM (Java Virtual Machine).
**Answer:**

```
                      [.java Source File]
                              │ (javac)
                              ▼
                      [.class Bytecode]
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                 CLASS LOADER SUBSYSTEM                 │
  │  Loading (Bootstrap -> Extension/Platform -> App)    │
  │  Linking (Verify -> Prepare -> Resolve)               │
  │  Initialization (static blocks & static fields)       │
  └───────────────────────────┬───────────────────────────┘
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                 JVM RUNTIME DATA AREAS                 │
  │  ┌───────────────────────┐  ┌──────────────────────┐  │
  │  │ Heap Space (All Threads) │  │ Metaspace (Native RAM)│  │
  │  └───────────────────────┘  └──────────────────────┘  │
  │  ┌───────────────────────┐  ┌──────────────────────┐  │
  │  │ Thread Stack (Per Thread)│ │ PC Register & Native │  │
  │  └───────────────────────┘  └──────────────────────┘  │
  └───────────────────────────┬───────────────────────────┘
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                    EXECUTION ENGINE                   │
  │  Interpreter ──► JIT Compiler (C1 / C2) ──► GC (ZGC/G1)│
  └───────────────────────────────────────────────────────┘
```

---

### Q2: What are the JVM Memory Data Areas and what does each store?
**Answer:**
1. **Heap Space (Shared across all threads):**
   Stores all instantiated objects, arrays, and their instance fields. Managed by the Garbage Collector.
2. **Thread Stack (Private per thread):**
   Stores stack frames for active method invocations. Each frame contains local primitive variables, references to heap objects, operand stack, and method return address.
3. **Metaspace (Shared, allocated in Native OS RAM since Java 8):**
   Stores class metadata, bytecodes, method data, vtables, and runtime constant pools. Replaced PermGen to eliminate `java.lang.OutOfMemoryError: PermGen space`.
4. **Program Counter (PC) Register (Private per thread):**
   Stores the memory address of the JVM instruction currently being executed by the thread.
5. **Native Method Stack (Private per thread):**
   Holds stack frames for native C/C++ methods called via JNI (Java Native Interface).

---

### Q3: How does the Tiered JIT (Just-In-Time) Compiler work (Interpreter vs C1 vs C2)?
**Answer:**
- **Interpreter:** Quickly converts bytecode into machine instructions one by one at startup (instant startup, but slow execution).
- **Tier 1 (C1 / Client Compiler):** Compiles frequently executed methods ("hot code") into native machine code with basic optimizations (fast compilation, moderate performance).
- **Tier 2 (C2 / Server Compiler):** Profiles code during runtime. For heavily invoked methods, C2 applies aggressive, deep optimizations: method inlining, loop unrolling, dead code elimination, and Escape Analysis.

---

### Q4: What is Escape Analysis and Scalar Replacement in the JVM?
**Answer:**
- **Escape Analysis:** JIT compiler analysis that determines whether a newly allocated object's reference escapes outside the method's scope.
- **Scalar Replacement (Stack Allocation):**
  If an object is proven **never to escape** the method, the JIT does NOT allocate the object on the Heap! Instead, it decomposes the object into its individual primitive fields (scalars) and allocates them directly on the **Thread Stack** or in CPU registers.
- **Impact:** Eliminates heap allocations and reduces Garbage Collection pressure to zero for temporary local objects.

---

### Q5: Is Java "Pass-by-Value" or "Pass-by-Reference"? Prove it.
**Answer:**
**Java is strictly and 100% Pass-by-Value.**
- When passing primitives (`int`, `boolean`), Java copies the raw value.
- When passing objects, Java passes **a copy of the reference address by value**.

**Proof:**
```java
public class ValueProof {
    public static void swap(Person p1, Person p2) {
        Person temp = p1;
        p1 = p2; // Reassigns local copy of pointer
        p2 = temp;
    }

    public static void main(String[] args) {
        Person a = new Person("Alice");
        Person b = new Person("Bob");
        swap(a, b);
        System.out.println(a.name); // Still "Alice"! (If pass-by-reference, would be "Bob")
    }
}
```

---

### Q6: Why is `String` immutable in Java? List 4 architectural reasons.
**Answer:**
1. **String Constant Pool (SCP) Optimization:** Different variables referencing `"hello"` share the exact same heap memory address. If Strings were mutable, modifying `s1` would silently corrupt `s2`.
2. **Security:** Strings are used for database connection URLs, passwords, filesystem paths, and network sockets. Immutability guarantees malicious code cannot alter connection targets after security validation.
3. **Thread Safety:** Immutable objects are inherently thread-safe and can be shared across multiple threads without synchronization locks.
4. **HashCode Caching:** A String's `hashCode()` is calculated once during creation and cached lazily. This makes Strings optimal keys for `HashMap` with instant $O(1)$ lookups.

---

### Q7: What is the String Constant Pool (SCP) and how does `String.intern()` work?
**Answer:**
- **String Constant Pool (SCP):** A dedicated memory area inside the Heap managed by JVM `StringTable`.
- `String s1 = "Java";` checks SCP. If `"Java"` exists, returns SCP reference; otherwise creates it in SCP.
- `String s2 = new String("Java");` creates two objects: one in SCP (if missing) and a separate new object in general Heap memory.
- **`s2.intern()`:** Queries the SCP. If the pool contains a matching string, returns the SCP reference, allowing `s2.intern() == s1` to evaluate to `true`.

---

### Q8: What is the difference between `String`, `StringBuilder`, and `StringBuffer`?
**Answer:**
| Feature | `String` | `StringBuilder` | `StringBuffer` |
| :--- | :--- | :--- | :--- |
| **Mutability** | **Immutable** | **Mutable** | **Mutable** |
| **Thread Safety** | Inherently thread-safe | **Not thread-safe** | **Thread-safe** (methods are `synchronized`) |
| **Performance** | Slow for concatenation ($O(N^2)$ creates intermediate objects) | **Fastest** (zero lock overhead) | Slower due to lock acquisition contention |
| **Use Case** | Constants, Map keys, entity fields | Local string manipulations inside single methods | Multi-threaded shared append buffers (rare) |

---

### Q9: What is the contract between `equals()` and `hashCode()`?
**Answer:**
1. If two objects are equal according to `equals(Object)`, their `hashCode()` **MUST return the exact same integer**.
2. If two objects have the same `hashCode()`, they are **NOT required to be equal** (Hash Collision).
3. If `equals()` is overridden, `hashCode()` **MUST ALWAYS be overridden**; otherwise, the object will fail to be retrieved when used as a key in `HashMap` or `HashSet`.

---

### Q10: What is the Integer Cache in Java?
**Answer:**
- To save memory and improve performance, the JVM pre-allocates and caches `Integer` objects for values between **`-128` and `127`** (inclusive) inside `Integer.IntegerCache`.
- Boxing primitives in this range returns the same cached instance:

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b); // true (Same cached instance!)

Integer c = 128;
Integer d = 128;
System.out.println(c == d); // false (Allocated as two different heap objects!)
System.out.println(c.equals(d)); // true (Compares underlying int value)
```

---

### Q11: Explain JVM Garbage Collection: Generational Hypothesis.
**Answer:**
Based on the empirical observation that **most objects die shortly after allocation**:
- **Young Generation (Eden + 2 Survivor Spaces S0/S1):**
  New objects are allocated in Eden. When Eden fills, **Minor GC** moves live objects to S0. Objects that survive multiple minor GC cycles (default threshold: 15) are promoted to Old Generation.
- **Old Generation (Tenured):**
  Holds long-lived objects (Spring singletons, connection pools). Collected via **Major / Full GC**.

---

### Q12: How does the G1 (Garbage-First) Collector work?
**Answer:**
- Standard in Java 9 through Java 21 for general workloads.
- Divides the entire heap into ~2,048 equal-sized contiguous memory **regions** (from 1MB to 32MB).
- Regions are assigned roles dynamically (Eden, Survivor, Old, Humongous).
- **Garbage-First Principle:** Tracks regions containing the most dead garbage and collects those regions first, meeting user-specified pause time targets (`-XX:MaxGCPauseMillis=200`).

---

### Q13: What is ZGC (Z Garbage Collector) in Java 21?
**Answer:**
- A scalable, low-latency concurrent garbage collector designed for modern multi-terabyte heaps.
- **Key Metric:** Guarantees max GC pause times of **$< 1$ millisecond**, independent of heap size (from 8MB to 16 Terabytes)!
- **How it works:**
  1. Performs all heavy GC work (Marking, Relocation, Compaction) **concurrently with active application threads**.
  2. Uses **Colored Pointers** (stores reference metadata in reference bit flags) and **Load Barriers** (intercepts reference access to update pointers on the fly).
  3. **Generational ZGC (Java 21):** Introduced generational separation for even higher throughput.

---

### Q14: What is the difference between `final`, `finally`, and `finalize()`?
**Answer:**
- **`final` (Keyword):**
  - Variable: Value cannot be reassigned (constant).
  - Method: Method cannot be overridden by subclasses.
  - Class: Class cannot be extended/subclassed.
- **`finally` (Block):** Block following `try-catch` that **always executes** (used for resource cleanup), even if exceptions are thrown or `return` is executed.
- **`finalize()` (Method):** Deprecated method on `Object`. Called before GC reclaims memory. Highly discouraged due to unpredictable execution timing and memory leaks; completely removed in modern Java.

---

### Q15: When does a `finally` block NOT execute?
**Answer:**
A `finally` block fails to execute in only 3 extreme scenarios:
1. `System.exit(0)` is invoked inside the `try` or `catch` block.
2. The JVM crashes or suffers a fatal fatal OS signal (`kill -9`, OutOfMemoryError in GC thread).
3. The thread executing the `try` block is interrupted or killed externally by the OS host.

---

### Q16: What is the Diamond Problem and how does Java 8 resolve it with Interfaces?
**Answer:**
- Occurs when a class inherits from two parents that implement the same method signature.
- Java avoids this in classes by restricting to single class inheritance.
- **Java 8 Default Methods:** If Class `C` implements interfaces `A` and `B`, and both define `default void print()`, Java refuses to compile: `duplicate default methods named print`.
- **Resolution:** The implementing class `C` **must explicitly override** the colliding method and choose which implementation to invoke: `A.super.print();`.

---

### Q17: What are Records in Java 17/21 and what boilerplate do they eliminate?
**Answer:**
- A `record` is an immutable, transparent data carrier class introduced in Java 14 and finalized in Java 16.
- Declaring `public record UserDto(Long id, String name, String email) {}`:
  - Automatically generates: `final` fields, canonical constructor, accessor methods (`id()`, `name()`, `email()`), `equals()`, `hashCode()`, and `toString()`.
  - Records cannot extend other classes (they implicitly extend `java.lang.Record`), but can implement interfaces.

---

### Q18: What are Sealed Classes in Java 17/21?
**Answer:**
- A `sealed` class or interface restricts which other classes or interfaces may extend or implement it using the `permits` keyword:
  ```java
  public sealed interface PaymentMethod permits CreditCard, PayPal, Crypto {}
  ```
- **Benefit:** Enables exhaustive Pattern Matching in `switch` statements without requiring a `default` branch, catching missing domain models at compile time!

---

### Q19: What is Pattern Matching for `switch` in Java 21?
**Answer:**
Allows switching over types and destructuring records directly with `when` guards:

```java
static String formatValue(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("Integer: %d", i);
        case Long l    -> String.format("Long: %d", l);
        case String s when s.length() > 10 -> "Long String: " + s;
        case String s  -> "Short String: " + s;
        case null      -> "Null value handled safely!";
        default        -> obj.toString();
    };
}
```

---

### Q20: What is the difference between `Comparable` and `Comparator`?
**Answer:**
- **`Comparable<T>` (Internal/Natural Ordering):**
  Implemented by the domain class itself (`class Employee implements Comparable<Employee>`). Overrides `compareTo(T o)`. Defines a single default sorting logic.
- **`Comparator<T>` (External/Custom Ordering):**
  Separate class or lambda passed to sort methods: `list.sort(Comparator.comparing(Employee::getSalary).reversed())`. Allows multiple dynamic sorting criteria (by salary, by age, by name).
