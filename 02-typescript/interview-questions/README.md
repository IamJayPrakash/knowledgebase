# 🟦 TypeScript Interview Questions & Problem Index

> A categorized index of **Type System Challenges, Type Utility Implementations, Short Questions, and Compiler Architecture Questions** for Senior TypeScript Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific TypeScript interview questions in this folder (e.g., `01_type_narrowing_challenges.md`, `02_custom_deep_readonly.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. Rapid-Fire / Short Questions
- [ ] `short_questions_type_system.md` — `unknown` vs `any` vs `never`, interface vs type, tuple types.
- [ ] `short_questions_compiler.md` — `strictNullChecks`, `noImplicitAny`, `target` vs `module` flags.

### 2. Type Manipulation & Utility Implementation Challenges
- [ ] `coding_utility_pick_omit.md` — Re-implement `MyPick<T, K>` and `MyOmit<T, K>` without built-ins.
- [ ] `coding_utility_return_type.md` — Re-implement `MyReturnType<T>` using conditional types and `infer`.
- [ ] `coding_deep_readonly.md` — Implement `DeepReadonly<T>` for arbitrarily nested objects and arrays.
- [ ] `coding_tuple_to_union.md` — Convert a constant array/tuple to a union type (`TupleToUnion<T>`).
- [ ] `coding_template_literal_parser.md` — Parse route parameters from URL string template (e.g. `/user/:id/:name`).

### 3. Senior Lead Architectural Scenarios
- [ ] `scenario_branded_types.md` — How to enforce type-safe domain IDs (e.g. `UserId` vs `OrderId`) using Nominal / Branded Types.
- [ ] `scenario_monorepo_types.md` — Sharing type definitions across React frontend and Node/FastAPI backend in a monorepo.
