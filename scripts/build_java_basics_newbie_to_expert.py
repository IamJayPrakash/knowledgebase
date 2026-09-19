# scripts/build_java_basics_newbie_to_expert.py
import os

BASE_DIR = r"D:\Projects\knowledgebase"

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# ==============================================================================
# 3. JAVA CORE BASICS (NEWBIE TO EXPERIENCED)
# ==============================================================================

JAVA_FUNDAMENTALS = """# Java Platform Fundamentals: JDK vs JRE vs JVM, Primitives & Pass-by-Value

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - JDK (Java Development Kit): Ek pura kitchen setup jisme recipe book, chaku, gas chulha sab hai (Compiler + Tools).
> - JRE (Java Runtime Environment): Ek dining table jahan sirf bana hua khana serve karke khaya ja sakta hai (Libraries + JVM, no cooking/compiler).
> - JVM (Java Virtual Machine): Ek magical chef jo kisi bhi sheher (Windows, Mac, Linux) mein ja kar wahi same recipe (Bytecode) padh kar waisa hi tasty khana bana deta hai ("Write Once, Run Anywhere").
> - Pass-by-Value: Java mein sab kuch copy hoke pass hota hai! Agar aap kisi ko apne ghar ki duplicate chaabi do, aur wo chaabi tod de, toh aapki original chaabi safe hai. Lekin agar wo us duplicate chaabi se ghar ke andar ghus kar sofa tod de (Object mutation), toh sofa toota hua hi milega!
>
> **Real-World Analogy:** Sending a photo via WhatsApp. You send a copy of the photo. If the recipient deletes or crops their copy, your original photo is unchanged. However, if you send a Google Doc link (reference value copy) and they delete the document text, the document itself is modified because both links pointed to the same document.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Execution Architecture**:
  - `javac MyProgram.java` compiles source code into platform-independent `.class` bytecode.
  - The JVM executes bytecode on the host operating system via ClassLoader, Bytecode Verifier, and Execution Engine (Interpreter + JIT Compiler).
- **8 Primitive Types**:
  - `byte` (8-bit, -128 to 127)
  - `short` (16-bit)
  - `int` (32-bit, default integer)
  - `long` (64-bit, suffix `L`)
  - `float` (32-bit IEEE 754, suffix `f`)
  - `double` (64-bit IEEE 754, default decimal)
  - `char` (16-bit Unicode `\\u0000` to `\\uffff`)
  - `boolean` (`true` or `false`)
- **Wrapper Classes & Autoboxing**:
  - Primitives have wrapper classes (`int` -> `Integer`, `char` -> `Character`).
  - Autoboxing automatically converts primitive to wrapper; Unboxing extracts primitive.
  - **Trap**: Unboxing a `null` wrapper throws a runtime `NullPointerException`!
- **Strictly Pass-by-Value**: Java is **100% Pass-by-Value**. There is no pass-by-reference in Java! When an object is passed, the reference address is copied by value. Reassigning the reference inside a method has zero effect on the caller's reference.

### 🧓 What an Experienced Candidate Knows:
- **Integer Cache Pool**: Java caches `Integer` objects in the range **`-128 to 127`**. Therefore, `Integer a = 100; Integer b = 100; a == b` is `true`, but `Integer c = 200; Integer d = 200; c == d` is `false`! Always use `.equals()` for object comparison.
- **JIT Compiler Optimization (Tiered Compilation)**:
  - C1 (Client Compiler): Fast startup with basic optimizations.
  - C2 (Server Compiler): Heavy profiling and aggressive optimizations (Method inlining, loop unrolling, escape analysis, lock coarsening/elision).
- **Escape Analysis**: If the JVM detects that an object created inside a method never escapes the method scope, it can eliminate heap allocation entirely and allocate the object's fields directly on the **Stack (Scalar Replacement)**!

---

## 3. 📊 Visual Architecture Diagram

```text
Java Compilation & Execution Pipeline:

   [ MyCode.java ] ──> javac Compiler ──> [ MyCode.class (Bytecode) ]
                                                    │
                                                    v
   ┌─────────────────────────────────────────────────────────────┐
   │                  Java Virtual Machine (JVM)                 │
   │  ┌──────────────────┐   ┌────────────────────────────────┐  │
   │  │   ClassLoader    │──>│      Bytecode Verifier         │  │
   │  └──────────────────┘   └────────────────────────────────┘  │
   │                                   │                         │
   │                                   v                         │
   │  ┌───────────────────────────────────────────────────────┐  │
   │  │                   Execution Engine                    │  │
   │  │  Interpreter ──> JIT Compiler (C1 / C2 Tiered)        │  │
   │  │  Hotspot profiling & Native Machine Code Generation   │  │
   │  └───────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘
                               │
                               v
               [ Host OS: Windows / Linux / macOS ]
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Define public demonstration class
public class JavaFundamentalsDemo {

    // Line 2: Helper class to demonstrate object mutation vs reference reassignment
    static class Account {
        // Line 3: Account balance field
        int balance;
        // Line 4: Constructor initializing balance
        Account(int balance) {
            this.balance = balance;
        }
    }

    // Line 5: Method attempting to reassign the reference
    public static void tryReassign(Account acc) {
        // Line 6: acc receives a COPY of the reference pointer
        // Line 7: Reassigning acc points the local copy to a brand-new object on the heap
        acc = new Account(99999);
        // Line 8: Caller's original reference remains completely untouched!
    }

    // Line 9: Method mutating the object via the copied reference
    public static void mutateAccount(Account acc) {
        // Line 10: Dereferencing the copied pointer to mutate internal state
        acc.balance += 500;
        // Line 11: Caller sees this mutation because both pointers pointed to the same heap object!
    }

    // Line 12: Main entry point for JVM execution
    public static void main(String[] args) {
        // Line 13: Primitive demonstration
        int primitiveVal = 42;
        // Line 14: Output primitive value
        System.out.println("Original Primitive: " + primitiveVal);

        // Line 15: Autoboxing: primitive int converted to Integer wrapper
        Integer boxedVal = primitiveVal;
        // Line 16: Unboxing: extracting primitive int from Integer wrapper
        int unboxedVal = boxedVal;

        // Line 17: Integer Cache (-128 to 127) trap demonstration
        Integer cacheA = 127;
        Integer cacheB = 127;
        // Line 18: true because both point to the cached Integer instance in memory
        System.out.println("127 == 127 check: " + (cacheA == cacheB)); // true

        Integer outOfCacheA = 128;
        Integer outOfCacheB = 128;
        // Line 19: false because values outside -128..127 allocate separate objects!
        System.out.println("128 == 128 check: " + (outOfCacheA == outOfCacheB)); // false
        // Line 20: Correct way: always compare wrapper objects with .equals()
        System.out.println("128 .equals check: " + outOfCacheA.equals(outOfCacheB)); // true

        // Line 21: Proof of Pass-by-Value in Java
        Account myAccount = new Account(1000);
        // Line 22: Attempt to reassign reference
        tryReassign(myAccount);
        // Line 23: Balance is still 1000, proving reassignment inside method failed
        System.out.println("Balance after tryReassign: " + myAccount.balance); // 1000

        // Line 24: Mutate account via copied reference
        mutateAccount(myAccount);
        // Line 25: Balance is now 1500, proving object mutation succeeded through copied reference
        System.out.println("Balance after mutateAccount: " + myAccount.balance); // 1500
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Is Java pass-by-value or pass-by-reference, and how does the Integer Cache affect equality checks?"
>
> **You:** "Java is strictly pass-by-value, without exception. When you pass an object, the value being passed is the 32-bit or 64-bit reference address pointing to that object on the heap. Therefore, you can mutate the object's internal fields through the copied reference, but reassigning the reference variable itself inside the method has zero effect on the caller. Regarding object comparisons, Java maintains an internal flyweight Integer Cache for values between -128 and 127. Comparing Integers with `==` checks reference equality, which accidentally succeeds within the cached range but silently fails for values >= 128. In enterprise applications, we must always enforce `.equals()` for object comparisons to avoid subtle data bugs."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A banking payment reconciliation pipeline processed transaction batches. During a quarterly audit, duplicate transaction alerts were missed when transaction amounts exceeded $127.00.
* **Task / Challenge:** Identify why transaction ID matching worked for transactions 1 through 127 but silently produced false negatives for transaction ID 128 and above.
* **Action Taken:** Inspected the reconciliation filter and found the line `if (currentTx.getId() == previousTx.getId())`. The `id` field was of type `java.lang.Long`. For values up to 127, the JVM cache returned identical references, masking the bug during basic unit tests. Replaced `==` with `.equals()` and added an automated ArchUnit static analysis rule banning `==` comparisons on wrapper classes.
* **Result & Business Impact:** Fixed the reconciliation logic, passing compliance audits across 4.5 million daily financial transactions.
"""

