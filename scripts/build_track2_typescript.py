# -*- coding: utf-8 -*-
"""
Generator for Track 2: TypeScript Deep Dive & Interview Questions
Generates:
1. 02-typescript/03_interfaces_vs_type_aliases.md
2. 02-typescript/04_generics_and_constraints.md
3. 05_conditional_types_and_infer.md
4. 06_mapped_types_and_template_literals.md
5. 07_utility_types_from_scratch.md
6. 08_function_utility_types.md
7. 09_structural_vs_nominal_typing.md
8. 10_declaration_files_and_ambient_modules.md
9. 11_tsconfig_and_compiler_architecture.md
10. 02-typescript/interview-questions/top_typescript_interview_questions.md
11. 02-typescript/interview-questions/coding_custom_utility_types.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "02-typescript", "03_interfaces_vs_type_aliases.md"): """# Interfaces vs Type Aliases: Architectural Decision Guide

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Interface ek **Open Legal Stamp Paper** ki tarah hai: Agar aapne stamp paper pe ek company policy likhi hai (`interface User { name: string }`), toh dusra partner aake usi stamp paper ke neeche ek aur line add kar sakta hai (`interface User { role: string }`). Dono lines aapas mein merge ho jayengi (**Declaration Merging**).
Type Alias ek **Permanent Car Number Plate** ki tarah hai: Ek baar jo number plate ban gayi (`type User = { name: string }`), usme aap nayi digit weld nahi kar sakte. Agar aap wahi naam dobara declare karne ki koshish karoge, toh RTO police (TypeScript Compiler) turant chalan kaat degi (`Duplicate identifier error`).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Declaration Merging**:
   - `interface` supports declaration merging: defining the same interface name multiple times merges their members. Crucial for extending global definitions (`Window`, `Express.Request`).
   - `type` cannot be declared multiple times with the same name; doing so throws `TS2300: Duplicate identifier`.
2. **Union & Primitive Types**:
   - `type` can represent unions (`type Status = "idle" | "loading" | "success"`), primitives (`type ID = string | number`), tuples (`type Point = [number, number]`), and template literals.
   - `interface` can only describe object shapes and callable function shapes; it cannot directly declare a union of primitives.
3. **Extensibility Syntax**:
   - `interface` extends via `extends`: `interface Admin extends User {}`.
   - `type` composes via intersection `&`: `type Admin = User & { permissions: string[] }`.
4. **Compiler Performance**:
   - In very large codebases (100k+ lines), interfaces are faster for the TS compiler to typecheck because TS caches interface shapes by flat identifier lookup, whereas type intersections require recursive structural evaluation.
5. **Computed Properties**:
   - In interfaces, mapped types cannot be used directly inside the interface body (`interface Mapped { [K in Keys]: string }` is invalid syntax).
   - In type aliases, mapped types are fully supported (`type Mapped = { [K in Keys]: string }`).

---

## 📊 3. Visual Architecture Diagram

```
      INTERFACE (Declaration Merging)            TYPE ALIAS (Immutable & Unions)
      
      ┌─────────────────────────────┐           ┌─────────────────────────────┐
      │ interface ExpressRequest {  │           │ type HttpMethod =           │
      │   body: any;                │           │   "GET" | "POST" | "DELETE";│
      │ }                           │           └──────────────┬──────────────┘
      └──────────────┬──────────────┘                          │ (Unions & Primitives)
                     │ (Merged automatically)                  ▼
      ┌──────────────┴──────────────┐           ┌─────────────────────────────┐
      │ interface ExpressRequest {  │           │ type UserWithRole =         │
      │   user?: JwtPayload;        │           │   User & { role: string };  │
      │ }                           │           └─────────────────────────────┘
      └─────────────────────────────┘
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Interface Declaration Merging (Augmentation)
// ==========================================
// Line 5: Declare base User profile interface
interface UserProfile {
  id: string;
  email: string;
}

// Line 11: Re-open the same interface in another file or middleware
interface UserProfile {
  // Line 13: Augment with authentication token
  jwtToken?: string;
  // Line 15: Augment with role property
  role: "admin" | "editor" | "viewer";
}

// Line 19: Object must satisfy ALL merged properties
const activeUser: UserProfile = {
  id: "USR-001",
  email: "jay@example.com",
  role: "admin",
  jwtToken: "eyJhbGciOi..."
};

// ==========================================
// 2. Type Aliases for Unions, Tuples & Primitives
// ==========================================
// Line 30: Union types cannot be declared via interfaces
type HttpStatusCode = 200 | 201 | 400 | 401 | 404 | 500;

// Line 33: Tuple types with named elements
type GeoCoordinates = [latitude: number, longitude: number];

// Line 36: Template literal type
type EventName = `on${"Click" | "Hover" | "Focus"}`;

// ==========================================
// 3. Extending Interfaces vs Intersecting Types
// ==========================================
// Interface extension (Cleaner compiler error diagnostics)
interface Animal {
  species: string;
}
interface Mammal extends Animal {
  hasFur: boolean;
}

// Type intersection (Can produce 'never' on incompatible primitives)
type Vehicle = { maxSpeed: number };
type Electric = { batteryKwh: number };
type Tesla = Vehicle & Electric & { autopilotVersion: number };

const myCar: Tesla = {
  maxSpeed: 250,
  batteryKwh: 100,
  autopilotVersion: 4
};
```

