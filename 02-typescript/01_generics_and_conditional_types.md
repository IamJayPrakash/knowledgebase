# TypeScript Advanced Types & Conditional Types

## 1. Executive Summary
Conditional types in TypeScript allow type definitions to depend on type relationships (`T extends U ? X : Y`). Combined with the `infer` keyword, type mapping, and generics, they enable powerful meta-programming, compile-time validation, and exact type safety for API responses and ORMs.

---

## 2. Under the Hood Mechanics

```typescript
// Inferring return type of a function signature
type CustomReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Example Usage
function getUser() {
  return { id: 101, name: "Jay Prakash", role: "Tech Lead" };
}

type User = CustomReturnType<typeof getUser>;
// User -> { id: number; name: string; role: string; }
```

---

## 3. Senior Interview Q&A
* **Q: Explain Distributive Conditional Types.**
  * **A:** When conditional types act on generic type parameters, union types automatically distribute across the conditional check if the type parameter is naked (unwrapped). E.g., `ToArray<string | number>` expands to `ToArray<string> | ToArray<number>`.
