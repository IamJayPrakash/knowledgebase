# Building TypeScript Utility Types From Scratch

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
TypeScript ke built-in utility types (`Partial`, `Pick`, `Omit`, `Readonly`) jaise toolbox ke ready-made tools hote hain. Lekin ek master carpenter (Senior Developer) ko ye pata hona chahiye ki ye tools lohe aur lakdi se bante kaise hain. Jab standard tool fail hota hai (jaise deep nested objects ko readonly banana), tab aapko scratch se apna custom tool banana aana chahiye.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`MyPartial<T>`**: Loops through all keys in `T` and appends `?`.
2. **`MyRequired<T>`**: Loops through all keys in `T` and strips `-?`.
3. **`MyReadonly<T>`**: Loops through all keys and adds `readonly`.
4. **`MyRecord<K, T>`**: Maps each key in union `K` to type `T`.
5. **`MyPick<T, K>`**: Filters `T` to include only keys present in `K extends keyof T`.
6. **`MyOmit<T, K>`**: Combines `MyPick` and `MyExclude` to strip specified keys.
7. **`DeepReadonly<T>`**: Recursively walks nested objects and arrays to freeze modifications at all depths.

---

## 📊 3. Visual Architecture Diagram

```
           OMIT ARCHITECTURE PIPELINE: Pick<T, Exclude<keyof T, K>>
           
   Input Type T: { id: string; name: string; passwordHash: string }
                               │
   Target Keys to Omit K: "passwordHash"
                               │
                               ▼
   Step 1: Exclude<keyof T, K> ──► "id" | "name"
                               │
                               ▼
   Step 2: Pick<T, "id" | "name"> ──► { id: string; name: string }
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Core Object Utility Types from Scratch
// ==========================================

// Line 6: Partial: Make every property optional
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

// Line 11: Required: Strip optionality from every property
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};

// Line 16: Readonly: Enforce immutability on every property
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Line 21: Record: Construct object type with specified key union and value
type MyRecord<K extends keyof any, T> = {
  [P in K]: T;
};

// Line 26: Pick: Extract subset of keys K from T
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// Line 31: Exclude: Filter union T to exclude members assignable to U
type MyExclude<T, U> = T extends U ? never : T;

// Line 34: Omit: Pick keys of T that are NOT in K
type MyOmit<T, K extends keyof any> = MyPick<T, MyExclude<keyof T, K>>;


// ==========================================
// 2. Advanced: DeepReadonly Implementation
// ==========================================
// Line 41: Recursively freezes objects and arrays
type DeepReadonly<T> = T extends (...args: any[]) => any
  ? T // Functions are left untouched
  : T extends Array<infer U>
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T; // Primitives are already immutable by value

interface ServerState {
  version: number;
  config: {
    host: string;
    ssl: {
      cert: string;
      enabled: boolean;
    };
  };
  tags: string[];
}

const frozenState: DeepReadonly<ServerState> = {
  version: 1,
  config: {
    host: "localhost",
    ssl: {
      cert: "key.pem",
      enabled: true
    }
  },
  tags: ["prod", "v1"]
};

// frozenState.config.ssl.enabled = false; // Compiler Error: Cannot assign to 'enabled' because it is a read-only property!
// frozenState.tags.push("new"); // Compiler Error: Property 'push' does not exist on type 'readonly string[]'
```

---

## 🎯 5. The "Interview Pitch"
> "Demonstrating how to implement TypeScript's utility types from scratch showcases an understanding of mapped types, indexed access types, and distributive conditional types. For instance, `Partial<T>` uses `[K in keyof T]?: T[K]`, while `Omit<T, K>` combines `Pick<T, Exclude<keyof T, K>>`. Furthermore, standard utility types like `Readonly` are shallow; in real-world production architectures handling immutable state stores like Redux or NgRx, implementing a recursive `DeepReadonly<T>` using conditional type checks for functions, arrays, and objects is essential to guarantee state immutability at all nesting levels."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a fintech React/Redux app, developers were accidentally mutating nested account preferences (`state.user.settings.notifications.email = false`). Standard Redux state typed with `Readonly<RootState>` failed to protect nested objects because `Readonly` is strictly shallow.
- **Task**: Enforce 100% deep immutability across the entire state tree at compile-time without adding the runtime overhead of Immutable.js.
- **Action**: We wrote a custom `DeepReadonly<T>` recursive utility type and applied it to our root state definition. We verified that arrays mapped to `ReadonlyArray<T>` and nested objects mapped recursively.
- **Result**: Caught 27 unintentional state mutations immediately during compilation, preventing subtle UI state sync bugs and saving 45 KB of bundle size by avoiding external immutable runtime libraries.
