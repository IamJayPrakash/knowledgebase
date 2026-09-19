# ⚛️ React Senior & Lead Master Interview Question Bank (100 Questions)

> Comprehensive, production-grade 100-question interview bank covering everything from basic JSX & Virtual DOM reconciliation to Fiber internals, Lanes concurrency, state architectures, and React 19 / Server Components.

---

## 📑 Curriculum & Question Bank Structure

```
04-react/interview-questions/
├── 01_react_foundations_vdom_and_jsx_qna.md        ──► Questions 1 to 20
├── 02_react_hooks_internals_and_state_qna.md        ──► Questions 21 to 40
├── 03_react_fiber_reconciliation_and_concurrency_qna.md ──► Questions 41 to 60
├── 04_react_performance_memoization_and_patterns_qna.md ──► Questions 61 to 80
├── 05_react_server_components_and_react19_qna.md    ──► Questions 81 to 100
├── [Machine Coding Challenges]
│   ├── machine_coding_autocomplete_search.md
│   └── machine_coding_virtualized_list.md
└── [Quick Refresher]
    └── top_react_interview_questions.md
```

---

## 🎯 Master Question Index (1 - 100)

### Part 1: Foundations, JSX, Virtual DOM & Component Architecture (Q1 - Q20)

* [`01_react_foundations_vdom_and_jsx_qna.md`](./01_react_foundations_vdom_and_jsx_qna.md)
  1. JSX compilation under the hood (`_jsx` runtime vs `React.createElement`).
  2. Virtual DOM purpose and performance architecture.
  3. Reconciliation diffing algorithm and two heuristic assumptions.
  4. Why using array `index` as a `key` is an anti-pattern.
  5. Controlled vs Uncontrolled components comparison.
  6. Why `<input type="file" />` is strictly uncontrolled.
  7. Synthetic Events and container root delegation in React 17+.
  8. React Element vs Component vs Instance.
  9. Pure Components and `React.memo` shallow comparisons.
  10. Higher-Order Components (HOCs) and Wrapper Hell trade-offs.
  11. The Render Props pattern.
  12. Props (unidirectional) vs State (internal mutable).
  13. React Fragments (`<React.Fragment>` with keys vs `<>...</>`).
  14. Portals (`createPortal`) and event bubbling across DOM boundaries.
  15. Error Boundaries and uncaught error categories.
  16. Prop Drilling vs Context API trade-offs.
  17. Strict Mode (`<React.StrictMode>`) double-invoking mechanics.
  18. Declarative vs Imperative UI paradigms.
  19. Upward child-to-parent communication via callbacks.
  20. Modern default props in functional components.

### Part 2: Hooks Internals, State Batching & Lifecycle Synchronization (Q21 - Q40)

* [`02_react_hooks_internals_and_state_qna.md`](./02_react_hooks_internals_and_state_qna.md)
  21. Rules of Hooks and Fiber hook singly linked list.
  22. Automatic Batching in React 18 across async boundaries.
  23. Direct values vs functional updates in `setState`.
  24. Lazy state initialization in `useState`.
  25. `useEffect` vs `useLayoutEffect` vs `useInsertionEffect`.
  26. `useRef` mechanics and escaping the React lifecycle.
  27. Capturing previous props/state with `useRef`.
  28. Stale closures in hooks and dependency array correctness.
  29. When to choose `useReducer` over `useState`.
  30. `useImperativeHandle` for controlled ref exposure.
  31. `useId` and SSR hydration mismatch elimination.
  32. Why updating state in the render body causes infinite loops.
  33. How React detects when to execute effect cleanup functions.
  34. Why `useEffect` callbacks cannot be `async`.
  35. `useDebugValue` for custom hook development.
  36. Errors inside cleanup functions and Error Boundaries.
  37. Building a custom `useDebounce` hook.
  38. Building a custom `useLocalStorage` hook with cross-tab syncing.
  39. `useCallback` purpose, valid use cases, and wasted allocations.
  40. `useMemo` computation caching and runtime memory cost.

### Part 3: Fiber Architecture, Reconciliation & Concurrent Mode (Q41 - Q60)