JAVA_STRINGS = """# Java String Memory Internals: String Constant Pool, Immutability & StringBuilder

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - `String` immutability: Ek baar patthar par lakeer khinch gayi toh wo badli nahi ja sakti (Agar "Hello" mein " World" jodoge, toh pura naya patthar banega, purana wahi pada rahega!).
> - String Constant Pool (SCP): Ek community library jahan agar "Jay" naam ki book pehle se hai, toh naya user wahi purani book use karega naya copy banane ke bajaye (Heap memory bachti hai!).
> - `StringBuilder`: Ek white-board jahan jab chahe text mita kar ya aage naya text jod kar likh sakte ho bina naya board khareede ($O(1)$ fast modification).
>
> **Real-World Analogy:** Currency notes vs a scratchpad. A $100 bill is immutable—you cannot erase the print and write $200 on it; the central bank must issue a new bill. A scratchpad (StringBuilder) allows you to continuously write and append notes on the same physical sheet of paper.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Why are Strings Immutable in Java?**:
  - **Security**: Sensitive parameters (passwords, database URLs, network sockets) cannot be altered maliciously after validation.
  - **Thread Safety**: Multiple threads can share a String instance safely without synchronization or locking.
  - **Caching**: The hash code (`hashCode`) is calculated once and cached, making Strings optimal dictionary keys in `HashMap`.
  - **String Constant Pool (SCP)**: Saves memory by sharing identical string literals across the entire JVM.
- **String Literals vs `new String()`**:
  - `String s1 = "Java";` -> Checks SCP. If present, returns reference. If absent, creates in SCP.
  - `String s2 = new String("Java");` -> Guarantees a brand-new object allocated in the normal **Heap**, outside the SCP (plus ensures "Java" is in SCP).
  - `s2.intern()` -> Moves/returns reference from the SCP.
- **`String` vs `StringBuilder` vs `StringBuffer`**:
  - `String`: Immutable. Concatenating in a loop (`s += i`) creates $N$ intermediate garbage objects, turning an $O(N)$ task into $O(N^2)$ memory churning!
  - `StringBuilder`: Mutable, unsynchronized, optimal for single-threaded string concatenation.
  - `StringBuffer`: Mutable, thread-safe with `synchronized` methods, but carries lock acquisition overhead.

### 🧓 What an Experienced Candidate Knows:
- **The `equals()` and `hashCode()` Contract**:
  1. If `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()` **MUST ALWAYS** be `true`.
  2. If `a.hashCode() == b.hashCode()`, `a.equals(b)` may be `true` or `false` (Hash collision).
  3. If you override `equals()`, you **MUST** override `hashCode()`. Failing to do so breaks `HashMap` and `HashSet` lookups!
- **Compact Strings (Java 9+)**:
  - Historically, Java used a 16-bit `char[]` (UTF-16) for every character, consuming 2 bytes per char even for ASCII.
  - Java 9 introduced Compact Strings: uses a `byte[]` with an encoding flag byte (`LATIN1` = 1 byte per char if ISO-8859-1; `UTF16` = 2 bytes per char otherwise), slashing heap consumption by **up to 50%** for text-heavy workloads.

---

## 3. 📊 Visual Architecture Diagram

```text
Heap Memory & String Constant Pool (SCP) Allocation:

   Code:
     String s1 = "Hello";
     String s2 = "Hello";
     String s3 = new String("Hello");

   JVM Heap Memory Layout:
   ┌─────────────────────────────────────────────────────────────┐
   │                         JVM HEAP                            │
   │                                                             │
   │  ┌───────────────────────────────────────────────────────┐  │
   │  │             String Constant Pool (SCP)                │  │
   │  │                                                       │  │
   │  │   "Hello" Object (ID: 0x100) <──┬── s1                │  │
   │  │                                 └── s2                │  │
   │  │                                      ^                │  │
   │  └──────────────────────────────────────┼────────────────┘  │
   │                                         │                   │
   │  Normal Heap Space:                     │                   │
   │  [ new String("Hello") (ID: 0x200) ] <──┴── s3              │
   │    └── references internal char[]/byte[] in SCP             │
   └─────────────────────────────────────────────────────────────┘

   Equality Checks:
     s1 == s2          ──> TRUE  (Same memory address 0x100)
     s1 == s3          ──> FALSE (0x100 != 0x200)
     s1.equals(s3)     ──> TRUE  (Same character content "Hello")
     s1 == s3.intern() ──> TRUE  (intern() points back to 0x100)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Define demonstration class
public class StringInternalsDemo {

    // Line 2: Main execution entry point
    public static void main(String[] args) {
        // Line 3: String literal: created in the String Constant Pool (SCP)
        String s1 = "CloudPlatform";
        // Line 4: Reuses the existing literal from the SCP (no new heap allocation)
        String s2 = "CloudPlatform";
        // Line 5: Explicitly creates a new object in general Heap memory
        String s3 = new String("CloudPlatform");

        // Line 6: Reference equality check (checks memory addresses)
        System.out.println("s1 == s2 (SCP literals): " + (s1 == s2)); // true
        // Line 7: Reference check between SCP and general heap
        System.out.println("s1 == s3 (Literal vs new String): " + (s1 == s3)); // false
        // Line 8: Value equality check (compares actual characters)
        System.out.println("s1.equals(s3): " + s1.equals(s3)); // true

        // Line 9: Calling intern() retrieves the SCP reference for s3
        String s4 = s3.intern();
        System.out.println("s1 == s3.intern(): " + (s1 == s4)); // true

        // Line 10: ANTI-PATTERN DEMONSTRATION: String concatenation in loops
        long startTime = System.currentTimeMillis();
        String badStr = "";
        for (int i = 0; i < 5000; i++) {
            // Line 11: Creates a new String object and copies previous characters on EVERY iteration!
            badStr += i;
        }
        long badDuration = System.currentTimeMillis() - startTime;
        System.out.println("String (+) loop duration: " + badDuration + " ms");

        // Line 12: BEST PRACTICE: StringBuilder for single-threaded appends
        startTime = System.currentTimeMillis();
        // Line 13: Pre-size capacity if estimated length is known to prevent buffer doubling
        StringBuilder goodBuilder = new StringBuilder(15000);
        for (int i = 0; i < 5000; i++) {
            // Line 14: Appends directly into internal resizing char/byte array in-place!
            goodBuilder.append(i);
        }
        String resultStr = goodBuilder.toString();
        long goodDuration = System.currentTimeMillis() - startTime;
        System.out.println("StringBuilder loop duration: " + goodDuration + " ms (100x faster!)");
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Why is String immutable in Java, and what happens when you concatenate strings using the `+` operator?"
>
> **You:** "Strings in Java are immutable for security, thread safety, hashcode caching, and to enable the String Constant Pool. In Java, string literals are pooled on the heap so identical values share memory. When you use the `+` operator outside loops, modern Java compilers optimize it into `StringBuilder` or `invokedynamic` with `StringConcatFactory`. However, inside loops, writing `s += item` creates a new `StringBuilder` and a brand-new `String` on every single iteration, leading to $O(N^2)$ memory churn and triggering frequent Garbage Collection stop-the-world pauses. In production systems, we always use `StringBuilder` with an initial capacity estimate for iterative string assembly."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An invoice generation service generated daily PDF export summaries for 100,000 corporate accounts. The batch job took 4.5 hours to finish, and the JVM frequently crashed with `java.lang.OutOfMemoryError: Java heap space`.
* **Task / Challenge:** Accelerate the invoice assembly job and prevent OutOfMemory crashes without scaling container RAM from 4GB to 16GB.
* **Action Taken:** Captured a Java flight recording (JFR) and heap dump using `jcmd`. Profiling showed 78% of all heap allocations were transient `char[]` and `String` instances generated by `reportHtml += formatRow(account)` inside nested loops. Refactored the invoice generator to stream writes into a pre-sized `StringBuilder` and flushed directly to the output stream.
* **Result & Business Impact:** Cut execution time from 4.5 hours down to 18 minutes (a $15\times$ speedup), and reduced heap memory consumption by 82%, completely eliminating OOM crashes.
"""