---

## 🎯 5. The "Interview Pitch"
> "I recommend using **interfaces** for object shapes, public API contracts, and domain models, especially when building libraries where consumers need to augment types via declaration merging (such as extending Express `Request` or browser `Window`). Interfaces also compile faster in TypeScript's type-checker due to flat caching. Conversely, I use **type aliases** whenever I need unions, primitives, tuples, mapped types, or complex conditional type transformations where an interface simply cannot express the type grammar."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an enterprise SaaS dashboard, TypeScript build times in CI degraded from 45 seconds to 4 minutes and 15 seconds after migrating state models to deep intersections of type aliases (`type A = B & C & D & E`).
- **Task**: Reduce CI compilation times back under 60 seconds without dropping strict type safety.
- **Action**: Using the TypeScript compiler profiler (`tsc --extendedDiagnostics`), we discovered that recursive evaluation of complex nested type alias intersections was creating over 120,000 internal type identity evaluations. We refactored the core domain entities from type intersections to `interface Child extends ParentA, ParentB` hierarchies.
- **Result**: `tsc` build time dropped from 4m 15s to 38 seconds (an 85% speedup), memory footprint of the compiler fell by 250 MB, and developer hot-reload was restored to sub-second latency.
""",

    os.path.join(BASE_DIR, "02-typescript", "04_generics_and_constraints.md"): """# Generics and Generic Constraints: Dynamic Type Engineering

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Generic ek **Mould / Sancha** ki tarah hai. Agar aapke paas ek cake mould hai, toh aap usme chocolate batter daalo toh chocolate cake banega, vanilla batter daalo toh vanilla cake banega. Aapko har cake ke liye alag mould banane ki zaroorat nahi hai.
Generic Constraint (`T extends HasId`) ek **VIP Entry Gate** ki tarah hai: Koi bhi guest andar aa sakta hai (T is generic), LEKIN uske paas ID card zaroor hona chahiye (`extends { id: string }`). Agar kisi ke paas ID card nahi hai, toh compiler gatekeeper use block kar dega!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Type Parameter `T`**: Functions, classes, and interfaces can accept type arguments dynamically at call time (`identity<T>(arg: T): T`).
2. **Type Inference**: TypeScript can automatically infer `T` from the runtime argument values, meaning you rarely need to write `<string>` manually.
3. **Generic Constraints (`extends`)**: Restricts generic arguments to types that satisfy a structural contract (`<T extends Record<string, any>>`).
4. **`keyof` with Generics**: Enforces that a parameter must be an existing property key of another generic object: `<T, K extends keyof T>(obj: T, key: K): T[K]`.
5. **Default Type Arguments**: Generic parameters can specify fallbacks (`<T = string>`).
6. **Generic Instantiation in Classes**: Generics allow creating reusable data structures (e.g. `LRUCache<K, V>`, `Repository<T>`).

---

## 📊 3. Visual Architecture Diagram

```
                         GENERIC PIPELINE FLOW
                         
  Caller provides: { id: 101, name: "Order" }
                           │
                           ▼
  Function Definition: function processRecord<T extends { id: number }>(record: T): T
                           │
                           ├─► Constraint Check: Does T have { id: number }? ──► YES
                           │
                           ▼
  V8/TS Evaluates: Return type is exact input type T (preserves all extra keys!)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Generic Constraint on Entity with ID
// ==========================================
// Line 5: Define minimal structural contract
interface Identifiable {
  id: string | number;
  createdAt: Date;
}

// Line 11: Constrain T to types that possess at least the Identifiable properties
function syncWithDatabase<T extends Identifiable>(entity: T): T {
  // Line 13: We are guaranteed that entity.id and entity.createdAt exist safely
  console.log(`Syncing entity ID: ${entity.id} created at ${entity.createdAt.toISOString()}`);
  
  // Line 16: Return entity preserving its complete specific shape (not just Identifiable)
  return entity;
}

// Line 20: Concrete record
const order = {
  id: "ORD-99",
  createdAt: new Date(),
  totalAmount: 149.99,
  items: ["book", "pen"]
};

// Line 28: TypeScript retains exact order shape including totalAmount and items
const savedOrder = syncWithDatabase(order);
console.log(savedOrder.totalAmount); // Fully type-safe!


// ==========================================
// 2. Safe Property Getter with keyof Constraint
// ==========================================
// Line 36: K is constrained to only valid keys of object T
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  // Line 38: Return exact property type corresponding to key K
  return obj[key];
}

const userAccount = {
  username: "jay_dev",
  followers: 4200,
  isVerified: true
};

// Line 48: Type is inferred as string
const uName = getProperty(userAccount, "username");
// Line 50: Type is inferred as number
const fCount = getProperty(userAccount, "followers");
// getProperty(userAccount, "invalidProp"); // Compiler Error: Argument of type '"invalidProp"' is not assignable to parameter of type '"username" | "followers" | "isVerified"'
```

---

