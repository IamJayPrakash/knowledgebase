# ⚛️ React Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **React Core Mechanics to Fiber Architecture & RSC** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section

- Use this `README.md` as your master index and curriculum roadmap for React.
- Create single concept files inside `03-react/` (e.g., `01_fiber_architecture_and_reconciliation.md`) as you learn and add your notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. React Architecture & Core Concepts

- [ ] `01_virtual_dom_and_jsx.md` — Virtual DOM diffing (Heuristic O(n) algorithm), JSX transpilation (`react/jsx-runtime`), Synthetic Event System.
- [ ] `02_fiber_architecture_deep_dive.md` — Fiber nodes tree, Work Loop, Render Phase (Interruptible) vs Commit Phase (Synchronous), Double Buffering tree strategy.
- [ ] `03_reconciliation_and_keys.md` — Diffing strategy (Component type changes vs Element attribute changes), Why index as `key` is an anti-pattern.

### 2. Hooks Deep Dive & Custom Hooks

- [ ] `04_state_hooks_usestate_usereducer.md` — `useState` & `useReducer` under the hood (Linked list of hook nodes), Batching updates, Functional state updates.
- [ ] `05_effect_hooks_useeffect_uselayouteffect.md` — `useEffect` lifecycle, Clean-up functions, `useLayoutEffect` (synchronous post-DOM mutation) vs `useEffect`, Race conditions in data fetching.
- [ ] `06_memoization_usememo_usecallback_memo.md` — Referential equality, When to use `useMemo`/`useCallback` vs Over-memoization penalty, `React.memo` shallow comparison.
- [ ] `07_advanced_hooks.md` — `useRef` (persistent mutable values across renders), `useImperativeHandle`, `useId`, `useSyncExternalStore` (subscribing to external stores safely).

### 3. Concurrent Mode & React 18/19 Features

- [ ] `08_concurrent_react_usetransition.md` — Concurrent Mode, `useTransition` (Non-blocking UI updates), `useDeferredValue` (Deferring expensive sub-tree renders), Automatic Batching.
- [ ] `09_suspense_and_streaming_ssr.md` — `<Suspense>` boundaries, Code splitting with `React.lazy`, HTML Streaming SSR, Selective Hydration.

### 4. State Management & Server Components (RSC)

- [ ] `10_state_management_patterns.md` — Prop drilling, Context API pitfalls & optimization (`useMemo` context value, splitting context), Redux Toolkit vs Zustand vs Jotai.
- [ ] `11_react_server_components_rsc.md` — Server Components vs Client Components, Server actions, Serialization boundary, Zero-bundle-size server code.

### 5. Performance Optimization & Security

- [ ] `12_performance_optimization_guide.md` — Profiling React applications (React DevTools Profiler), Windowing/Virtualization (react-window), Debouncing/Throttling UI inputs, Code splitting.
- [ ] `13_react_security_best_practices.md` — Preventing XSS (DangerouslySetInnerHTML sanitization), CSRF tokens, Securing local storage vs HTTP-only cookies.

---

## 📂 Master 100 Interview Question Bank & Coding Index

- [`interview-questions/README.md`](./interview-questions/README.md) — ⚛️ **Complete 100-Question Master Curriculum Index & Topic Guide**.
- [`interview-questions/01_react_foundations_vdom_and_jsx_qna.md`](./interview-questions/01_react_foundations_vdom_and_jsx_qna.md) — Questions 1 to 20: Foundations, JSX, Virtual DOM, and Component Architecture.
- [`interview-questions/02_react_hooks_internals_and_state_qna.md`](./interview-questions/02_react_hooks_internals_and_state_qna.md) — Questions 21 to 40: Hooks Internals, State Batching, and Lifecycle Synchronization.
- [`interview-questions/03_react_fiber_reconciliation_and_concurrency_qna.md`](./interview-questions/03_react_fiber_reconciliation_and_concurrency_qna.md) — Questions 41 to 60: Fiber Architecture, Reconciliation, and Concurrent Mode.
- [`interview-questions/04_react_performance_memoization_and_patterns_qna.md`](./interview-questions/04_react_performance_memoization_and_patterns_qna.md) — Questions 61 to 80: Performance Optimization, Memoization, and State Management.
- [`interview-questions/05_react_server_components_and_react19_qna.md`](./interview-questions/05_react_server_components_and_react19_qna.md) — Questions 81 to 100: React 19, Server Components (RSC), and Fullstack Architecture.
- [`interview-questions/machine_coding_autocomplete_search.md`](./interview-questions/machine_coding_autocomplete_search.md) — Machine Coding: Autocomplete Search with Debounce & Cache.
- [`interview-questions/machine_coding_virtualized_list.md`](./interview-questions/machine_coding_virtualized_list.md) — Machine Coding: High-Performance Virtualized Windowing List.
- [`interview-questions/top_react_interview_questions.md`](./interview-questions/top_react_interview_questions.md) — Senior Lead Quick Refresher.