JAVA_OOP = """# Java OOP Foundations: Encapsulation, Inheritance, Polymorphism & Abstraction

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Encapsulation (Capsule): ATM machine ke andar ka cash box locked hai (Private data). Aap sirf buttons (Public methods) se paise nikaal sakte ho, direct cash box mein haath nahi daal sakte.
> - Inheritance: Beta apne pitaji se car aur zameen inherit karta hai (`extends`), bina wapas shuru se mehnat kiye.
> - Polymorphism (Bahu-roopi): Ek hi shakhs office mein Manager hai, ghar mein Pitaji hai, aur dukan pe Customer hai (Same method call `pay()`, different behavior depending on who executes it!).
> - Abstraction: Gaadi ka accelerator dabane par car tez bhagti hai. Driver ko engine ke andar ke fuel injectors aur piston ka physics janne ki zaroorat nahi hai (Complex mechanics hidden behind simple interface).
>
> **Real-World Analogy:** A universal TV remote control. The remote interface exposes buttons like `Power`, `VolumeUp`, and `Mute` (Abstraction). The internal circuitry is sealed in plastic (Encapsulation). You can point the remote at a Sony TV, an LG TV, or a Samsung soundbar; each device responds to `VolumeUp` appropriately according to its own driver (Polymorphism).

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Encapsulation**: Hide data using access modifiers (`private`, `default`, `protected`, `public`) and expose controlled access via getters and setters with validation.
- **Inheritance (`extends`, `implements`)**:
  - Java supports **Single Inheritance of Classes** (A class can extend only one class) to avoid the Diamond Problem.
  - Java supports **Multiple Inheritance of Type via Interfaces** (A class can implement multiple interfaces).
- **Polymorphism**:
  - **Compile-time Polymorphism (Method Overloading)**: Same method name, different parameter signature in the same class. Resolved at compile-time based on static reference type.
  - **Runtime Polymorphism (Method Overriding)**: Subclass provides a specific implementation of a method declared in its superclass. Resolved at runtime based on actual object instance in heap memory.
- **Abstraction**:
  - **Abstract Class**: Can have state (instance variables), constructors, abstract methods, and concrete methods. Used when classes share core identity and code.
  - **Interface**: A pure contract. Since Java 8, interfaces can have `default` and `static` methods. Since Java 9, interfaces can have `private` helper methods.

### 🧓 What an Experienced Candidate Knows:
- **Dynamic Method Dispatch & Virtual Method Table (vtable)**:
  - When you invoke `parentRef.execute()`, the JVM does NOT resolve this via compile-time pointer arithmetic.
  - Every class loaded into Metaspace has a **vtable** containing pointers to its virtual methods. At runtime, the JVM looks up the vtable of the **actual heap instance**, enabling dynamic dispatch in constant $O(1)$ time.
- **The `final` Keyword Mechanics**:
  - `final` variable: Value cannot be changed after initialization (constant). For objects, the reference cannot be rebound, but the object itself remains mutable!
  - `final` method: Cannot be overridden in subclasses (enables the JIT compiler to inline the method body directly, eliminating call stack overhead!).
  - `final` class: Cannot be extended (e.g. `java.lang.String`, `java.lang.Integer`).

---

## 3. 📊 Visual Architecture Diagram

```text
Runtime Polymorphism & Virtual Method Table (vtable) Dispatch:

   Code:
     PaymentProcessor processor = new UpiProcessor();
     processor.processPayment(500);

   Memory Resolution:
     Stack Reference: [ processor (Type: PaymentProcessor) ]
            │
            v (Points to Heap Instance)
     Heap Object: [ UpiProcessor Instance ]
            │
            v (Points to Class Metadata in Metaspace)
     [ Metaspace: UpiProcessor vtable ]
     ┌─────────────────────────────────────────────────────────────┐
     │ Method Index 0: Object.toString()       ──> Object implementation
     │ Method Index 1: PaymentProcessor.init() ──> Base implementation
     │ Method Index 2: processPayment()        ──> UpiProcessor.processPayment() [OVERRIDDEN!]
     └─────────────────────────────────────────────────────────────┘
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Define abstract base class representing a Payment Gateway
abstract class PaymentGateway {
    // Line 2: Encapsulated private field for gateway transaction audit ID
    private final String gatewayId;

    // Line 3: Constructor initializing common base state
    public PaymentGateway(String gatewayId) {
        this.gatewayId = gatewayId;
    }

    // Line 4: Getter providing read-only encapsulated access
    public String getGatewayId() {
        return this.gatewayId;
    }

    // Line 5: Abstract method: forces subclasses to provide customized processing logic
    public abstract boolean process(double amount);

    // Line 6: Concrete template method shared across all subclasses
    public void executeWithAudit(double amount) {
        System.out.println("[" + gatewayId + "] Auditing payment request: $" + amount);
        // Line 7: Dynamic method dispatch invokes specific subclass implementation!
        boolean success = process(amount);
        System.out.println("[" + gatewayId + "] Payment status: " + (success ? "APPROVED" : "REJECTED"));
    }
}

// Line 8: CreditCardGateway subclass extending base gateway
class CreditCardGateway extends PaymentGateway {
    public CreditCardGateway() {
        super("CREDIT_CARD_V2");
    }

    // Line 9: Override annotation ensures compile-time check against signature mistakes
    @Override
    public boolean process(double amount) {
        System.out.println("  -> Validating CVV and charging credit line for $" + amount);
        return amount <= 5000.0; // Credit limit rule
    }
}

// Line 10: UpiGateway subclass extending base gateway
class UpiGateway extends PaymentGateway {
    public UpiGateway() {
        super("UPI_FAST_PAY");
    }

    @Override
    public boolean process(double amount) {
        System.out.println("  -> Verifying Virtual Payment Address (VPA) and MPIN for $" + amount);
        return amount <= 1000.0; // UPI daily transaction limit rule
    }
}

// Line 11: Main class demonstrating polymorphism
public class OopPrinciplesDemo {
    public static void main(String[] args) {
        // Line 12: Polymorphism in action: Base reference pointing to CreditCard instance
        PaymentGateway gateway1 = new CreditCardGateway();
        // Line 13: Base reference pointing to UPI instance
        PaymentGateway gateway2 = new UpiGateway();

        // Line 14: Invoking identical method call on gateway1 triggers CreditCard logic
        gateway1.executeWithAudit(2500.0);

        // Line 15: Invoking identical method call on gateway2 triggers UPI logic
        gateway2.executeWithAudit(2500.0);
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the difference between method overloading and overriding, and how does Java achieve runtime polymorphism?"
>
> **You:** "Method overloading represents compile-time static polymorphism, where multiple methods share the same name with different parameter counts or types; the compiler resolves the target method based on static reference types at compile time. In contrast, method overriding represents runtime dynamic polymorphism, where a subclass provides its own implementation of an inherited method with an identical signature. At runtime, the JVM uses dynamic method dispatch: it inspects the actual object instance on the heap and consults the class's Virtual Method Table (vtable) in Metaspace to invoke the overridden method. This is the foundation of clean, extensible Object-Oriented Architecture."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A multi-tenant SaaS application handled payments via hardcoded `if-else` blocks (`if (provider.equals("STRIPE")) ... else if (provider.equals("PAYPAL"))`). Every time a new payment provider was added, developers had to modify 8 different service files, resulting in frequent regression bugs and broken checkout flows.
* **Task / Challenge:** Redesign the payment architecture to adhere to the Open/Closed Principle (open for extension, closed for modification) and prevent regressions.
* **Action Taken:** Replaced the conditional branching with a polymorphic Factory and Strategy Pattern. Defined a common `PaymentGateway` interface and implemented tenant-specific gateway classes. Spring's Dependency Injection was configured to auto-register all gateway implementations into a `Map<String, PaymentGateway>` at startup.
* **Result & Business Impact:** Reduced the code footprint by 60%, eliminated payment regression defects entirely, and reduced the onboarding time for new payment partners from 3 weeks to 2 days.
"""

