# TypeScript Types: any vs unknown vs never & Exhaustiveness Checking

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** any type-checking band kar deta hai (unsafe). unknown safe any hai jisme use karne se pehle type check karna padta hai. never un values ko represent karta hai jo kabhi exist hi nahi kar sakti.
>
> **Real-World Analogy:** any is an unlocked door with no guard. unknown is a locked vault where you must present ID before entering. never is an impossible black hole that can never be reached.

---

## 2. 📌 Core Mechanics & Key Points
- `any` completely disables compiler type checks (escapes the type system).
- `unknown` accepts any value, but forces type narrowing/guards before performing operations.
- `never` represents functions that throw or never return, and exhaustive switch-case validation.
- Exhaustive Checking: Using `never` in default cases guarantees compile errors when new union variants are added.

---

## 3. 📊 Visual Architecture Diagram

```text
[Type Hierarchy]
Top Type:    unknown / any (Accepts all values)
               │
Mid Types:   string | number | boolean | objects
               │
Bottom Type: never (No value can be assigned to never)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
// Line 1: any vs unknown demonstration
let anyVal: any = "hello";
anyVal.nonExistentMethod(); // Compiles fine, crashes at runtime! ❌

let unknownVal: unknown = "hello";
// unknownVal.toUpperCase(); // Compile Error! Must narrow type first ✅

// Line 2: Safe type narrowing with unknown
if (typeof unknownVal === "string") {
  console.log(unknownVal.toUpperCase()); // Safe!
}

// Line 3: Exhaustive Checking with never
type PaymentMethod = "credit_card" | "paypal" | "crypto";

function processPayment(method: PaymentMethod) {
  switch (method) {
    case "credit_card": return "Processed Card";
    case "paypal": return "Processed PayPal";
    case "crypto": return "Processed Crypto";
    default:
      // Line 4: If a new method is added to PaymentMethod, this line causes compile error!
      const _exhaustiveCheck: never = method;
      return _exhaustiveCheck;
  }
}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain TypeScript Types and your production experience with it?"
>
> **You:** "any disables the type checker, while unknown requires explicit type narrowing before usage, maintaining full type safety. never represents impossible values and unreachable code. We use never in union switch-cases to enforce exhaustive checking, catching unhandled cases at compile time."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** API response parser crashing on unanticipated null fields because types were typed as `any`.
* **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility under scale.
* **Action Taken:** Refactored all untrusted network JSON payloads to `unknown` and validated with Zod/Pydantic schemas.
* **Result & Business Impact:** Eliminated 100% of production runtime `TypeError: undefined is not a function` bugs.

🗣️ **Script to Tell Interviewer:**
*"In our production systems, api response parser crashing on unanticipated null fields because types were typed as `any`. I took charge of the architecture by refactored all untrusted network json payloads to `unknown` and validated with zod/pydantic schemas., successfully achieving eliminated 100% of production runtime `typeerror: undefined is not a function` bugs.."*