## 🎯 5. The "Interview Pitch"
> "Generics allow developers to author reusable, type-safe functions, classes, and data structures while avoiding the unsafe loss of type information caused by `any`. With generic constraints via the `extends` keyword, we enforce minimal structural preconditions on type parameters without erasing additional properties. Combining generics with the `keyof` operator creates bulletproof APIs where property names and return types are strictly bound together, preventing runtime `undefined` property access bugs."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a multi-tenant Node/TypeScript banking backend, generic repository methods used `any` (`async findById(id: string): Promise<any>`). This led to runtime bugs where developers mistakenly called `.getBalence()` (typo) instead of `.getBalance()`, silently resulting in `NaN` transactions.
- **Task**: Create a unified, strictly typed database repository layer where every query dynamically preserves the entity schema without code duplication.
- **Action**: We engineered a generic base repository class `BaseRepository<T extends BaseEntity, K extends keyof T>` implementing CRUD methods with strict constraints. The `updateField<F extends keyof T>(id: string, field: F, value: T[F])` method ensured that both the field name and its corresponding assigned value type were strictly coupled.
- **Result**: Completely eradicated typo-induced property access runtime exceptions across all 32 microservices and reduced boilerplate repository code by 60%.
""",

    os.path.join(BASE_DIR, "02-typescript", "05_conditional_types_and_infer.md"): """# Conditional Types and the `infer` Keyword: Advanced Type Algebra

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
""",

    os.path.join(BASE_DIR, "02-typescript", "06_mapped_types_and_template_literals.md"): """# Mapped Types and Template Literal Types: Metaprogramming in TypeScript

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Mapped Type ek **Factory Conveyor Belt (`Array.prototype.map`)** ki tarah hai, jo values ko transform karne ke bajaye **Object ke Keys aur Types** ko transform karta hai. Agar aapke paas 50 fields ka form object hai, toh ek mapped type har field par jaakar usko ek jhatke mein `readonly` ya `optional (?)` bana sakta hai.
Template Literal Type JavaScript ke backtick strings (`` `hello ${name}` ``) ka type-level roop hai: Aap strings ke valid patterns ko compile-time par lock kar sakte ho, jaise `GET /api/users` ya `#FFFFFF` hex colors.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Mapped Type Syntax**: `[K in Keys]: ValueType`. Iterates over a union of string/number/symbol keys.
2. **Modifier Flags (`+`, `-`)**:
   - `+readonly` / `-readonly`: Adds or removes immutability.
   - `+?` / `-?`: Adds or removes optionality (e.g. making all properties required).
3. **Key Remapping (`as`)**: In TypeScript 4.1+, mapped types can transform key names using the `as` clause (`[K in keyof T as NewKeyName]: T[K]`).
4. **Template Literal Types**: Concatenates string literal types to form new unions: ``type Route = `/${string}` ``.
5. **Intrinsic String Manipulation Types**: Built-in compiler primitives: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`.

---

## 📊 3. Visual Architecture Diagram

```
                       MAPPED TYPE TRANSFORMATION
                       
   Source Type: { name: string; age: number }
                         │
                         ▼
   Transformation Rule: { [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K] }
                         │
                         ▼
   Resulting Type: {
      getName: () => string;
      getAge: () => number;
   }
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Modifiers in Mapped Types (-readonly and -?)
// ==========================================
interface UserSchema {
  readonly id: string;
  name?: string;
  age?: number;
}

// Line 11: Removes both readonly and optional modifiers
type ConcreteMutable<T> = {
  -readonly [K in keyof T]-?: T[K];
};

// Line 16: Resulting type: { id: string; name: string; age: number }
type ActiveUser = ConcreteMutable<UserSchema>;


// ==========================================
// 2. Key Remapping with Template Literals (Getters Generator)
// ==========================================
// Line 23: Transforms object properties into strongly-typed getter methods
type GenerateGetters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface AppConfig {
  apiUrl: string;
  port: number;
}

// Line 33: Resulting type: { getApiUrl: () => string; getPort: () => number }
type ConfigGetters = GenerateGetters<AppConfig>;

const getters: ConfigGetters = {
  getApiUrl: () => "https://api.domain.com",
  getPort: () => 8080
};


// ==========================================
// 3. Strict CSS / Hex Color Template Literal Validation
// ==========================================
// Line 45: Restrict strings to valid CSS color variables or hex format
type HexDigit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "A" | "B" | "C" | "D" | "E" | "F";
type HexColor = `#${HexDigit}${HexDigit}${HexDigit}` | `#${HexDigit}${HexDigit}${HexDigit}${HexDigit}${HexDigit}${HexDigit}`;

