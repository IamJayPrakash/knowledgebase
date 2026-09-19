# 🟦 TypeScript Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **Basic Types to Advanced Type System Engineering** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for TypeScript.
- Create single concept files inside `02-typescript/` (e.g., `01_generics_and_conditional_types.md`) as you learn and add your notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. Type System Foundations
- [ ] `01_basic_types_any_unknown_never.md` — Primitives, `any` vs `unknown` vs `never`, Void, Literal types, Exhaustiveness checking.
- [ ] `02_unions_intersections_type_guards.md` — Union (`|`) vs Intersection (`&`), Discriminated Unions, User-defined Type Guards (`is` predicate), `typeof` & `instanceof` narrowing.
- [ ] `03_interfaces_vs_type_aliases.md` — Differences, Declaration Merging, Extension (`extends` vs `&`), Performance implications during compilation.

### 2. Generics & Type Meta-Programming
- [ ] `04_generics_and_constraints.md` — Generic functions, interfaces & classes, Generic constraints (`extends keyof`), Default generic parameters.
- [ ] `05_conditional_types_and_infer.md` — Conditional Types (`T extends U ? X : Y`), Distributive conditional types, Pattern matching with `infer` keyword.
- [ ] `06_mapped_types_and_template_literals.md` — Mapped Types (`[K in keyof T]`), Key remapping (`as`), Template Literal Types (`${Prefix}_${Suffix}`), Modifier flags (`-readonly`, `+?`).

### 3. Utility Types Deep Dive & Re-implementation
- [ ] `07_utility_types_from_scratch.md` — Re-implementing `Partial<T>`, `Required<T>`, `Readonly<T>`, `Record<K, T>`, `Pick<T, K>`, `Omit<T, K>`.
- [ ] `08_function_utility_types.md` — Re-implementing `ReturnType<T>`, `Parameters<T>`, `ConstructorParameters<T>`, `Awaited<T>`.

### 4. Compiler, Module System & Architecture
- [ ] `09_structural_vs_nominal_typing.md` — Duck typing in TS, Structural equivalence, Simulating Nominal typing (Branded types / Flavoring).
- [ ] `10_declaration_files_and_ambient_modules.md` — `.d.ts` files, Ambient modules (`declare module`), Module Augmentation, `@types/` package resolution.
- [ ] `11_tsconfig_and_compiler_architecture.md` — `tsconfig.json` best practices (`strict`, `noImplicitAny`, `skipLibCheck`), AST compiler phases (Scanner, Parser, Binder, Checker, Emitter).

---

## 🎯 Master Interview Questions (50 Deep Dive Questions)

For dedicated deep-dive technical interview preparation with runnable code and diagrams:
- 📖 [TypeScript Master Interview Directory](./interview-questions/README.md)
- 🧱 [Part 1: Types, Generics & Narrowing (Q1 - Q25)](./interview-questions/01_typescript_types_generics_and_narrowing_qna.md)
- ⚙️ [Part 2: Advanced Types, `infer` & Compiler Internals (Q26 - Q50)](./interview-questions/02_typescript_advanced_types_infer_and_compiler_qna.md)

---

## 💡 High-Yield Senior Interview Questions Pointers


1. **Difference between `unknown` and `any`?**
   * *Answer Pointer:* Both accept any value. `any` disables all type-checking (bypasses compiler). `unknown` enforces type narrowing or type assertions before performing operations on the variable, ensuring type safety.
2. **What are Branded Types and why are they used?**
   * *Answer Pointer:* TypeScript uses structural typing. Branded Types add a unique nominal tag (e.g., `type UserId = string & { readonly __brand: unique symbol }`) to prevent accidentally passing a raw `string` or `EmailId` where a `UserId` is expected.
3. **How does type inference work with `infer` in conditional types?**
   * *Answer Pointer:* `infer` introduces a type variable within the `extends` clause of a conditional type to extract sub-types (e.g. extracting array element type `T extends (infer U)[] ? U : T` or Promise unwrap `T extends Promise<infer U> ? U : T`).