JAVA_COLLECTIONS = """# Java Collections Framework (JCF) Deep Dive: List, Set, Queue & HashMap Architecture

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - `ArrayList`: Cinema hall ki seat row jisme sab saath baithe hain ($O(1)$ direct index access, par beech mein naya aadmi ghusana ho toh sabko shift hona padta hai).
> - `LinkedList`: Train ke dibbe jo ek doosre se hook se jude hain (Naya dibba jodna aasan hai, par 50th dibbe tak pahunchne ke liye 1st dibbe se chalke jana padega).
> - `HashSet`: Ek club jisme security guard check karta hai ki aapka fingerprint pehle se registered hai ya nahi (Unique items, no duplicates, $O(1)$ instant check).
> - `HashMap`: Hotel ki reception jahan Room Key (Key) dekar saman (Value) mil jata hai. Agar do logon ki key ek hi pigeonhole mein chali jaye (Collision), toh reception wahan choti list ya tree bana leti hai!
>
> **Real-World Analogy:** An unrolled measuring tape (`ArrayList`) vs a scavenger hunt list (`LinkedList`). With the measuring tape, you can jump directly to centimeter mark 42 instantly. With a scavenger hunt, clue 1 tells you where clue 2 is, clue 2 tells you where clue 3 is; you cannot jump to clue 10 without visiting all prior clues.

---

## 2. 📌 Core Mechanics & Time Complexities (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **`List` Interface (Ordered, Allows Duplicates)**:
  - `ArrayList`: Backed by a dynamic resizable array. Default initial capacity is 10. When full, it grows by **50%** ($1.5\times$ growth: `newCapacity = oldCapacity + (oldCapacity >> 1)`). $O(1)$ get/set; $O(N)$ insertion/removal in the middle.
  - `LinkedList`: Doubly linked list of `Node` objects (`item`, `prev`, `next`). $O(1)$ add/remove at ends; $O(N)$ traversal. Consumes significantly more memory due to node pointer overhead.
- **`Set` Interface (Unique Elements Only)**:
  - `HashSet`: Backed internally by a `HashMap` where the element is the Key, and a dummy `Object` is the Value. $O(1)$ add/remove/contains. Unordered.
  - `LinkedHashSet`: Maintains a doubly-linked list through the hash buckets, preserving **insertion order**.
  - `TreeSet`: Backed by a Red-Black Tree. Elements stored in sorted order. $O(\log N)$ add/remove/contains.
- **`Queue` & `Deque`**:
  - `ArrayDeque`: Resizing circular array. Faster than `LinkedList` for stacks and queues; does not permit `null`.
  - `PriorityQueue`: Backed by a binary min-heap. Elements ordered by natural ordering or custom `Comparator`. $O(\log N)$ enqueue/dequeue.

### 🧓 What an Experienced Candidate Knows:
- **`HashMap` Internal Architecture (Java 8+)**:
  1. Internal storage is an array of `Node<K,V>[] table`.
  2. Hashing algorithm mixes high and low bits to minimize collisions: `hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16)`.
  3. Bucket index calculated via bitwise AND: `index = (n - 1) & hash` (which requires table capacity $n$ to always be a power of 2!).
  4. Default capacity = 16; Load Factor = 0.75. When size exceeds `16 * 0.75 = 12`, the array doubles to 32.
  5. **Treeification**: When collisions in a single bucket reach **8 elements** AND total table capacity is at least **64**, the bucket converts from a singly linked list ($O(N)$) into a balanced **Red-Black Tree** (`TreeNode`), slashing worst-case lookup from $O(N)$ to $O(\log N)$ to protect against HashDoS attacks!
- **Fail-Fast vs Fail-Safe Iterators**:
  - Fail-Fast (`ArrayList`, `HashMap`): Checks `modCount`. If modified during iteration without `iterator.remove()`, throws `ConcurrentModificationException`.
  - Fail-Safe / Concurrent (`CopyOnWriteArrayList`, `ConcurrentHashMap`): Operates on a snapshot or segmented bucket locks, never throwing `ConcurrentModificationException`.

---

## 3. 📊 Visual Architecture Diagram

```text
Java 8+ HashMap Internal Memory & Treeification:

   table = Node<K,V>[16]
   Index 0:  null
   Index 1:  [ Node: Key="A" ] ──> [ Node: Key="B" ] ──> null (Linked List, < 8 elements)
   Index 2:  null
   ...
   Index 7:  [ TreeNode: Root ]  <── Treeified! (>= 8 colliding keys in same bucket)
               ├── Left:  [ TreeNode ]
               └── Right: [ TreeNode ] (Red-Black Tree: O(log N) lookup instead of O(N)!)
   ...
   Index 15: null
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Import required Java Collections Framework classes
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

// Line 2: Demonstration class for collections mechanics
public class CollectionsDeepDiveDemo {

    // Line 3: Main execution method
    public static void main(String[] args) {
        // Line 4: ArrayList demonstrating capacity and fast access
        List<String> names = new ArrayList<>(20); // Pre-size capacity to prevent reallocations
        names.add("Jay");
        names.add("Prakash");
        names.add("Alice");
        // Line 5: Fast O(1) random access via index
        System.out.println("Second element: " + names.get(1)); // 'Prakash'

        // Line 6: DEMONSTRATING FAIL-FAST ITERATOR & ConcurrentModificationException
        try {
            // Line 7: Standard foreach loop uses iterator under the hood
            for (String name : names) {
                if (name.equals("Alice")) {
                    // Line 8: DIRECT MODIFICATION TRAP: Modifies list while iterating!
                    names.remove(name); // Throws ConcurrentModificationException!
                }
            }
        } catch (Exception e) {
            // Line 9: Catch and explain the exception
            System.out.println("Caught Expected Fail-Fast Exception: " + e.getClass().getSimpleName());
        }

        // Line 10: THE CORRECT WAY: Safe removal via Iterator
        Iterator<String> safeIterator = names.iterator();
        while (safeIterator.hasNext()) {
            String name = safeIterator.next();
            if (name.equals("Alice")) {
                // Line 11: Iterator's own remove() updates modCount synchronously, preventing exceptions
                safeIterator.remove();
            }
        }
        System.out.println("Names after safe iterator removal: " + names);

        // Line 12: HashMap frequency counter using modern getOrDefault / compute
        Map<String, Integer> wordFrequencies = new HashMap<>();
        String[] words = {"apple", "banana", "apple", "cherry", "banana", "apple"};
        for (String word : words) {
            // Line 13: Increments count atomically in map
            wordFrequencies.put(word, wordFrequencies.getOrDefault(word, 0) + 1);
        }
        System.out.println("Word Frequencies: " + wordFrequencies);

        // Line 14: PriorityQueue Min-Heap demonstration
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.add(45);
        minHeap.add(10);
        minHeap.add(30);
        // Line 15: poll() extracts minimum element in O(log N)
        System.out.println("Extracted Minimum from Heap: " + minHeap.poll()); // 10
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How does `HashMap` handle hash collisions, and what changed in Java 8?"
>
> **You:** "In Java, `HashMap` uses an array of buckets to store key-value pairs, computing the bucket index via `(n - 1) & hash`. When multiple keys map to the same bucket index, a hash collision occurs. Prior to Java 8, collisions were resolved strictly using singly linked lists, which caused lookup time to degrade to $O(N)$ in worst-case collision scenarios. In Java 8, Oracle introduced bucket treeification: when a bucket accumulates 8 or more colliding entries and the total map capacity is at least 64, the linked list converts into a self-balancing Red-Black Tree. This guarantees a worst-case search time of $O(\log N)$ instead of $O(N)$, mitigating Denial-of-Service collision vulnerabilities."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An e-commerce inventory sync service experienced intermittent 100% CPU lockups during high-traffic flash sale events. Thread dumps revealed multiple worker threads were stuck in an infinite loop inside `HashMap.get()` during concurrent rehashing.
* **Task / Challenge:** Eliminate the high-CPU thread hang without sacrificing read and write throughput.
* **Action Taken:** Diagnosed that a standard, non-thread-safe `HashMap` was being shared across multiple worker threads. When concurrent writes triggered `resize()`, the circular linked list pointer corruption caused infinite loops. Replaced the `HashMap` with `ConcurrentHashMap`, which uses lock-free CAS (Compare-And-Swap) for empty buckets and fine-grained per-bucket node locking.
* **Result & Business Impact:** Completely eradicated CPU lockup crashes, allowing the inventory service to process 65,000 concurrent inventory updates per second with zero thread contention.
"""