const validRed: HexColor = "#F00";
const validCyan: HexColor = "#00FFFF";
// const invalidColor: HexColor = "#GG0011"; // Compiler Error!
```

---

## 🎯 5. The "Interview Pitch"
> "Mapped types allow us to iterate over existing keys and produce modified object contracts dynamically, utilizing modifiers like `-readonly` or `-?` to strip immutability or optionality. Combined with TypeScript 4.1's key remapping using the `as` clause and template literal types, we can perform compile-time string metaprogramming—such as automatically generating strongly-typed getter/setter interfaces or validating event strings like `on${Capitalize<Event>}`. This drastically reduces manual boilerplate while maintaining ironclad compile-time safety."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a Next.js fullstack application, developers frequently mistyped backend REST route strings in API calls (`fetch('/api/v1/usrs')`), causing 404 errors that only surfaced during staging tests.
- **Task**: Enforce type-safe API routing at compile time across 120+ REST endpoints without using manual string constants.
- **Action**: We leveraged template literal types and mapped types over the backend controller contracts to construct a union of all valid routes: ``type ApiRoute = `/api/v1/${keyof Controllers}/${string}` ``. We wrapped `fetch` in an `apiFetch<R extends ApiRoute>(route: R)` client that only accepted valid constructed route templates.
- **Result**: Eliminated 100% of invalid endpoint URL 404 bugs during development and added automated IDE autocomplete for every API route in the application.
""",

    os.path.join(BASE_DIR, "02-typescript", "07_utility_types_from_scratch.md"): """# Building TypeScript Utility Types From Scratch

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
""",

    os.path.join(BASE_DIR, "02-typescript", "08_function_utility_types.md"): """# Function Utility Types: Parameters, ReturnType, and ConstructorParameters

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Function utility types ek **Automatic Resume Parser** ki tarah hain. Job applicant (function) se poochne ki zaroorat nahi hai ki uski qualifications kya hain; software function signature ko scan karke khud hi decide kar leta hai:
- Usse kitne arguments chahiye? (`Parameters<T>`)
- Wo kya result wapas karega? (`ReturnType<T>`)
- Usko initialize karne ke liye `new` ke sath kya dena padega? (`ConstructorParameters<T>`)

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`Parameters<T>`**: Extracts the parameter types of a function as a tuple:
   `type Parameters<T extends (...args: any) => any> = T extends (...args: infer P) => any ? P : never`.
2. **`ReturnType<T>`**: Extracts the return type of a function:
   `type ReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : any`.
3. **`ConstructorParameters<T>`**: Extracts parameters of a constructor function as a tuple:
   `type ConstructorParameters<T extends abstract new (...args: any) => any> = T extends abstract new (...args: infer P) => any ? P : never`.
4. **`InstanceType<T>`**: Extracts the instance type produced by a constructor function.
5. **Handling Overloaded Functions**: When applied to an overloaded function, `ReturnType` and `Parameters` only extract from the **last** overload signature.

---

## 📊 3. Visual Architecture Diagram

```
                 FUNCTION SIGNATURE INTROSPECTION
                 
  function createUser(name: string, age: number): { id: string; active: boolean }
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
       Parameters<T>                      ReturnType<T>
               │                               │
               ▼                               ▼
     [name: string, age: number]      { id: string; active: boolean }
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. Function Utility Types Implemented from Scratch
// ==========================================

// Line 6: Parameters from scratch
type CustomParameters<T extends (...args: any[]) => any> = T extends (
  ...args: infer P
) => any
  ? P
  : never;

// Line 14: ReturnType from scratch
type CustomReturnType<T extends (...args: any[]) => any> = T extends (
  ...args: any[]
) => infer R
  ? R
  : never;

// Line 22: ConstructorParameters from scratch
type CustomConstructorParameters<
  T extends abstract new (...args: any[]) => any
> = T extends abstract new (...args: infer P) => any ? P : never;


// ==========================================
// 2. Real-World Practical Application (API Wrapper)
// ==========================================
// Line 32: Third-party SDK function
function sendPayment(
  recipientId: string,
  amountInCents: number,
  currency: "USD" | "EUR" | "GBP",
  metadata?: Record<string, string>
): Promise<{ transactionId: string; status: "success" | "pending" }> {
  return Promise.resolve({ transactionId: "TX-1234", status: "success" });
}

// Line 42: Extract payment arguments tuple
type PaymentArgs = CustomParameters<typeof sendPayment>;

// Line 45: Extract payment resolution data
type PaymentResult = Awaited<CustomReturnType<typeof sendPayment>>;

