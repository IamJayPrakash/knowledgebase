# 🟨 JavaScript Senior & Lead Master Interview Question Bank (100 Questions)

> Comprehensive, battle-tested 100-question interview bank covering everything from basic foundations to deep V8 engine internals, memory management, closures, prototypal inheritance, and async concurrency.

---

## 📑 Curriculum & Question Bank Structure

```
02-javascript/interview-questions/
├── 01_js_foundations_types_and_operators_qna.md    ──► Questions 1 to 20
├── 02_js_closures_scope_and_execution_context_qna.md ──► Questions 21 to 40
├── 03_js_objects_prototypes_and_classes_qna.md     ──► Questions 41 to 60
├── 04_js_async_event_loop_and_promises_qna.md      ──► Questions 61 to 80
├── 05_js_v8_memory_dom_and_modern_es_qna.md        ──► Questions 81 to 100
├── [Machine Coding & Polyfill Challenges]
│   ├── coding_polyfill_promise_all.md
│   ├── coding_deep_clone.md
│   ├── coding_debounce_and_throttle.md
│   ├── coding_curry_function.md
│   └── coding_event_emitter.md
└── [Output Tracing & Scenario Debugging]
    ├── output_event_loop_promises.md
    ├── output_this_binding.md
    └── scenario_memory_leak_debugging.md
```

---

## 🎯 Master Question Index (1 - 100)

### Part 1: Foundations, Types, Coercion & Operators (Q1 - Q20)

* [`01_js_foundations_types_and_operators_qna.md`](./01_js_foundations_types_and_operators_qna.md)
  1. Primitive data types and memory layout (Stack vs Heap).
  2. `typeof null === 'object'` and `typeof NaN === 'number'` historical context.
  3. `==` (Abstract) vs `===` (Strict) equality and coercion algorithm.
  4. `Object.is()` vs `===` (SameValue algorithm, NaN and signed zero).
  5. Temporal Dead Zone (TDZ) and `let`/`const` scoping.
  6. `null` vs `undefined` vs `undeclared`.
  7. Nullish Coalescing (`??`) vs Logical OR (`||`).
  8. Optional Chaining (`?.`) under the hood.
  9. `for...in` vs `for...of` semantics.
  10. Variable shadowing and scope leakage.
  11. Implicit type coercion in arithmetic operators (`+`, `-`, `*`, `/`).
  12. `Object.freeze()` vs `Object.seal()` vs `Object.preventExtensions()`.
  13. Shallow copy vs Deep copy mechanics.
  14. `structuredClone()` capabilities and boundary limitations.
  15. `Symbol` primitive and well-known symbols.
  16. `Map` vs Plain Object performance and features.
  17. `WeakMap` garbage collection semantics and use cases.
  18. `WeakSet` mechanics and tag pattern.
  19. `Array.prototype.slice()` vs `Array.prototype.splice()`.
  20. Tagged template literals and sanitization.

### Part 2: Closures, Lexical Scope, Execution Context & `this` (Q21 - Q40)

* [`02_js_closures_scope_and_execution_context_qna.md`](./02_js_closures_scope_and_execution_context_qna.md)
  21. Execution Context creation vs execution phases.
  22. Call Stack LIFO structure and Stack Overflow triggers.
  23. Closure heap allocation and V8 `[[Scopes]]` context.
  24. Solving the classic `for (var i = 0; i < 5; i++) setTimeout` problem (3 approaches).
  25. Function Currying, partial application, and point-free style.
  26. Generic `memoize` function using closures and Map.
  27. The 4 binding rules of `this` and precedence order.
  28. `call()`, `apply()`, and `bind()` comparison and use cases.
  29. Re-binding hard-bound functions and polyfill mechanics.
  30. Arrow functions lexical `this`, missing `arguments`, and lack of prototype.
  31. Function Declarations vs Function Expressions hoisting behavior.
  32. IIFE (Immediately Invoked Function Expression) architecture.
  33. Scope Chain identifier resolution algorithm.
  34. Four common memory leak sources in closures.
  35. V8 Accidental Shared Closure Context memory leak.
  36. Pure Functions and deterministic properties.
  37. Implement a `once` execution wrapper.
  38. Tail Call Optimization (TCO) status and engine trade-offs.
  39. Debouncing vs Throttling event rate limiting.
  40. `delete obj.prop` vs `delete varName`.

### Part 3: Objects, Prototypes, Inheritance & ES6 Classes (Q41 - Q60)

