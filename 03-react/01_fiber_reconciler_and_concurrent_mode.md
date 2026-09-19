# React 18 Fiber Architecture & Concurrent Mode

## 1. Executive Summary
React Fiber is a complete rewrite of React's core reconciliation algorithm. It breaks rendering work into incremental units of work (Fibers), enabling React to pause, resume, prioritize, or abort render work to maintain 60fps UI responsiveness.

---

## 2. Fiber Tree & Render Phases
- **Render Phase (Asynchronous):** Traverses Fiber nodes, computes diffs, tags side effects. Work can be interrupted by higher priority events (e.g. user input).
- **Commit Phase (Synchronous):** Applies updates to the actual DOM in a single unbroken pass. Cannot be interrupted.

---

## 3. Senior Interview Q&A
* **Q: How does `useTransition` prevent UI freezing during heavy re-renders?**
  * **A:** `useTransition` marks updates as non-urgent. React yields control to the browser event loop during rendering of non-urgent transitions, ensuring user inputs (typing, clicks) remain responsive.