// Line 48: Create a logged proxy that guarantees exact argument forwarding
async function loggedPayment(
  ...args: PaymentArgs
): Promise<PaymentResult> {
  console.log(`Processing payment for recipient: ${args[0]} of amount ${args[1]}`);
  const result = await sendPayment(...args);
  console.log(`Payment complete. TX: ${result.transactionId}`);
  return result;
}
```

---

## 🎯 5. The "Interview Pitch"
> "TypeScript's function utility types—`Parameters<T>`, `ReturnType<T>`, `ConstructorParameters<T>`, and `InstanceType<T>`—rely on conditional type pattern matching with `infer`. They are essential when wrapping third-party libraries or legacy code that doesn't explicitly export its internal argument or return types. By using `typeof functionRef` combined with `Parameters` and `ReturnType`, we can derive exact types without manual copy-pasting, ensuring wrapper functions stay perfectly in sync when upstream libraries update their signatures."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: An upstream authentication SDK updated a method signature from `login(email, pass)` to `login(email, pass, mfaCode?)`. Because our wrapper service manually hardcoded the parameters in 12 microservices, the upgrade broke builds and led to missed type checks during deployment.
- **Task**: Decouple our wrapper functions from manual type declarations and ensure auto-synchronization with upstream SDK types.
- **Action**: We refactored our wrapper methods to consume `Parameters<typeof sdk.login>` and `ReturnType<typeof sdk.login>`. We forwarded arguments via `(...args: Parameters<typeof sdk.login>)`.
- **Result**: When the SDK added the optional MFA code parameter, our wrappers immediately accepted it without writing a single line of redundant type definitions, saving hours of maintenance per SDK release.
""",

    os.path.join(BASE_DIR, "02-typescript", "09_structural_vs_nominal_typing.md"): """# Structural Typing vs Nominal Typing: Branding & Flavoring Techniques

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Structural Typing (Duck Typing)**: Agar koi pakshi batakh jaisa dikhta hai, batakh jaisa tairta hai aur batakh jaisa bolta hai, toh TypeScript use batakh hi manega. Chahe uska naam Cow ho, agar uske paas do pankh aur choonch hai, TS bolega: "All good!"
**Nominal Typing**: India aur USA dono mein 100 ka note hota hai. Dono pe "100" likha hai (Structure same hai). Lekin kya aap Indian shopkeeper ko 100 US Dollar dekar chai pi sakte ho? Nahi! Shopkeeper bolega currency ka "Brand" (Nominal origin) alag hai.
TypeScript is structurally typed, but we use **Branding (Type Flavoring)** to simulate nominal typing for safety.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Structural Equivalence**: If two objects share the same property names and types, TypeScript considers them compatible, regardless of interface names.
2. **Excess Property Checks**: Structural compatibility allows extra properties in variables, but object literals passed directly to functions trigger strict **excess property checking**.
3. **The Nominal Safety Problem**: In financial or safety-critical software, passing a `UserId` into a function expecting a `CompanyId` compiles fine if both are `string`.
4. **Type Branding / Nominal Tagging**: Attaching an un-inhabited unique property (`__brand: unique symbol`) forces TypeScript to treat structurally identical types as nominally distinct.
5. **Type Flavoring**: Using optional brand properties (`_flavor?: string`) allows partial nominal safety while preserving easier assignment ergonomics.

---

## 📊 3. Visual Architecture Diagram

```
       STRUCTURAL TYPING (DEFAULT)             NOMINAL TYPING (BRANDED)
       
  UserId = string;                       UserId = string & { readonly __brand: unique symbol }
  OrderId = string;                      OrderId = string & { readonly __brand: unique symbol }
  
  [ "usr_123" ]                          [ "usr_123" (branded) ]
       │                                            │
       ├────────────────────────┐                   ├────────────X (COMPILE ERROR!)
       ▼                        ▼                   ▼
  fn(uid: UserId)         fn(oid: OrderId)     fn(uid: UserId)   fn(oid: OrderId)
  (Both pass silently!)                         (Compiler blocks cross-assignment!)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. The Dangers of Structural Typing
// ==========================================
type USD = number;
type INR = number;

function transferFunds(amountInINR: INR) {
  console.log(`Transferring ₹${amountInINR}`);
}

const usdSalary: USD = 5000;
// Compiles without error! But results in disastrous financial error ($5000 treated as ₹5000)
transferFunds(usdSalary);


// ==========================================
// 2. Simulating Nominal Typing with Unique Symbol Brands
// ==========================================
// Line 18: Declare unique symbols for branding
declare const UsdBrand: unique symbol;
declare const InrBrand: unique symbol;

// Line 22: Define branded nominal types
export type BrandedUSD = number & { readonly [UsdBrand]: typeof UsdBrand };
export type BrandedINR = number & { readonly [InrBrand]: typeof InrBrand };

// Line 26: Type assertion constructor helpers
export function makeUSD(n: number): BrandedUSD {
  return n as BrandedUSD;
}

export function makeINR(n: number): BrandedINR {
  return n as BrandedINR;
}

// Line 35: Function accepting ONLY BrandedINR
function transferFundsStrict(amount: BrandedINR) {
  console.log(`Safely transferring ₹${amount}`);
}

const secureUsd = makeUSD(5000);
const secureInr = makeINR(415000);

transferFundsStrict(secureInr); // Compiles perfectly!