* [`03_js_objects_prototypes_and_classes_qna.md`](./03_js_objects_prototypes_and_classes_qna.md)
  41. The Prototype Chain and property delegation.
  42. `__proto__` vs `prototype` differences and pointers.
  43. Step-by-step mechanics of the `new` operator and polyfill.
  44. `Object.create(null)` for prototype-pollution proof lookup dictionaries.
  45. ES6 `class` syntactic sugar desugaring to ES5 prototypes.
  46. Constructor return values: primitive vs object behavior.
  47. Property Descriptors (`writable`, `enumerable`, `configurable`).
  48. Prototype Pollution vulnerabilities and runtime defenses.
  49. Native Private Class Fields (`#field`) vs TypeScript `private`.
  50. Getters and Setters property descriptors.
  51. The `super` keyword in constructors and method overrides.
  52. `Object.assign()` vs Object Spread (`...`).
  53. Multiple inheritance and Mixin patterns.
  54. `instanceof` operator and `Symbol.hasInstance`.
  55. `in` operator vs `hasOwnProperty()` vs `Object.hasOwn()`.
  56. Static initialization blocks in ES2022 classes.
  57. JavaScript Object vs JSON string differences.
  58. Polymorphism and dynamic dispatch in JavaScript.
  59. Deep freezing objects recursively.
  60. `Symbol.toPrimitive` and custom object type coercion.

### Part 4: Async Architecture, Event Loop, Promises & Concurrency (Q61 - Q80)

* [`04_js_async_event_loop_and_promises_qna.md`](./04_js_async_event_loop_and_promises_qna.md)
  61. Complete Event Loop diagram: Call Stack, Microtasks, Render, Macrotasks.
  62. Complex output tracing snippet breakdown (Promises + Timers + Microtasks).
  63. Microtask queue starvation and UI freeze mechanics.
  64. The 3 Promise states and irreversible settlement.
  65. Production `Promise.all` polyfill from scratch.
  66. `Promise.all` vs `allSettled` vs `race` vs `any` decision matrix.
  67. `async/await` desugaring into Generators and Promises.
  68. `return await promise` vs `return promise` inside and outside `try...catch`.
  69. Canceling fetch requests using `AbortController`.
  70. Automatic request timeouts with `AbortSignal.timeout()`.
  71. Generator functions (`function*` and `yield`) state suspension.
  72. Async Generators (`async function*`) and `for await...of`.
  73. `requestAnimationFrame` vs `setTimeout` frame synchronization.
  74. `queueMicrotask()` vs `Promise.resolve().then()`.
  75. Sequential asynchronous execution patterns.
  76. Unhandled Promise rejections and global listeners.
  77. Single-threaded Concurrency vs multi-threaded Parallelism.
  78. `Promise.resolve(val)` instance preservation vs new wrapper allocation.
  79. Building a concurrency-limiting Promise Pool queue.
  80. Error handling differences between Microtasks and Macrotasks.

### Part 5: V8 Internals, Memory Management, DOM & Modern ECMAScript (Q81 - Q100)

* [`05_js_v8_memory_dom_and_modern_es_qna.md`](./05_js_v8_memory_dom_and_modern_es_qna.md)
  81. V8 Engine pipeline: Ignition interpreter vs TurboFan compiler.
  82. Hidden Classes (Shapes) and Inline Caching (IC) optimization.
  83. Generational Garbage Collection: Scavenge vs Mark-Sweep-Compact.
  84. GC Roots in JavaScript memory graphs.
  85. Detached DOM Tree memory leaks and Chrome DevTools Heap profiling.
  86. Event propagation: Capturing vs Target vs Bubbling phases.
  87. Event Delegation pattern for high-performance dynamic lists.
  88. `event.target` vs `event.currentTarget`.
  89. `event.stopPropagation()` vs `stopImmediatePropagation()` vs `preventDefault()`.
  90. Asynchronous DOM observation with `MutationObserver`.
  91. High-performance scroll tracking via `IntersectionObserver`.
  92. Responsive element dimension tracking with `ResizeObserver`.
  93. Metaprogramming with `Proxy` and interception traps.
  94. Why you should always pair `Reflect` inside `Proxy` traps.
  95. CommonJS (CJS) vs ES Modules (ESM) architectural comparison.
  96. Tree-Shaking static dead code elimination requirements.
  97. Top-Level Await in ES2022 modules.
  98. Non-mutating array operations (`toSorted`, `toReversed`, `toSpliced`, `with`).
  99. Background threading with Web Workers and message serialization.
  100. True shared memory concurrency with `SharedArrayBuffer` and `Atomics`.

---

## 💻 Machine Coding & Polyfill Challenges

* [`coding_polyfill_promise_all.md`](./coding_polyfill_promise_all.md) — Implement `Promise.all` with fail-fast rejection.
* [`coding_deep_clone.md`](./coding_deep_clone.md) — Circular-reference safe recursive deep clone.
* [`coding_debounce_and_throttle.md`](./coding_debounce_and_throttle.md) — Debounce & Throttle with leading/trailing options.
* [`coding_curry_function.md`](./coding_curry_function.md) — Generic auto-currying function.
* [`coding_event_emitter.md`](./coding_event_emitter.md) — Custom typed EventEmitter with subscription disposal.