* [`03_react_fiber_reconciliation_and_concurrency_qna.md`](./03_react_fiber_reconciliation_and_concurrency_qna.md)
  41. React 15 Stack Reconciler limitations and call stack blocking.
  42. Fiber Node structure (`child`, `sibling`, `return`, `alternate`, `lanes`).
  43. Double Buffering (`current` tree vs `workInProgress` tree).
  44. Render phase (concurrent/interruptible) vs Commit phase (synchronous).
  45. Time Slicing, Cooperative Scheduling, and the WorkLoop.
  46. The 31-bit Lanes Priority Model (`SyncLane`, `TransitionLane`, `IdleLane`).
  47. `useTransition` for separating urgent input from non-urgent filtering.
  48. `useDeferredValue` vs traditional timer debouncing.
  49. Tearing in concurrent state reads and `useSyncExternalStore`.
  50. `<Suspense>` and throwing raw JavaScript Promises under the hood.
  51. How React differentiates thrown Errors from thrown Thenables.
  52. Hydration Mismatch errors and recovery.
  53. Selective Hydration driven by user interaction priority.
  54. What happens when a sync update interrupts a transition.
  55. Fiber node mutation flags (`Placement`, `Update`, `ChildDeletion`).
  56. Why React Scheduler uses `MessageChannel` over `requestIdleCallback`.
  57. Virtual DOM diffing vs Fiber reconciliation.
  58. `flushSync` for emergency synchronous DOM measurements.
  59. `FiberRootNode` vs `HostRoot` differences.
  60. React's Bailout optimization mechanism.

### Part 4: Performance Optimization, Memoization & State Management (Q61 - Q80)

* [`04_react_performance_memoization_and_patterns_qna.md`](./04_react_performance_memoization_and_patterns_qna.md)
  61. Complete list of triggers that cause React components to re-render.
  62. `React.memo` and writing custom `arePropsEqual` functions.
  63. Why `React.memo` fails due to unstable inline function/object references.
  64. Context API performance bottlenecks and context splitting.
  65. Redux Toolkit vs Zustand vs Recoil/Jotai architectural matrix.
  66. How Zustand avoids re-renders via selectors outside Context.
  67. DOM Virtualization (Windowing) for large datasets.
  68. Code Splitting with `React.lazy` and dynamic imports.
  69. Profiler API: `actualDuration` vs `baseDuration`.
  70. Structural Sharing in immutable state and $O(1)$ reference checks.
  71. Immer Proxy-based mutable syntax producing immutable snapshots.
  72. Container vs Presentational component design pattern.
  73. Why declaring components inside other components is an anti-pattern.
  74. Compound Component pattern with implicit context.
  75. Preventing layout thrashing in React DOM measurements.
  76. Throttling vs React 18 `useTransition`.
  77. In-production telemetry profiling with `<Profiler>`.
  78. Cost of anonymous arrow functions in JSX props.
  79. React DevTools "Highlight updates when components render".
  80. Stable callback references with `useCallback`.

### Part 5: React 19, Server Components (RSC) & Fullstack Architecture (Q81 - Q100)

* [`05_react_server_components_and_react19_qna.md`](./05_react_server_components_and_react19_qna.md)
  81. React Server Components (RSC) vs Traditional SSR.
  82. RSC streaming wire protocol and zero-bundle-size components.
  83. When to use the `"use client"` directive boundary.
  84. Server Actions (`"use server"`) and type-safe RPCs.
  85. `useActionState` hook for managing Server Action state.
  86. `useOptimistic` hook for instant optimistic UI updates.
  87. The `use()` API reading Promises and Context conditionally.
  88. React 19 direct `ref` prop and `forwardRef` deprecation.
  89. The React Compiler (React Forget) automatic memoization.
  90. Native Document Metadata (`<title>`, `<meta>`) support.
  91. Server Actions vs standard REST API Routes.
  92. `useFormStatus` hook for nested submit button states.
  93. Passing functions across server/client boundaries.
  94. Server-only poisoning protection with `import 'server-only'`.
  95. Streaming SSR with HTML Suspense chunks.
  96. Why Server Components cannot access browser globals (`window`).
  97. Partial Prerendering (PPR) in Next.js 15 / React 19.
  98. Asynchronous scripts and style hoist management.
  99. Asset preloading functions (`preload`, `preinit`).
  100. Step-by-step React 18 to React 19 migration playbook.

---

## 💻 Machine Coding Challenges

* [`machine_coding_autocomplete_search.md`](./machine_coding_autocomplete_search.md) — Production Autocomplete with debounce, LRU cache, and keyboard navigation.
* [`machine_coding_virtualized_list.md`](./machine_coding_virtualized_list.md) — Custom Virtual Windowing list from scratch.