// transferFundsStrict(secureUsd);
// COMPILER ERROR: Type 'typeof UsdBrand' is not assignable to type 'typeof InrBrand'!
```

---

## 🎯 5. The "Interview Pitch"
> "TypeScript's type system is fundamentally structural, meaning compatibility is governed solely by an entity's shape and members rather than its explicit declaration. While this provides tremendous flexibility in JavaScript ecosystems, it creates dangerous failure modes when distinct domain primitives—like sanitized HTML versus raw HTML, or UserIDs versus OrderIDs—are represented by plain strings. We solve this using **Type Branding**, which intersects the primitive type with a nominal tag such as `{ readonly [brand]: unique symbol }`. This enforces compile-time nominal discrimination with zero runtime memory overhead."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an international crypto exchange, a bug occurred where internal trading bot code passed `BitcoinAmount` (float 0.05) into an execution routine expecting `Satoshis` (integer 5,000,000). Because both were typed as `number`, the system attempted to execute a transfer for 0.05 satoshis, corrupting settlement ledgers.
- **Task**: Permanently prevent cross-unit numeric assignments at compile time across the trading engine.
- **Action**: We implemented type branding for all financial units: `BTC`, `Satoshi`, `USD_Cents`, and `USDT`. We created validated builder functions (`toSatoshi(btc)`) that performed unit conversion before applying the brand.
- **Result**: Completely eliminated unit-mismatch trading errors across the exchange platform and caught two latent unit bugs in pre-existing calculation pipelines during rollout.
""",

    os.path.join(BASE_DIR, "02-typescript", "10_declaration_files_and_ambient_modules.md"): """# Declaration Files (`.d.ts`) and Ambient Modules

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
`.d.ts` file ek **Movie Subtitle File (`.srt`)** ki tarah hoti hai. Movie (JavaScript file) mein sirf action aur sound hai. Lekin movie player (TypeScript Compiler / IDE) ko samajhne ke liye ek alag text file chahiye hoti hai jo bataye ki kaun sa character kab kya bol raha hai. 
`.d.ts` files contain **zero runtime JavaScript code**; they only describe the types so your IDE can provide autocomplete and type safety for raw JS files or global browser variables.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Ambient Declarations (`declare`)**: Instructs the TypeScript compiler that a variable, function, or class exists in the global execution environment at runtime.
2. **`.d.ts` vs `.ts`**: `.d.ts` files contain only types and ambient declarations. Any actual runtime code (`const x = 5`) inside a declaration file triggers a compiler error.
3. **Module Augmentation (`declare module`)**: Allows extending external npm package types without modifying their node_modules source files.
4. **Global Augmentation (`declare global`)**: Injects types directly onto the global namespace (`Window`, `process.env`).
5. **Wildcard Module Declarations**: Used to type non-JavaScript assets such as CSS modules, SVGs, and image imports: `declare module '*.svg'`.

---

## 📊 3. Visual Architecture Diagram

```
                 AMBIENT DECLARATION RESOLUTION
                 
   import logo from "./logo.svg"; 
                 │
                 ▼
   TypeScript Compiler checks .d.ts files:
   ┌──────────────────────────────────────────────┐
   │ declare module "*.svg" {                     │
   │   const content: string;                     │
   │   export default content;                    │
   │ }                                            │
   └──────────────────────────────────────────────┘
                 │
                 ▼
   Result: logo is recognized as type 'string' (Zero compile errors!)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// ==========================================
// 1. global.d.ts: Augmenting Node.js Process & Browser Window
// ==========================================

// Line 5: Augment the global NodeJS namespace
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: "development" | "production" | "test";
    PORT: string;
    DATABASE_URL: string;
    JWT_SECRET: string;
  }
}

// Line 16: Augment browser Window object with custom analytics SDK
interface Window {
  myAnalytics: {
    track: (event: string, properties: Record<string, unknown>) => void;
    userId?: string;
  };
}


// ==========================================
// 2. assets.d.ts: Wildcard Declarations for Static Assets
// ==========================================
// Line 29: Typing CSS Modules
declare module "*.module.css" {
  const classes: { readonly [key: string]: string };
  export default classes;
}

// Line 35: Typing Image Assets
declare module "*.png" {
  const src: string;
  export default src;
}


// ==========================================
// 3. Module Augmentation: Extending Express Request
// ==========================================
import "express";