JAVA_GENERICS = """# Java Generics, Wildcards & Type Erasure: The PECS Principle

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Generics bina: Ek aisi delivery van jisme kisi bhi tarah ka saman (Fruits, Chemical, Electronics) bina label ke fenk diya jata hai. Jab driver delivery karta hai, toh usko guess karna padta hai aur galat saman nikalne par blast (ClassCastException) ho jata hai!
> - Generics ke saath: Har dabbe par strict label laga hai: `List<Apple>`. Isme koi galti se `Orange` nahi daal sakta (Compile-time par hi error pakda jayega).
> - Type Erasure: Java ka compiler bahut chalak hai. Wo code check karte waqt strict checking karta hai, lekin compiled `.class` bytecode banate waqt saare labels mita kar purana `Object` bana deta hai taaki purane Java version ke saath compatibility bani rahe!
>
> **Real-World Analogy:** A pill organizer with compartments labeled Monday through Sunday. You can only put pills into their designated compartments, preventing you from taking the wrong medication. Once swallowed, your stomach absorbs them without caring about the plastic compartment labels (Type Erasure).

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Why Generics?**:
  1. Strong compile-time type checking (Catches bugs during compilation rather than crashing in production with `ClassCastException`).
  2. Elimination of manual type casting: writing `String s = (String) list.get(0)` is no longer necessary.
  3. Reusable, type-safe algorithms.
- **Generic Syntax**:
  - Generic Classes: `class Box<T> { private T value; }`
  - Generic Methods: `public <E> void printArray(E[] elements)`
  - Common naming conventions: `T` (Type), `E` (Element), `K` (Key), `V` (Value), `N` (Number).

### 🧓 What an Experienced Candidate Knows:
- **The PECS Principle: Producer Extends, Consumer Super**:
  - **`? extends T` (Upper Bounded Wildcard)**: Used when the collection is a **Producer** (You are reading data *from* the collection). You can read `T`, but you **CANNOT add** elements into it (except `null`) because the compiler doesn't know the exact subtype!
  - **`? super T` (Lower Bounded Wildcard)**: Used when the collection is a **Consumer** (You are writing data *into* the collection). You can safely add `T` and its subclasses, but reading from it only yields `Object`.
- **Type Erasure Internals**:
  - Generics exist **only at compile time**. The Java compiler replaces all type parameters with their bounds (or `Object` if unbounded) and inserts explicit casts in the bytecode.
  - Consequences of Type Erasure:
    - You cannot do `new T()`.
    - You cannot create generic arrays: `new T[10]` is illegal.
    - You cannot use `instanceof List<String>` at runtime (you can only check `instanceof List<?>`).
    - Primitive types cannot be used as type arguments (`List<int>` is invalid; you must use `List<Integer>`).
  - **Bridge Methods**: The compiler generates synthetic bridge methods in bytecode to preserve polymorphic method overriding when type erasure alters method signatures.

---

## 3. 📊 Visual Architecture Diagram

```text
The PECS Principle (Producer Extends, Consumer Super):

          [ Number (Base Class) ]
                    ▲
                    │
         ┌──────────┴──────────┐
         │                     │
    [ Integer ]           [ Double ]

   1. Producer Extends (? extends Number):
      List<? extends Number> producer = new ArrayList<Integer>();
      Number n = producer.get(0);  ──> SAFE! (Produces Numbers)
      producer.add(10);            ──> COMPILE ERROR! (Cannot guarantee subtype)

   2. Consumer Super (? super Integer):
      List<? super Integer> consumer = new ArrayList<Number>();
      consumer.add(10);            ──> SAFE! (Consumes Integers)
      Object obj = consumer.get(0);──> Only returns Object (Cannot guarantee Integer)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Import required collections utilities
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

// Line 2: Demonstration class for Generics and PECS
public class GenericsPecsDemo {

    // Line 3: Producer Extends: Reads numbers from source list and computes their sum
    // Line 4: List<? extends Number> PRODUCES data; read-only operations on Number
    public static double sumOfList(List<? extends Number> list) {
        double sum = 0.0;
        // Line 5: Safe to read as Number because all elements are guaranteed to be at least Number
        for (Number n : list) {
            sum += n.doubleValue();
        }
        // Line 6: list.add(10); // COMPILE ERROR! Cannot add to <? extends T>
        return sum;
    }

    // Line 7: Consumer Super: Adds integers into a destination list
    // Line 8: List<? super Integer> CONSUMES data; write operations for Integer
    public static void addIntegers(List<? super Integer> list) {
        // Line 9: Safe to add Integer because the list is at least Integer or an ancestor (Number, Object)
        list.add(100);
        list.add(200);
        list.add(300);
        // Line 10: Reading from <? super T> only guarantees Object
        Object item = list.get(0);
    }

    // Line 11: Generic Method with Type Parameter Bounds
    public static <T extends Comparable<T>> T findMax(T a, T b) {
        // Line 12: compareTo is guaranteed to exist because T extends Comparable<T>
        return (a.compareTo(b) > 0) ? a : b;
    }

    // Line 13: Main execution method
    public static void main(String[] args) {
        // Line 14: Test sumOfList with Integer list
        List<Integer> intList = Arrays.asList(1, 2, 3, 4, 5);
        System.out.println("Sum of Integers: " + sumOfList(intList)); // 15.0

        // Line 15: Test sumOfList with Double list (demonstrating covariance)
        List<Double> doubleList = Arrays.asList(1.5, 2.5, 3.5);
        System.out.println("Sum of Doubles: " + sumOfList(doubleList)); // 7.5

        // Line 16: Test addIntegers with a Number list (demonstrating contravariance)
        List<Number> numList = new ArrayList<>();
        addIntegers(numList);
        System.out.println("Consumer list after adding: " + numList); // [100, 200, 300]

        // Line 17: Test generic findMax method
        String maxString = findMax("Apple", "Zebra");
        System.out.println("Max String: " + maxString); // 'Zebra'
        Integer maxInt = findMax(50, 99);
        System.out.println("Max Integer: " + maxInt);   // 99
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the PECS rule in Java Generics, and how does Type Erasure impact runtime execution?"
>
> **You:** "PECS stands for 'Producer Extends, Consumer Super'. We use `? extends T` when a collection acts as a producer and we only read elements from it, because any element is guaranteed to be a subtype of `T`. Conversely, we use `? super T` when a collection acts as a consumer and we write elements into it, because the collection is guaranteed to accept `T` and its subtypes. Type erasure is how Java enforces backward compatibility: the compiler verifies all generic types at compile time, but then erases them from bytecode, replacing them with raw `Object` or their upper bound and inserting casts. This is why generic type arguments cannot be instantiated with `new T()` or inspected via `instanceof` at runtime."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An open-source event-bus library had a method `public void registerListeners(List<EventListener> listeners)`. Client services attempted to pass `List<AuditLogListener>` (which implemented `EventListener`), but Java compilation failed with type mismatch errors.
* **Task / Challenge:** Enable the event-bus to accept lists of any subclass of `EventListener` while preventing compile-time type errors across 200 microservices.
* **Action Taken:** Identified that Java generics are invariant by default (`List<Sub>` is NOT a subtype of `List<Super>`). Refactored the method signature to apply the Producer Extends rule: `public void registerListeners(List<? extends EventListener> listeners)`.
* **Result & Business Impact:** Resolved the API rigidity, allowing all client services to pass subtype collections natively without ugly, unsafe manual type casting.
"""

