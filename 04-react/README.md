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

## 💡 High-Yield Senior Interview Questions Pointers

1. **How does React Fiber enable Concurrent Rendering?**
   * *Answer Pointer:* Fiber breaks reconciliation into small units of work (Fiber nodes). During the Render Phase, React uses `requestIdleCallback` / `scheduler` to execute work incrementally and yield back to the browser thread if high-priority tasks (e.g. user input) arrive.
2. **Why does Context API trigger re-renders in all consumers, and how to fix it?**
   * *Answer Pointer:* Whenever context value reference changes, all components calling `useContext` re-render regardless of whether they use that specific property. Fixes: Split contexts by concern, memoize context value object, or use selector-based state stores like Zustand.
3. **What is the difference between Server Components and Client Components in Next.js / React 19?**
   * *Answer Pointer:* Server Components execute ONLY on the server, outputting a serialized JSON tree to the client with zero JS bundle footprint. Client Components render on server for initial HTML and hydrate on client, allowing interactivity (`useState`, event listeners).