declare module "express-serve-static-core" {
  interface Request {
    user?: {
      id: string;
      email: string;
      role: "admin" | "user";
    };
  }
}
```

---

## 🎯 5. The "Interview Pitch"
> "TypeScript declaration files with the `.d.ts` extension provide type definitions for JavaScript code without emitting any runtime artifacts. They are utilized in three primary scenarios: first, providing types for untyped third-party npm packages via DefinitelyTyped (`@types/*`); second, declaring non-code assets like SVGs and CSS modules via wildcard declarations (`declare module '*.png'`); and third, performing module augmentation to extend existing library types—such as adding a strongly-typed `user` object to Express's `Request` interface."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a Next.js enterprise app, environment variables were accessed via `process.env.NEXT_PUBLIC_STRIPE_KEY`. A developer deployed code with a typo (`process.env.STRIPE_KEY`), which evaluated to `undefined` in production and caused checkout payments to fail.
- **Task**: Ensure that any missing or mistyped environment variable throws an immediate compile-time error during build.
- **Action**: We added an ambient declaration file `env.d.ts` augmenting `NodeJS.ProcessEnv` with strict literal types for all application configuration keys. We also hooked `zod` schema parsing into Next.js configuration to validate variables at startup.
- **Result**: Eliminated all environment variable typos across development and staging, catching two missing environment variables in CI before production deployment.
""",

    os.path.join(BASE_DIR, "02-typescript", "11_tsconfig_and_compiler_architecture.md"): """# `tsconfig.json` Mastery and TypeScript Compiler Architecture

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
TypeScript Compiler (`tsc`) ek **High-Tech Airport Customs Scanner** ki tarah hai, aur `tsconfig.json` us scanner ki **Sensitivity Settings File** hai.
- Agar aapne `strict: true` rakha hai, toh scanner har choti se choti suspicious cheez (`any`, uninitialized variables, null access) par beep karega.
- Agar aapne sensitivity kam kar di (`noImplicitAny: false`), toh koi bhi illegal bag leke nikal jayega aur airport ke bahar (production runtime) crash ho jayega.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`tsc` Internal Pipeline**:
   - **Parser**: Converts source code into Abstract Syntax Tree (AST).
   - **Binder**: Creates Symbols linking identifiers to declarations.
   - **Type Checker**: The heavy engine that checks types across the symbol graph.
   - **Emitter**: Emits clean JavaScript (`.js`) and declarations (`.d.ts`).
2. **`strict: true` Flag Bundle**:
   Enables `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, and `useUnknownInCatchVariables`.
3. **`moduleResolution: "bundler"` vs `"node16"` / `"nodenext"`**:
   - `"bundler"`: Modern standard for Vite/Next.js; understands ESM packages with extensionless imports.
   - `"nodenext"`: Strictly enforces Node.js native ESM rules (requires explicit `.js` extensions in imports even in TypeScript files).
4. **`skipLibCheck: true`**: Skips type-checking of all `.d.ts` files in `node_modules`. Saves up to 60% of compilation time.
5. **Project References (`composite: true`)**: Enables incremental builds across monorepo packages.

---

## 📊 3. Visual Architecture Diagram

```
                 TSC COMPILER FIVE-STAGE PIPELINE
                 
   Source (.ts)
        │
        ▼
   [ 1. Scanner ] ──► Tokens
        │
        ▼
   [ 2. Parser ] ──► Abstract Syntax Tree (AST)
        │
        ▼
   [ 3. Binder ] ──► Symbols & Scopes
        │
        ▼
   [ 4. Type Checker ] ──► Diagnostics & Type Validation (HEAVIEST STAGE)
        │
        ▼
   [ 5. Emitter ] ──► Output (.js, .d.ts, .map)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```json
{
  "compilerOptions": {
    /* Base Options */
    "target": "ES2022",                          // Target modern ECMAScript standard
    "module": "NodeNext",                        // Modern native Node.js ESM module system
    "moduleResolution": "NodeNext",              // Enforces strict file extension rules
    "lib": ["ES2022"],                           // Standard runtime library typings
    
    /* Strict Type Checking (Production Gold Standard) */
    "strict": true,                              // Enable all strict type-checking options
    "noImplicitAny": true,                       // Error on expressions with implied 'any' type
    "strictNullChecks": true,                    // null and undefined have their own distinct types
    "strictFunctionTypes": true,                 // Ensure function parameters are checked contravariantly
    "noImplicitThis": true,                      // Error when 'this' expression has type 'any'
    "useUnknownInCatchVariables": true,          // Catch clause variables default to 'unknown'
    
    /* Code Quality & Linter Rules */
    "noUnusedLocals": true,                      // Report errors on unused local variables
    "noUnusedParameters": true,                  // Report errors on unused function parameters
    "noFallthroughCasesInSwitch": true,          // Report errors for fallthrough cases in switch
    "noUncheckedIndexedAccess": true,            // Add 'undefined' to any unindexed access (obj[key])
    
    /* Emit & Build Performance */
    "declaration": true,                         // Generate corresponding .d.ts files
    "declarationMap": true,                      // Create sourcemaps for d.ts to navigate to TS source
    "sourceMap": true,                           // Create .js.map files for production debugging
    "skipLibCheck": true,                        // Skip type checking of all declaration files (Huge speedup)
    "incremental": true,                         // Enable incremental compilation via .tsbuildinfo
    "tsBuildInfoFile": "./.tsbuildinfo"          // Cache location for incremental compilation
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 🎯 5. The "Interview Pitch"
> "A production-grade `tsconfig.json` balances maximum type safety with fast build performance. Beyond turning on `strict: true`, the most critical flag for preventing runtime bugs is `noUncheckedIndexedAccess`, which forces TypeScript to type dictionary and array lookups as `T | undefined` rather than assuming the element always exists. For performance, setting `skipLibCheck: true` prevents redundant re-checking of third-party node_modules declarations, while enabling `incremental: true` allows `tsc` to persist build state graphs and drastically accelerate developer compilation loops."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A production Node.js service crashed with `TypeError: Cannot read properties of undefined (reading 'country')` when processing user addresses fetched from an external API (`const country = response.addresses[0].country`).
- **Task**: Prevent array index out-of-bounds crashes from ever compiling in our repository.
- **Action**: We enabled `"noUncheckedIndexedAccess": true` in `tsconfig.json`. This forced all array index access `arr[0]` and arbitrary key access `record[key]` to be inferred as `T | undefined`. The compiler immediately flagged 43 unsafe array lookups where developers assumed elements existed without checking length.
- **Result**: Zero index-out-of-bounds runtime crashes occurred over the following 12 months, and developers adopted optional chaining (`addresses[0]?.country`) universally.
""",

    os.path.join(BASE_DIR, "02-typescript", "interview-questions", "top_typescript_interview_questions.md"): """# Top TypeScript Senior Interview Questions (Architecture & Theory)