JAVA_EXCEPTIONS = """# Java Exception Handling: Hierarchy, Checked vs Unchecked & Try-With-Resources

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - `Throwable`: Har museebat ka dada (Grandparent class).
> - `Error`: Ghar mein bhukamp ya aag lag jana (`OutOfMemoryError`)—ispe aap kuch nahi kar sakte, building se bahar bhagna padega (JVM crashes, application cannot recover).
> - `Checked Exception`: Ghar se nikalte waqt mummy ka bolna ki "Chhata leke jao, baarish ho sakti hai" (`IOException`). Compiler aapko ghar se bahar nikalne hi nahi dega jab tak aap chhata (try-catch ya throws) na le lo!
> - `Unchecked Exception (RuntimeException)`: Chalte chalte sadak par kela ke chhilke par fisal jana (`NullPointerException`). Ye programmer ki laparwahi ki wajah se hota hai, compiler pehle se warn nahi kar sakta.
> - `try-with-resources`: Ek aisi modern tap (nal) jo haath dhone ke baad apne aap band ho jati hai, chahe aap nal band karna bhool jao!
>
> **Real-World Analogy:** An airline flight check-in. A Checked Exception is forgetting your passport—the gate agent checks it before you board and won't let you proceed without resolving it. An Unchecked Exception is a passenger suddenly fainting mid-flight due to personal negligence. An Error is the airplane's engine falling off.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Exception Hierarchy**:
  - `java.lang.Throwable`
    - `java.lang.Error`: Serious system issues (`OutOfMemoryError`, `StackOverflowError`). Applications should **never** catch `Error`.
    - `java.lang.Exception`:
      - **Checked Exceptions**: Subclasses of `Exception` (excluding `RuntimeException`). Enforced at compile-time (`IOException`, `SQLException`, `ClassNotFoundException`). Must be handled via `try-catch` or declared via `throws`.
      - **Unchecked Exceptions (RuntimeExceptions)**: Subclasses of `RuntimeException` (`NullPointerException`, `IllegalArgumentException`, `IndexOutOfBoundsException`, `ArithmeticException`). Caused by programming logic flaws. Compiler does not force handling.
- **`try-catch-finally` Execution Guarantee**:
  - Code inside `finally` block **ALWAYS executes**, even if an exception is thrown, caught, or if the `try` block executes a `return` statement!
  - **Only Exception**: `finally` does NOT execute if `System.exit(0)` is called or JVM crashes.
- **Java 7+ `try-with-resources`**:
  - Automatically closes any resource implementing `java.lang.AutoCloseable` or `java.io.Closeable` when leaving the block.
  - Eliminates boilerplate `finally { if (res != null) res.close(); }` code.

### 🧓 What an Experienced Candidate Knows:
- **Suppressed Exceptions**:
  - If an exception is thrown inside the `try` block AND another exception is thrown when closing the resource in `close()`, the `close()` exception is **suppressed** so the primary root-cause exception is not lost. You can inspect them via `e.getSuppressed()`.
- **Exception Anti-Patterns in Production**:
  1. **Swallowing Exceptions**: `catch (Exception e) {}` (Silently hides production bugs).
  2. **Catching Generic `Throwable` or `Exception`**: Catches unintended runtime errors or errors that should terminate the process.
  3. **Destructive Wrapping**: Re-throwing `throw new RuntimeException("error")` without passing the original cause `throw new RuntimeException("error", originalException)` destroys the original stack trace!

---

## 3. 📊 Visual Architecture Diagram

```text
Java Throwable Class Hierarchy:

                        ┌───────────────────────┐
                        │ java.lang.Throwable   │
                        └───────────┬───────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               │                                         │
    ┌──────────▼───────────┐                  ┌──────────▼───────────┐
    │   java.lang.Error    │                  │ java.lang.Exception  │
    │ (Fatal: OOM, Stack)  │                  └──────────┬───────────┘
    └──────────────────────┘                             │
                                        ┌────────────────┴────────────────┐
                                        │                                 │
                             ┌──────────▼───────────┐          ┌──────────▼───────────┐
                             │ Checked Exceptions   │          │  RuntimeException    │
                             │ (IOException, SQL)   │          │ (Unchecked: NPE, IAE)│
                             │ [Compile-Time Check] │          │  [Runtime Bug Check] │
                             └──────────────────────┘          └──────────────────────┘
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Define a custom AutoCloseable database connection simulation
class DatabaseConnection implements AutoCloseable {
    private final String dbName;

    public DatabaseConnection(String dbName) {
        this.dbName = dbName;
        System.out.println("[" + dbName + "] Connection established.");
    }

    public void executeQuery(String sql) throws Exception {
        System.out.println("[" + dbName + "] Executing query: " + sql);
        // Line 2: Simulate query failure
        if (sql.contains("FAIL")) {
            throw new Exception("Query syntax error in SQL execution");
        }
    }

    // Line 3: AutoCloseable contract method: guaranteed to execute automatically
    @Override
    public void close() throws Exception {
        System.out.println("[" + dbName + "] Connection closed cleanly.");
    }
}

// Line 4: Custom Business Exception preserving the causal chain
class OrderProcessingException extends RuntimeException {
    // Line 5: Constructor accepting message and original root-cause throwable
    public OrderProcessingException(String message, Throwable cause) {
        super(message, cause); // Passes cause to superclass to preserve complete stack trace!
    }
}

// Line 5: Main demonstration class
public class ExceptionHandlingDemo {

    public static void processOrder(String orderId) {
        // Line 6: try-with-resources: resource is automatically closed at the end of this block
        try (DatabaseConnection conn = new DatabaseConnection("Orders-DB")) {
            // Line 7: Execute query
            conn.executeQuery("SELECT * FROM orders WHERE id = '" + orderId + "'");
        } catch (Exception e) {
            // Line 8: Wrap checked exception into business exception while preserving root cause
            throw new OrderProcessingException("Failed to process order " + orderId, e);
        }
    }

    public static void main(String[] args) {
        // Line 9: Demonstrate normal execution
        System.out.println("--- Successful Execution ---");
        processOrder("ORD_1001");

        // Line 10: Demonstrate error recovery and causal chain
        System.out.println("\n--- Exception Handling & Stack Trace Preservation ---");
        try {
            processOrder("FAIL_ORD_9999");
        } catch (OrderProcessingException opex) {
            System.out.println("Caught High-Level Exception: " + opex.getMessage());
            // Line 11: Inspect root cause
            System.out.println("Underlying Root Cause: " + opex.getCause().getMessage());
        }
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the difference between Checked and Unchecked exceptions, and why is `try-with-resources` preferred over `finally`?"
>
> **You:** "Checked exceptions inherit directly from `Exception` and represent anticipated, recoverable conditions like network drops or file missing; the Java compiler forces developers to either catch them or declare them using `throws`. Unchecked exceptions extend `RuntimeException` and indicate programming errors like `NullPointerException` or invalid arguments, which should be resolved by code validation rather than catch blocks. `try-with-resources` is preferred over traditional `finally` blocks because it ensures deterministic closure of `AutoCloseable` resources, drastically reduces boilerplate, and cleanly manages suppressed exceptions so secondary exceptions thrown during resource closing do not obscure the primary application failure."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A Spring Boot banking API began experiencing severe connection pool exhaustion (`HikariCP: Connection is not available, request timed out after 30000ms`) during peak trading hours, degrading service availability to 85%.
* **Task / Challenge:** Identify and resolve the database connection leak without increasing pool limits or restarting servers.
* **Action Taken:** Thread dump and code analysis revealed that a legacy reporting method opened raw JDBC connections inside a traditional `try-catch` block. When an unexpected `NullPointerException` occurred before the `finally` block's null check, the connection was never closed. Refactored all raw database and stream calls to use Java 7 `try-with-resources`.
* **Result & Business Impact:** Permanently resolved the connection leak, restoring 99.99% API availability and stabilizing HikariCP active connection counts at under 20% capacity.
"""

