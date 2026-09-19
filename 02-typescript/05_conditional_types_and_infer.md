# Conditional Types and the `infer` Keyword: Advanced Type Algebra

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Conditional type TypeScript ka **Ternary Operator (`condition ? true : false`)** hai, jo runtime values ke liye nahi balki **Types** ke liye kaam karta hai: `T extends U ? X : Y`.
`infer` keyword ek **X-Ray Scanner** ki tarah hai: Socho ek gift box band hai (`Promise<User>`). Aapko nahi pata andar kya hai. `infer` keyword box ke andar jhankta hai, andar ke object ka type nikalta hai (`infer U`), aur use bahar nikal kar aapke haath mein de deta hai (`U` ban jata hai `User`).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Conditional Type Syntax**: `T extends U ? TrueType : FalseType`. Evaluates whether type `T` is assignable to `U`.
2. **Distributive Conditional Types**: When applied to a naked type parameter over a union, conditional types distribute over the union:
   `ToArray<string | number> === ToArray<string> | ToArray<number>`.
3. **Preventing Distribution**: Wrap both sides in square brackets: `[T] extends [U] ? TrueType : FalseType`.
4. **The `infer` Keyword**: Declares an unconstrained type variable inside the `extends` clause to be deduced pattern-matchingly by TypeScript.
5. **Multiple `infer` Usages**: Can extract function arguments, return types, Promise unwrap types, Array element types, and constructor parameters.
6. **Recursive Conditional Types**: Conditional types can call themselves recursively (e.g. deep unwrapping promises `Awaited<T>`).

---

## 📊 3. Visual Architecture Diagram

```
                      INFER PATTERN MATCHING
                      
  Input Type: Promise<UserSession>
                    │
                    ▼
  Match Pattern: T extends Promise<infer Inner> ? Inner : T
                    │
                    ├─► Match succeeds! T is Promise<...>
                    │   Inner is inferred as: UserSession
                    │
                    ▼
  Output Result: UserSession
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Extracting Array Element Type via infer
// ==========================================
// Line 5: If T is an array of infer E, return E; otherwise return T
type Flatten<T> = T extends Array<infer E> ? E : T;

type StringArray = string[];
type ExtractedString = Flatten<StringArray>; // string
type NonArray = number;
type LeftAlone = Flatten<NonArray>; // number


// ==========================================
// 2. Custom ReturnType Implementation
// ==========================================
// Line 17: Pattern match on callable function signature
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function fetchUser() {
  return { id: 101, username: "jay_prakash", role: "admin" };
}

// Line 24: Inferred as { id: number; username: string; role: string }
type FetchedUser = MyReturnType<typeof fetchUser>;


// ==========================================
// 3. Deep Unwrap of Promises (Recursive Conditional Type)
// ==========================================
// Line 31: Recursively unwraps nested Promise<Promise<T>>
type DeepAwaited<T> = T extends Promise<infer SubType>
  ? DeepAwaited<SubType>
  : T;

type NestedPromise = Promise<Promise<Promise<{ token: string }>>>;
// Line 37: Cleanly resolves to { token: string }
type ResolvedPayload = DeepAwaited<NestedPromise>;


// ==========================================
// 4. Distributive Conditional Types in Action
// ==========================================
// Line 44: Exclude implementation from scratch
type MyExclude<T, U> = T extends U ? never : T;

// Evaluates: ("a" extends "a" ? never : "a") | ("b" extends "a" ? never : "b")
type Filtered = MyExclude<"a" | "b" | "c", "a">; // "b" | "c"
```

---

## 🎯 5. The "Interview Pitch"
> "Conditional types introduce logic branching into TypeScript's type system via `T extends U ? X : Y`. When `T` is a naked type parameter over a union, it distributes automatically across each union constituent. The `infer` keyword enables pattern matching inside conditional type checks, allowing us to dynamically extract inner types from compound structures like Promise resolutions, function return types, constructor arguments, or tuple elements. This enables building custom utility types like `ReturnType<T>`, `Parameters<T>`, and `Awaited<T>` from scratch."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a distributed event-driven system with 80+ distinct Kafka message topics, event handler functions manually cast raw payloads (`payload as unknown as OrderCreatedPayload`). Type mismatches were slipping into production due to outdated manual assertions.
- **Task**: Create an automated type-inference dispatch engine where passing an event topic string automatically forces the callback payload to be 100% strictly typed according to the event schema registry.
- **Action**: We designed a type map `EventCatalog` and implemented a conditional extraction helper `type ExtractPayload<Topic extends keyof EventCatalog> = EventCatalog[Topic] extends { payload: infer P } ? P : never`. We created a generic subscriber `subscribe<K extends keyof EventCatalog>(topic: K, handler: (data: ExtractPayload<K>) => void)`.
- **Result**: Eliminated 100% of manual type assertions (`as unknown as T`) across all event consumers and caught 14 stale event schema mismatches at compile time during the refactor.