---

## 1. What is the difference between `any`, `unknown`, and `never`?
- **`any`**: Turns off type-checking completely. You can assign anything to it, and assign it to anything. Bypasses compiler safety.
- **`unknown`**: The type-safe counterpart of `any`. Anything can be assigned to `unknown`, but `unknown` **cannot** be assigned to any other type without type narrowing or type assertions.
- **`never`**: The bottom type representing values that never occur. Used for functions that never return (throw error or infinite loop), or exhaustive checks in switch statements.

```typescript
function exhaustiveCheck(val: never): never {
  throw new Error(`Unhandled case: ${val}`);
}
```

---

## 2. Explain Contravariance vs Covariance in TypeScript.
- **Covariance**: A subtype can be assigned where a supertype is expected. Return types of functions are covariant.
- **Contravariance**: A supertype can be assigned where a subtype is expected. When `strictFunctionTypes: true` is enabled, function parameters are checked **contravariantly** to prevent unsafe method calls.
- **Bivariance**: By default without strict flags, method parameters on interfaces are bivariant for historical compatibility.

---

## 3. What is Declaration Merging and where is it used in production?
- TypeScript merges multiple declarations of the same identifier if they are `interface` or `namespace`.
- In production, it is used for **Module Augmentation** (e.g. extending Express `Request` with session or user credentials, or extending `Window` with custom third-party SDK objects).

---

## 4. What is the difference between `type` intersection (`&`) and `interface extends`?
- `interface extends` checks for conflicts and throws clean compiler errors if property types are incompatible.
- `type` intersection (`A & B`) will synthesize conflicting primitive properties into `never` (`string & number === never`), which can lead to confusing downstream error messages.
- Interfaces are cached by name during typechecking and perform better in large codebases.

---

## 5. What does the `satisfies` operator do in TypeScript 4.9+?
- `satisfies` validates that an expression matches a type **without changing the inferred type** of the expression.
- With `: Type`, the variable gets widened to the declared type, losing literal precision.
- With `satisfies Type`, you get compile-time validation while keeping the exact literal types for autocomplete and narrowing.

```typescript
type Palette = Record<string, string | number[]>;

// Using satisfies retains exact RGB array type on 'blue'!
const colors = {
  red: "#FF0000",
  blue: [0, 0, 255]
} satisfies Palette;

// colors.blue is known to be number[], so .map() is safe!
colors.blue.map(c => c * 2);
```
""",

    os.path.join(BASE_DIR, "02-typescript", "interview-questions", "coding_custom_utility_types.md"): """# Machine Coding: Hard TypeScript Custom Utility Types

---

## Challenge 1: `DeepPartial<T>`
Recursively transforms all properties of an object (including nested objects and arrays) to optional.

```typescript
// Solution:
type DeepPartial<T> = T extends (...args: any[]) => any
  ? T
  : T extends Array<infer U>
  ? _DeepPartialArray<U>
  : T extends object
  ? _DeepPartialObject<T>
  : T;

type _DeepPartialArray<T> = Array<DeepPartial<T>>;
type _DeepPartialObject<T> = { [K in keyof T]?: DeepPartial<T[K]> };

// Test
interface ComplexUser {
  id: number;
  profile: {
    avatar: string;
    preferences: {
      theme: "light" | "dark";
      notifications: boolean;
    };
  };
}

const partialData: DeepPartial<ComplexUser> = {
  profile: {
    preferences: {
      theme: "dark"
    }
  }
};
```

---

## Challenge 2: `FlattenObjectKeys<T>` (Dot Notation Path Extractor)
Transforms a nested object type into dot-notated string literal paths (`"profile.preferences.theme"`).

```typescript
type FlattenObjectKeys<T extends object> = {
  [K in keyof T & string]: T[K] extends object
    ? `${K}` | `${K}.${FlattenObjectKeys<T[K]>}`
    : `${K}`;
}[keyof T & string];

type AppPaths = FlattenObjectKeys<ComplexUser>;
// Result: "id" | "profile" | "profile.avatar" | "profile.preferences" | "profile.preferences.theme" | "profile.preferences.notifications"
```

---

## Challenge 3: `RequireAtLeastOne<T, Keys>`
Enforces that at least one of the specified properties must be present.

```typescript
type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = Pick<
  T,
  Exclude<keyof T, Keys>
> &
  {
    [K in Keys]-?: Required<Pick<T, K>> &
      Partial<Pick<T, Exclude<Keys, K>>>;
  }[Keys];

interface ContactForm {
  name: string;
  email?: string;
  phone?: string;
}

// User must provide at least email OR phone
type ValidatedContact = RequireAtLeastOne<ContactForm, "email" | "phone">;

const valid1: ValidatedContact = { name: "Jay", email: "jay@test.com" };
const valid2: ValidatedContact = { name: "Jay", phone: "1234567890" };
// const invalid: ValidatedContact = { name: "Jay" }; // Error: Property 'email' or 'phone' missing!
```
"""
}

def main():
    print(f"Generating {len(FILES)} Track 2 TypeScript deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 2 TypeScript generation complete!")

if __name__ == "__main__":
    main()
