# Top TypeScript Senior Interview Questions (Architecture & Theory)

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
