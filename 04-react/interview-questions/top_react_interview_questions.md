# Top Senior React Interview Questions (Architecture & Diagnostics)

---

## 1. What problem does the React Fiber architecture solve?

- Prior to React 16 (Stack Reconciler), reconciliation was recursive and synchronous. If a large component tree updated, the main thread was blocked until the entire tree finished, causing dropped frames and unresponsive inputs.
- Fiber re-implemented reconciliation as a virtual stack frame data structure where each node is a Fiber unit of work.
- Fiber allows **incremental rendering**: pausing, prioritizing, aborting, and resuming work chunks across animation frames using requestIdleCallback/MessageChannel semantics.

---

## 2. Why can't React hooks be called inside conditional statements or loops?

- React maintains hook state internally as a **singly-linked list** attached to the Fiber node (`fiber.memoizedState`).
- On subsequent re-renders, React does NOT lookup hooks by name; it walks the linked list in the **exact sequential order** of execution.
- If a hook is called inside an `if` block that evaluates to false, all subsequent pointer lookups shift out of alignment, corrupting component state across the entire tree.

---

## 3. Explain how the `useId()` hook works in SSR hydration

- In SSR, generating random IDs (`Math.random()`) causes hydration mismatch errors because the server-generated ID and client-generated ID will not match.
- `useId()` generates deterministic, unique IDs based on the component's **hierarchical position in the Fiber tree**, guaranteeing 100% consistency across server and client renders.

---

## 4. What is the difference between controlled and uncontrolled components?

- **Controlled**: Form data is handled by React component state (`value` and `onChange`). React is the single source of truth.
- **Uncontrolled**: Form data is handled directly by the DOM itself. Access values using a `ref` (`inputRef.current.value`). Higher performance for large forms with minimal validation.

---

## 5. How do you prevent layout shifts (CLS) when loading dynamic components?

- Reserve container space using CSS aspect-ratio or min-height.
- Use `<Suspense fallback={<SkeletonHeightWrapper />}>` matching the target dimensions.
- Use `useLayoutEffect` if layout calculations must occur before the browser paints pixels.
