# Mapped Types and Template Literal Types: Metaprogramming in TypeScript

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
