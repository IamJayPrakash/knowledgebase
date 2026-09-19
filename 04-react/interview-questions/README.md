# ⚛️ React Interview Questions & Machine Coding Index

> A categorized index of **Hooks Mechanics, Component Optimization, Custom Hook Coding Challenges, and System/Architecture Questions** for Senior React Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific React interview questions in this folder (e.g., `01_custom_use_fetch.md`, `02_virtual_list_component.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. Rapid-Fire / Short Questions
- [ ] `short_questions_reconciliation.md` — Virtual DOM diffing rules, `key` prop role, Fiber node structure.
- [ ] `short_questions_hooks.md` — Rules of Hooks, `useEffect` dependencies, `useRef` vs `useState`.

### 2. Output-Based & Re-render Tracing Snippets
- [ ] `output_state_batching.md` — Tracing state updates in React 18 automatic batching vs asynchronous handlers.
- [ ] `output_useeffect_cleanup.md` — Tracing execution order of component mounts, unmounts, and effect cleanups.

### 3. Custom Hooks & Machine Coding Challenges
- [ ] `coding_use_debounce.md` — Implement `useDebounce` and `useThrottle` custom hooks.
- [ ] `coding_use_fetch_cache.md` — Implement `useFetch` with in-memory caching, status states, and request cancellation (`AbortController`).
- [ ] `coding_infinite_scroll.md` — Implement Infinite Scroll component using `IntersectionObserver`.
- [ ] `coding_virtualized_list.md` — Implement a Virtualized Windowing list component for rendering 100,000 items at 60fps.
- [ ] `coding_autocomplete_search.md` — Build an Autocomplete search box with debouncing, API caching, and keyboard navigation.

### 4. Senior Lead Architecture Scenarios
- [ ] `scenario_micro_frontends.md` — Designing a Micro-Frontend architecture with React, Module Federation, and shared state.
- [ ] `scenario_rsc_hydration.md` — Debugging hydration mismatch errors in Next.js / React Server Components.
