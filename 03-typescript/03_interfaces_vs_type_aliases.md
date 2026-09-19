# Interfaces vs Type Aliases: Architectural Decision Guide

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
>
> "I recommend using **interfaces** for object shapes, public API contracts, and domain models, especially when building libraries where consumers need to augment types via declaration merging (such as extending Express `Request` or browser `Window`). Interfaces also compile faster in TypeScript's type-checker due to flat caching. Conversely, I use **type aliases** whenever I need unions, primitives, tuples, mapped types, or complex conditional type transformations where an interface simply cannot express the type grammar."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an enterprise SaaS dashboard, TypeScript build times in CI degraded from 45 seconds to 4 minutes and 15 seconds after migrating state models to deep intersections of type aliases (`type A = B & C & D & E`).
- **Task**: Reduce CI compilation times back under 60 seconds without dropping strict type safety.
- **Action**: Using the TypeScript compiler profiler (`tsc --extendedDiagnostics`), we discovered that recursive evaluation of complex nested type alias intersections was creating over 120,000 internal type identity evaluations. We refactored the core domain entities from type intersections to `interface Child extends ParentA, ParentB` hierarchies.
- **Result**: `tsc` build time dropped from 4m 15s to 38 seconds (an 85% speedup), memory footprint of the compiler fell by 250 MB, and developer hot-reload was restored to sub-second latency.
