# 🟨 JavaScript Master Curriculum & Index

> A structured, step-by-step learning roadmap and interview index from **Basics to Advanced Core Engine Internals** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap.
- Create single concept files inside `01-javascript/` (e.g., `01_closures_and_lexical_scope.md`) as you learn and add your personal notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. Fundamentals & Core Types
- [ ] `01_data_types_and_type_coercion.md` — Primitive vs Reference types, Implicit vs Explicit coercion, `typeof` vs `instanceof`, `Object.is()`, `NaN` quirks.
- [ ] `02_var_let_const_hoisting_tdz.md` — Scoping differences, Variable Hoisting vs Function Hoisting, Temporal Dead Zone (TDZ).
- [ ] `03_functions_first_class_higher_order.md` — First-class functions, Higher-order functions, Pure functions vs Impure functions, Side effects.

### 2. Execution Context & Memory Management
- [ ] `04_execution_context_call_stack.md` — Creation phase vs Execution phase, Call Stack operations, Stack Overflow scenarios.
- [ ] `05_closures_and_lexical_scope.md` — Lexical Scope, Closure mechanics, Practical uses (Data Privacy, Currying, Memoization), Memory leak pitfalls.
- [ ] `06_v8_memory_garbage_collection.md` — V8 Heap & Stack memory allocation, Mark-and-Sweep algorithm, Generational GC (Scavenger vs Mark-Sweep-Compact), Identifying Memory Leaks.

### 3. Object-Oriented JS & Prototypes
- [ ] `07_this_keyword_and_binding.md` — Implicit binding, Explicit binding (`call`, `apply`, `bind`), Default binding, `new` binding, Arrow functions `this` behavior.
- [ ] `08_prototypes_and_inheritance.md` — Prototype chain, `__proto__` vs `prototype`, Prototypal Inheritance, Object.create(), Polyfills.
- [ ] `09_es6_classes_under_the_hood.md` — ES6 `class` syntax vs Constructor Functions, Transpilation to ES5, Private fields (`#`), Static methods.

### 4. Asynchronous JavaScript & Event Loop
- [ ] `10_event_loop_microtasks_macrotasks.md` — Single-threaded model, Call Stack, Web APIs, Microtask Queue (Promises, `queueMicrotask`, `MutationObserver`) vs Macrotask Queue (`setTimeout`, `setInterval`, I/O), Rendering steps.
- [ ] `11_promises_deep_dive.md` — Promise states (Pending, Fulfilled, Rejected), Chaining, Error propagation, Polyfilling `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`.
- [ ] `12_async_await_generators_iterators.md` — `async/await` under the hood (Generators + Promises), Generator functions (`function*`, `yield`), Symbol.iterator, Custom Iterators.

### 5. Advanced Engine Features & Web APIs
- [ ] `13_modules_cjs_vs_esm.md` — CommonJS (`require`/`module.exports`) vs ES Modules (`import`/`export`), Dynamic Imports, Tree Shaking prerequisites.
- [ ] `14_proxy_and_reflect_api.md` — Metaprogramming with `Proxy`, Traps (`get`, `set`, `has`, `deleteProperty`), `Reflect` object, Reactive frameworks connection (Vue 3/MobX).
- [ ] `15_dom_events_delegation_bubbling.md` — Event Propagation: Capturing phase vs Target phase vs Bubbling phase, Event Delegation pattern, `preventDefault()` vs `stopPropagation()`.

---

## 💡 High-Yield Senior Interview Questions Pointers

1. **What happens under the hood when V8 executes JavaScript code?**
   * *Answer Pointer:* Parser creates AST -> Ignition Interpreter generates Bytecode -> TurboFan JIT Compiler optimizes hot functions into machine code -> Deoptimization fallback if type assumptions fail.
2. **Why can't `setTimeout(fn, 0)` guarantee immediate execution in 0ms?**
   * *Answer Pointer:* `setTimeout` places callback into the Macrotask queue. It must wait for the current Call Stack to clear AND the entire Microtask Queue to drain before executing. Min delay spec is 4ms for nested timers.
3. **How do you detect and fix memory leaks in JavaScript?**
   * *Answer Pointer:* Use Chrome DevTools Heap Snapshots / Allocation Timeline. Look for: Un-cleared `setInterval`, Detached DOM nodes, Accidental Global Variables, Forgotten Event Listeners, Unclosed Closures holding large references.
4. **Difference between `Object.freeze()` and `Object.seal()`?**
   * *Answer Pointer:* `freeze()` prevents adding/deleting properties AND modifying values. `seal()` prevents adding/deleting properties but ALLOWS modifying existing values. Both are shallow.
