# Modern Java Features (Java 8 to 21): Lambdas, Streams, Records, Sealed Classes & Pattern Matching

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
>
> **Hinglish Intuition:**
>
> - Lambda Expression: Anonymous function—ek chota sa kaam karne ke liye pura class aur method ka tam-jham likhne ke bajaye ek line ka arrow function `(x) -> x * 2` likh dena.
> - Streams API: Factory ki assembly line—ek taraf se raw material (data) ghusta hai, beech mein conveyor belt pe cleaning (`filter`), painting (`map`), aur packaging (`collect`) hoti hai, aur aakhri mein final product bahar nikalta hai!
> - Records (Java 14-17): Ek transparent ID card—sirf data rakhne ke liye 100 line ka boilerplate (getter, setter, constructor, equals, hashCode) likhne ki zaroorat nahi, ek line mein `record User(String name, int age) {}` likho aur sab automatic mil jata hai!
> - Sealed Classes (Java 17): Ek VIP list—aap define karte ho ki meri class ko sirf ye specific 2 classes hi extend kar sakti hain, koi teesri anjaan class extend nahi kar sakti!
>
> **Real-World Analogy:** An automated car manufacturing plant. A Stream is the assembly line where each chassis moves smoothly through workstations (filtering defective chassis, attaching engines, spray-painting colors) without creating intermediate parking lots for half-finished cars.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand

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

### 🧓 What an Experienced Candidate Knows

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
>
> **Interviewer:** "How do Records, Sealed Classes, and Pattern Matching enhance Java application architecture?"
>
> **You:** "Modern Java from version 17 to 21 transforms domain modeling through data-oriented programming. Records eliminate hundreds of lines of boilerplate for immutable data carriers while guaranteeing correct `equals`, `hashCode`, and thread safety. Sealed classes and interfaces give developers precise control over inheritance by restricting subclasses to an explicit permitted set. When combined with Java 21 Pattern Matching for `switch`, the compiler can perform exhaustive pattern checking without requiring fragile `default` branches. If someone adds a new permitted subclass in the future, the compiler immediately flags every unhandled `switch` statement across the codebase, eliminating runtime type bugs."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)

- **Situation:** A risk evaluation service parsed heterogeneous financial events using legacy `instanceof` cascades and explicit casting across 12 nested event classes. When a junior developer added a new `CryptoTransferEvent` class, three un-updated evaluation methods silently defaulted to the `else` branch, letting high-risk transfers bypass fraud checks.
- **Task / Challenge:** Re-architect the event hierarchy to enforce compile-time exhaustiveness checks across all fraud evaluation handlers.
- **Action Taken:** Converted the event classes into Java 17 `sealed interface FinancialEvent` with immutable `record` subclasses. Replaced all `if-instanceof` blocks with Java 21 exhaustive `switch` pattern matching expressions.
- **Result & Business Impact:** Guaranteed 100% compile-time verification: adding any future financial event now breaks compilation if any handler omits it, preventing fraud bypasses and reducing risk processing code by 45%.
