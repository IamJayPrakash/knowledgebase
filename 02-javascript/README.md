# 🟨 JavaScript Master Curriculum & Index

> A structured, step-by-step learning roadmap and interview index from **Complete Newbie Basics to Advanced Core Engine Internals** for Senior Technical Lead & SDE-2/3 interviews.

---

## 🗺️ Learning Roadmap & Concept Index

### Level 1: 🐣 Beginner Foundations & Syntax
- [x] [`01_data_types_and_type_coercion.md`](./01_data_types_and_type_coercion.md) — 7 Primitive types vs Reference types on Heap, Implicit vs Explicit type coercion, `typeof null === 'object'` bug, `Object.is()`, and `NaN !== NaN`.
- [x] [`02_var_let_const_hoisting_tdz.md`](./02_var_let_const_hoisting_tdz.md) — Function scope vs Block scope, Variable & Function Hoisting, and the Temporal Dead Zone (TDZ).
- [x] [`03_operators_control_flow_and_loops.md`](./03_operators_control_flow_and_loops.md) — Strict equality (`===`) vs loose (`==`), Nullish Coalescing (`??`), Optional Chaining (`?.`), Falsy values, and `for...of` (values) vs `for...in` (prototype keys trap).
- [x] [`04_arrays_in_depth_methods_and_iteration.md`](./04_arrays_in_depth_methods_and_iteration.md) — Mutating (`splice`, `sort`) vs Non-mutating (`map`, `filter`, `slice`, `toSorted`), V8 Fast vs Dictionary elements, and hand-coded `reduce` polyfill.
- [x] [`05_objects_destructuring_rest_spread_and_cloning.md`](./05_objects_destructuring_rest_spread_and_cloning.md) — Destructuring aliases & defaults, Rest/Spread, Shallow vs Deep clone, `structuredClone()`, and cyclic references with `WeakMap`.
- [x] [`06_functions_first_class_higher_order.md`](./06_functions_first_class_higher_order.md) — First-class functions, Higher-order functions, Pure functions, Side-effects, and Currying.

### Level 2: 🧠 Intermediate Execution Context & Object-Oriented JS
- [x] [`07_execution_context_call_stack.md`](./07_execution_context_call_stack.md) — Global vs Function Execution Context, Creation Phase (Lexical/Variable Environment) vs Execution Phase, Call Stack, and Stack Overflow.
- [x] [`08_closures_and_lexical_scope.md`](./08_closures_and_lexical_scope.md) — Lexical scoping, Closure heap memory cells, Data privacy, Memoization, and unclosed closure leak prevention.
- [x] [`09_this_keyword_and_binding.md`](./09_this_keyword_and_binding.md) — Default, Implicit, Explicit (`call`, `apply`, `bind`), and `new` binding rules; Lexical `this` in Arrow Functions.
- [x] [`10_prototypes_and_inheritance.md`](./10_prototypes_and_inheritance.md) — Prototype chain lookup, `__proto__` vs `prototype`, `Object.create()`, and prototypal inheritance mechanics.
- [x] [`11_es6_classes_under_the_hood.md`](./11_es6_classes_under_the_hood.md) — ES6 `class` syntactic sugar desugared to constructor functions, Private fields (`#`), `super()`, and Static methods.

### Level 3: 🚀 Advanced Engine Internals, Asynchronous & Web APIs
- [x] [`12_v8_memory_garbage_collection.md`](./12_v8_memory_garbage_collection.md) — V8 Stack vs Heap, Generational GC (New Space Scavenger with semi-spaces vs Old Space Mark-Sweep-Compact), and Chrome DevTools memory leak detection.
- [x] [`13_event_loop_microtasks_macrotasks.md`](./13_event_loop_microtasks_macrotasks.md) — Single-threaded execution model, Microtask Queue (Promises, `queueMicrotask`) vs Macrotask Queue (`setTimeout`, I/O), and UI rendering ticks.
- [x] [`14_promises_deep_dive.md`](./14_promises_deep_dive.md) — Promise states (Pending, Fulfilled, Rejected), Chaining, Error propagation, and Hand-coded `Promise.all` & `Promise.allSettled`.
- [x] [`15_async_await_generators_iterators.md`](./15_async_await_generators_iterators.md) — `async/await` desugared into Generator functions (`function*`, `yield`) + Promises, Iteration protocols (`Symbol.iterator`).
- [x] [`16_modules_cjs_vs_esm.md`](./16_modules_cjs_vs_esm.md) — CommonJS (`require` synchronous runtime evaluation) vs ES Modules (`import` static compile-time graph), Dynamic imports, and Tree-shaking.
- [x] [`17_proxy_and_reflect_api.md`](./17_proxy_and_reflect_api.md) — Metaprogramming with `Proxy`, Interception traps (`get`, `set`, `deleteProperty`), `Reflect` API, and reactive state stores.
- [x] [`18_dom_events_delegation_bubbling.md`](./18_dom_events_delegation_bubbling.md) — Event Propagation: Capturing phase vs Target vs Bubbling phase, Event Delegation pattern, `stopPropagation()` vs `stopImmediatePropagation()`.

---

## 📂 Interview Questions
* [`interview-questions/coding_deep_clone.md`](./interview-questions/coding_deep_clone.md) — Hand-crafted recursive deep clone handling circular references and edge cases.
* [`interview-questions/coding_promise_all.md`](./interview-questions/coding_promise_all.md) — Complete production polyfill of `Promise.all` from scratch.
* [`interview-questions/javascript_conceptual_questions.md`](./interview-questions/javascript_conceptual_questions.md) — High-frequency conceptual questions for SDE-2/3.