JAVA_MODERN_FEATURES = """# Modern Java Features (Java 8 to 21): Lambdas, Streams, Records, Sealed Classes & Pattern Matching

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Lambda Expression: Anonymous function—ek chota sa kaam karne ke liye pura class aur method ka tam-jham likhne ke bajaye ek line ka arrow function `(x) -> x * 2` likh dena.
> - Streams API: Factory ki assembly line—ek taraf se raw material (data) ghusta hai, beech mein conveyor belt pe cleaning (`filter`), painting (`map`), aur packaging (`collect`) hoti hai, aur aakhri mein final product bahar nikalta hai!
> - Records (Java 14-17): Ek transparent ID card—sirf data rakhne ke liye 100 line ka boilerplate (getter, setter, constructor, equals, hashCode) likhne ki zaroorat nahi, ek line mein `record User(String name, int age) {}` likho aur sab automatic mil jata hai!
> - Sealed Classes (Java 17): Ek VIP list—aap define karte ho ki meri class ko sirf ye specific 2 classes hi extend kar sakti hain, koi teesri anjaan class extend nahi kar sakti!
>
> **Real-World Analogy:** An automated car manufacturing plant. A Stream is the assembly line where each chassis moves smoothly through workstations (filtering defective chassis, attaching engines, spray-painting colors) without creating intermediate parking lots for half-finished cars.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Lambdas & Functional Interfaces (`@FunctionalInterface`)**:
  - An interface with **exactly one abstract method**.
  - Built-in Functional Interfaces:
    - `Predicate<T>`: `boolean test(T t)` (Used for filtering).
    - `Function<T, R>`: `R apply(T t)` (Used for transformation).
    - `Consumer<T>`: `void accept(T t)` (Used for side effects).
    - `Supplier<T>`: `T get()` (Used for deferred generation).
- **Stream API**:
  - **Intermediate Operations (Lazy evaluation)**: `filter()`, `map()`, `sorted()`, `distinct()`. They do NOT execute until a terminal operation is called!
  - **Terminal Operations (Eager execution)**: `collect()`, `forEach()`, `reduce()`, `count()`, `anyMatch()`.
- **`Optional<T>`**: Container to represent value presence or absence, preventing `NullPointerException`. Never call `.get()` directly without checking; use `.orElseGet()` or `.map()`.

### 🧓 What an Experienced Candidate Knows:
- **Records Internals (Java 16+)**:
  - A `record` is implicitly `final` and extends `java.lang.Record`.
  - Automatically generates immutable private final fields, canonical constructor, accessors (without `get` prefix: `user.name()`), `equals()`, `hashCode()`, and `toString()`.
- **Sealed Classes & Interfaces (Java 17+)**:
  - Declared with `sealed class Shape permits Circle, Rectangle`.
  - Subclasses must be explicitly marked as `final`, `sealed`, or `non-sealed`.
  - Enables **Exhaustive Pattern Matching** in `switch` statements without needing a dummy `default` branch!
- **Pattern Matching for `switch` & `instanceof` (Java 21)**:
  - Eliminates ugly casting: `if (obj instanceof String s)` binds variable `s` directly.
  - Switch pattern matching supports guarded patterns using `when`: `case String s when s.length() > 5`.

---

## 3. 📊 Visual Architecture Diagram

```text
Java Stream Pipeline & Lazy Evaluation:

   Source Collection: [ 10, 15, 20, 25, 30 ]
           │
           v (Intermediate Operation 1: Lazy)
   [ .filter(n -> n > 15) ] ──> Only allows 20, 25, 30 through
           │
           v (Intermediate Operation 2: Lazy)
   [ .map(n -> n * 2) ]     ──> Transforms to 40, 50, 60
           │
           v (Terminal Operation: Eager Execution Trigger)
   [ .collect(Collectors.toList()) ] ──> Output: List [ 40, 50, 60 ]
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```java
// Line 1: Import modern functional utilities and collections
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

// Line 2: Define an immutable Record (Java 16+) representing a customer transaction
record Transaction(String id, double amount, String currency, String status) {
    // Line 3: Compact constructor for input validation
    public Transaction {
        if (amount < 0) {
            throw new IllegalArgumentException("Transaction amount cannot be negative");
        }
    }
}

// Line 4: Define a Sealed Interface (Java 17+)
sealed interface PaymentNotification permits EmailAlert, SmsAlert {}

// Line 5: Permitted record implementing sealed interface
record EmailAlert(String emailAddress, String message) implements PaymentNotification {}
// Line 6: Permitted record implementing sealed interface
record SmsAlert(String phoneNumber, String message) implements PaymentNotification {}

// Line 7: Main class demonstrating modern Java features
public class ModernJavaFeaturesDemo {

    // Line 8: Pattern Matching for switch (Java 21) on Sealed Types
    public static void dispatchNotification(PaymentNotification notification) {
        // Line 9: Exhaustive switch without needing default branch because PaymentNotification is sealed!
        String logMessage = switch (notification) {
            case EmailAlert email when email.emailAddress().endsWith("@vip.com") ->
                "Sending PRIORITY email to: " + email.emailAddress();
            case EmailAlert email ->
                "Sending standard email to: " + email.emailAddress();
            case SmsAlert sms ->
                "Sending SMS text to: " + sms.phoneNumber();
        };
        System.out.println(logMessage);
    }

    public static void main(String[] args) {
        // Line 10: Create sample transaction records
        List<Transaction> transactions = Arrays.asList(
            new Transaction("TXN_1", 250.0, "USD", "COMPLETED"),
            new Transaction("TXN_2", 50.0,  "EUR", "FAILED"),
            new Transaction("TXN_3", 1200.0, "USD", "COMPLETED"),
            new Transaction("TXN_4", 800.0, "USD", "COMPLETED"),
            new Transaction("TXN_5", 300.0, "EUR", "COMPLETED")
        );

        // Line 11: Stream API pipeline: Filter, group by currency, and calculate total sum
        Map<String, Double> totalCompletedByCurrency = transactions.stream()
            // Line 12: Filter intermediate step: only completed transactions
            .filter(tx -> "COMPLETED".equals(tx.status()))
            // Line 13: Terminal operation: group by currency and sum transaction amounts
            .collect(Collectors.groupingBy(
                Transaction::currency,
                Collectors.summingDouble(Transaction::amount)
            ));

        System.out.println("Total Completed by Currency: " + totalCompletedByCurrency);
        // Output: {EUR=300.0, USD=2250.0}

        // Line 14: Test pattern matching with notifications
        dispatchNotification(new EmailAlert("ceo@vip.com", "Large transaction executed"));
        dispatchNotification(new SmsAlert("+1234567890", "OTP verification code: 4492"));
    }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do Records, Sealed Classes, and Pattern Matching enhance Java application architecture?"
>
> **You:** "Modern Java from version 17 to 21 transforms domain modeling through data-oriented programming. Records eliminate hundreds of lines of boilerplate for immutable data carriers while guaranteeing correct `equals`, `hashCode`, and thread safety. Sealed classes and interfaces give developers precise control over inheritance by restricting subclasses to an explicit permitted set. When combined with Java 21 Pattern Matching for `switch`, the compiler can perform exhaustive pattern checking without requiring fragile `default` branches. If someone adds a new permitted subclass in the future, the compiler immediately flags every unhandled `switch` statement across the codebase, eliminating runtime type bugs."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A risk evaluation service parsed heterogeneous financial events using legacy `instanceof` cascades and explicit casting across 12 nested event classes. When a junior developer added a new `CryptoTransferEvent` class, three un-updated evaluation methods silently defaulted to the `else` branch, letting high-risk transfers bypass fraud checks.
* **Task / Challenge:** Re-architect the event hierarchy to enforce compile-time exhaustiveness checks across all fraud evaluation handlers.
* **Action Taken:** Converted the event classes into Java 17 `sealed interface FinancialEvent` with immutable `record` subclasses. Replaced all `if-instanceof` blocks with Java 21 exhaustive `switch` pattern matching expressions.
* **Result & Business Impact:** Guaranteed 100% compile-time verification: adding any future financial event now breaks compilation if any handler omits it, preventing fraud bypasses and reducing risk processing code by 45%.
"""

print("Writing Java basics files...")
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "01_java_fundamentals_jvm_primitives_and_pass_by_value.md"), JAVA_FUNDAMENTALS)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "02_java_strings_memory_string_pool_stringbuilder.md"), JAVA_STRINGS)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "03_java_oop_encapsulation_inheritance_polymorphism_abstraction.md"), JAVA_OOP)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "04_java_collections_framework_list_set_queue_map.md"), JAVA_COLLECTIONS)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "05_java_generics_wildcards_and_type_erasure.md"), JAVA_GENERICS)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "06_java_exception_handling_and_try_with_resources.md"), JAVA_EXCEPTIONS)
create_file(os.path.join(BASE_DIR, "09-backend-java-springboot", "07_java_modern_features_streams_lambdas_records_sealed.md"), JAVA_MODERN_FEATURES)
