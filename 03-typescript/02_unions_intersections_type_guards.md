# Unions, Intersections & Custom Type Guards (is Predicate)

## 1. 📜 Problem / Topic Definition
Explain Union types (|), Intersection types (&), and how to safely narrow types using discriminated unions and user-defined type predicates.

---

## 2. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Union ka matlab 'ya toh ye ya wo'. Type Guard (`param is Type`) compiler ko batata hai ki if-condition ke andar type narrow ho chuki hai.
>
> **Real-World Analogy:** A security passport check: until the officer verifies your nationality, you are an unverified traveler; once verified, you enter the designated line.

---

## 3. 🧠 Core Mechanics & Foundation (DSA / Architecture)
- **What is it:** Union types represent values that can be one of several types. Type guards narrow down the type inside conditional blocks.
- **When to Use:** When handling diverse API responses, action dispatch payloads, and state variants.
- **When NOT to Use:** Avoid unnecessary type assertions (`as Type`) which bypass the type checker.

---

## 4. 💻 The 3 Evolution Versions (Newbie ➡️ Intermediate ➡️ Senior)

### ❌ Version 1: Unsafe Type Assertion (Any/As Bypass)
```javascript
// Line 1: Forcing compiler to accept type without runtime verification ❌
function handleInput(val: unknown) {
  (val as string).toUpperCase(); // Runtime crash if val is a number!
}
```

### ⚠️ Version 2: Typeof & Instanceof Narrowing
```javascript
function handleInputSafe(val: string | number) {
  if (typeof val === 'string') {
    return val.toUpperCase();
  }
  return val.toFixed(2);
}
```

### ✅ Version 3: Discriminated Unions & Custom Type Guard (`is` predicate)
```javascript
// Line 1: Discriminated Union with common discriminator 'status'
type SuccessResponse = { status: 'success'; data: string[] };
type ErrorResponse = { status: 'error'; message: string };
type ApiResponse = SuccessResponse | ErrorResponse;

// Line 2: User-defined Type Guard with 'is' predicate
function isSuccess(res: ApiResponse): res is SuccessResponse {
  return res.status === 'success';
}

function processResponse(res: ApiResponse) {
  // Line 3: Compiler narrows type automatically inside branch
  if (isSuccess(res)) {
    console.log(res.data.join(', ')); // Safe access to data!
  } else {
    console.error(res.message);        // Safe access to error message!
  }
}
```

---

## 5. 🎯 Senior Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain Unions, Intersections & Custom Type Guards (is Predicate) and how you use it in production?"
>
> **You:** "Unions model values that can be one of multiple types. Discriminated unions use a common literal tag to enable clean compiler narrowing. When complex object structures require validation, user-defined type guards with 'param is Type' predicates instruct TypeScript to narrow types safely at compile time without risky 'as' type casting."

---

## 6. 💼 Real-World Project Challenge (STAR Production Story)
* **Situation:** Multi-provider payment gateway handling 4 different webhook schemas with polymorphic fields.
* **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility.
* **Action Taken:** Implemented discriminated unions for payment events with custom type guards.
* **Result & Business Impact:** Eliminated 100% of runtime property access crashes across 500,000 monthly webhook events.

🗣️ **Script to Tell Interviewer:**
*"In one of our core systems, multi-provider payment gateway handling 4 different webhook schemas with polymorphic fields. I resolved this by implemented discriminated unions for payment events with custom type guards., which eliminated 100% of runtime property access crashes across 500,000 monthly webhook events.."*
