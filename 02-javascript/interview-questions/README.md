# 🟨 JavaScript Interview Questions & Problem Index

> A categorized index of **Short Conceptual Questions, Output-Based Snippets, Machine Coding Problems, and Deep Engine Internals** for Senior JavaScript Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific interview questions in this folder (e.g., `01_output_promise_event_loop.md`, `02_polyfil_promise_all.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. Rapid-Fire / Short Questions
- [ ] `short_questions_basics.md` — `==` vs `===`, `null` vs `undefined`, `Object.is()`, primitive immutability.
- [ ] `short_questions_scope.md` — TDZ, Hoisting quirks, Block Scope vs Function Scope.
- [ ] `short_questions_functions.md` — Arrow function limitations, `arguments` object vs rest parameters.

### 2. Output-Based & Event Loop Snippets
- [ ] `output_event_loop_promises.md` — Tracing output order of `setTimeout`, Promises, `queueMicrotask`, and `async/await`.
- [ ] `output_this_binding.md` — Tracing `this` value across object methods, arrow functions, unbound calls, and strict mode.
- [ ] `output_closures_and_var.md` — Classic `for (var i=0; i<5; i++) setTimeout` problem and solutions.

### 3. Machine Coding & Polyfill Challenges
- [ ] `coding_polyfill_promise_all.md` — Implement `Promise.all` from scratch with proper error handling.
- [ ] `coding_polyfill_promise_allsettled.md` — Implement `Promise.allSettled`.
- [ ] `coding_debounce_and_throttle.md` — Implement `debounce` and `throttle` with leading/trailing option flags.
- [ ] `coding_deep_clone.md` — Implement `deepClone` handling nested objects, arrays, Circular references, Dates, and Maps.
- [ ] `coding_curry_function.md` — Implement `curry()` supporting arbitrary argument application.
- [ ] `coding_event_emitter.md` — Implement custom `EventEmitter` (`on`, `off`, `emit`, `once`).

### 4. Senior Lead Engine & Architectural Scenarios
- [ ] `scenario_memory_leak_debugging.md` — How to identify and fix a memory leak caused by un-cleared closures in Node/Browser.
- [ ] `scenario_event_loop_starvation.md` — How microtask queue flooding freezes the main thread and mitigation techniques.
