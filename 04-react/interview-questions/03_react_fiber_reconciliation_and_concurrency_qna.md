# React Master Interview Bank: Part 3 (Q41 - Q60)
## Fiber Architecture, Reconciliation & Concurrent Mode

---

### Q41: What was the Stack Reconciler in React 15 and why was it completely rewritten?
**Answer:**
- **React 15 Stack Reconciler:** Used recursive function calls to traverse and diff the component tree synchronously.
- **The Problem (Call Stack Blocking):**
  Once a reconciliation started, it could **not be paused, interrupted, or aborted**.
  If a complex component tree took 100ms to reconcile, the single JavaScript main thread was blocked for the entire duration.
  - Browser could not process user input (typing in input froze), click handlers were delayed, and animations dropped frames (jank).
- **The Solution:** **React Fiber (React 16+)**, which replaced recursive stack frames with a heap-allocated linked list of Fiber nodes that can pause, resume, prioritize, and abort work.

---

### Q42: What is a Fiber Node? What are its primary structural pointers?
**Answer:**
A **Fiber** is a plain JavaScript object that represents a unit of work and a 1-to-1 mapping with a React component or DOM node.
Unlike recursive trees with arrays of children, Fiber uses a **singly linked list traversal structure**:

```
           [ Parent Fiber ] (return)
                 │
                 ▼ (child)
          [ First Child ] ──(sibling)──► [ Second Child ] ──(sibling)──► [ Third Child ]
                 │                             │                              │
                 └──────────────(return)───────┴──────────────(return)────────┘
```

**Key Fiber Pointers:**
1. **`child`**: Points to the component's first immediate child.
2. **`sibling`**: Points to the next sibling fiber on the same level.
3. **`return`**: Points back to the parent fiber (the fiber to return to when work on the current node finishes).
4. **`alternate`**: Points to the corresponding fiber in the opposing tree (links `current` and `workInProgress` trees).
5. **`memoizedState`**: Holds the component's state or the head of the hooks linked list.
6. **`lanes`**: Bitmask representing the scheduled priority level of this fiber's updates.

---

### Q43: What is Double Buffering in React Fiber?
**Answer:**
Borrowed from graphics rendering (video games):
React maintains **two complete Fiber trees in memory simultaneously**:
1. **`current` Tree:** The tree currently displayed on screen and reflected in the real DOM.
2. **`workInProgress` (WIP) Tree:** The tree being constructed and reconciled in the background during the Render phase.

```
 [ Real DOM Screen ]
        ▲
        │
 [ Current Fiber Tree ] ◄──────────── alternate ───────────► [ WorkInProgress Tree ]
                                                             (Constructed in background)
```

**The Commit Swap:**
During the Render phase, React performs all calculations and diffing on the `workInProgress` tree. Once all work completes cleanly, React swaps a single root pointer: `fiberRoot.current = workInProgress`. The WIP tree instantly becomes the `current` tree in a single atomic pointer change.

---

### Q44: What are the two distinct phases of React Fiber execution?
**Answer:**
| Dimension | Render Phase | Commit Phase |
| :--- | :--- | :--- |
| **Nature** | **Asynchronous, Interruptible & Concurrent**. | **Synchronous & Uninterruptible**. |
| **Activities** | Computes virtual DOM diffing, calls component functions, resolves hooks, identifies DOM mutations, flags fibers (`Placement`, `Update`, `Deletion`). | Mutates the real browser DOM, executes `useLayoutEffect` synchronously, swaps tree pointers, executes `useEffect` asynchronously. |
| **Main Thread Impact** | Yields control back to the browser at ~5ms intervals to keep UI responsive. | Runs quickly to avoid visual tearing; cannot be paused. |
| **Side Effects Allowed?** | ❌ NO. Must be pure and side-effect free (can be aborted/re-run). | ✅ YES. Applies real DOM changes and lifecycle effects. |

---

### Q45: How does Time Slicing and Cooperative Scheduling work in React Fiber?
**Answer:**
- React Fiber runs a loop called the **WorkLoop**:
  ```javascript
  function workLoopConcurrent() {
    while (workInProgress !== null && !shouldYield()) {
      performUnitOfWork(workInProgress);
    }
  }
  ```
- **`shouldYield()`:** React monitors elapsed time using `performance.now()`. If a chunk of work exceeds **~5ms** (frame budget), `shouldYield()` returns `true`.
- React suspends execution, saves its current pointer in `workInProgress`, and yields control back to the browser via a micro/macro task scheduled on **`MessageChannel`** (`port.postMessage`).
- The browser processes user keystrokes, layout, and paints. Once the main thread is idle, the `MessageChannel` callback resumes the WorkLoop exactly where it paused.

---

### Q46: What is the Lanes Priority Model in React 18?
**Answer:**
React represents update priorities using a **31-bit integer bitmask** called **Lanes**:
- Each bit corresponds to a priority category. Bitwise operations (`&`, `|`) allow instant checking, merging, and masking of priorities in $O(1)$ time.

**Major Lanes Priorities (Highest to Lowest):**
1. **`SyncLane` (Highest):** Immediate updates (controlled input typing, `flushSync`). Cannot be interrupted.
2. **`InputContinuousLane`:** Continuous user gestures (dragging, sliders, hover effects).
3. **`DefaultLane`:** Standard updates (`setState` inside clicks or timers).
4. **`TransitionLane`:** Low-priority non-urgent UI transitions (`startTransition`). Can be interrupted by higher-priority lanes.
5. **`IdleLane` (Lowest):** Offscreen pre-rendering or background telemetry.

---

### Q47: What is `useTransition` and what problem does it solve?
**Answer:**
- `const [isPending, startTransition] = useTransition()` separates **urgent updates** from **non-urgent (transition) updates**.
- **The Problem:** When a user types in a search input that filters a list of 10,000 items, updating the input text and filtering the list traditionally happened at the same priority, causing the typing input to lag.
- **With `useTransition`:**
  - Updating the text input remains **Urgent (SyncLane)** $\to$ Instant typing response!
  - Filtering the 10,000 items is wrapped in `startTransition(() => setFilter(val))` $\to$ Marked as **TransitionLane**.
  - If the user types another character while the filter is rendering, React **aborts the in-progress filter calculation** and renders the new keystroke immediately!

```javascript
function SearchFilter() {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("");
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    setQuery(e.target.value); // Urgent: Instant input update
    startTransition(() => {
      setFilter(e.target.value); // Non-urgent: Interruptible filter render
    });
  };

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <HeavyList query={filter} />
    </div>
  );
}
```

---

### Q48: What is `useDeferredValue` and how does it differ from Debouncing?
**Answer:**
- `const deferredValue = useDeferredValue(value)` returns a deferred copy of `value` that "lags behind" during heavy re-renders.
- **Difference from Debouncing:**
  - **Debouncing:** Uses a fixed arbitrary timer (e.g. 300ms). Even on a super-fast 16-core M3 Max computer, the user is forced to wait 300ms. On a slow phone, 300ms may still drop frames.
  - **`useDeferredValue`:** **Hardware-adaptive and time-sliced**. On fast computers, it updates almost instantly (0-2ms). On slow devices, it yields to user interaction and updates as soon as the main thread has free time. There is **zero fixed delay**.

---

### Q49: What is Tearing in Concurrent React and what is `useSyncExternalStore`?
**Answer:**
- **Tearing:** A visual inconsistency where different UI components render with **different versions of the same state** within the same visual paint frame.
- **How it happens in Concurrent Mode:**
  Because the render phase is interruptible, a component can read state at Version 1, then React yields to the browser. An external store (like Redux or a global variable) updates to Version 2. When React resumes, a sibling component reads Version 2. Both are rendered on screen simultaneously with clashing data!
- **Solution:** **`useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)`**.
  Guarantees that reads from external non-React stores are synchronous during the render phase, completely eliminating tearing.

```javascript
import { useSyncExternalStore } from "react";

// Subscribing to browser online/offline status cleanly:
function useOnlineStatus() {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener("online", callback);
      window.addEventListener("offline", callback);
      return () => {
        window.removeEventListener("online", callback);
        window.removeEventListener("offline", callback);
      };
    },
    () => navigator.onLine // Client snapshot
  );
}
```

---

### Q50: What is Suspense and how does it work under the hood with Promises?
**Answer:**
- `<Suspense fallback={<Loading />}>` allows components to "wait" for something before rendering (code-splitting, data fetching).
- **Under the Hood (Throwing Promises!):**
  1. A child component suspended on data fetching **throws a raw JavaScript Promise** (`throw promise;`).
  2. React catches this thrown promise in the nearest `<Suspense>` boundary (similar to an Error Boundary catching an Error).
  3. React pauses rendering of that subtree and displays the `fallback` UI.
  4. React attaches a `.then()` handler to the thrown Promise.
  5. When the Promise resolves, React retries rendering the suspended child component.

---

### Q51: How does React differentiate between a component throwing an Error vs throwing a Promise?
**Answer:**
During the Render phase `renderWithHooks()`:
React executes the component in a `try...catch` block.
- If caught object is an instance of `Error` (or lacks a `.then` method) $\to$ React routes it to the nearest **Error Boundary**.
- If caught object is a "Thenable" (an object or function with a `.then` method) $\to$ React routes it to the nearest **Suspense Boundary**.

---

### Q52: What is Hydration Mismatch and how does Concurrent React handle it?
**Answer:**
- **Hydration:** The process where client-side React attaches event listeners to pre-rendered HTML sent from the server, turning static HTML into an interactive app.
- **Hydration Mismatch:** Occurs when the server-rendered HTML markup differs from what the client produces during initial render (e.g., using `new Date()` or checking `window.innerWidth`).
- **React 18/19 Behavior:**
  React logs a descriptive console warning showing the exact mismatch diff, discards the mismatched server HTML subtree, and re-renders that specific subtree on the client (Selective Hydration).

---

### Q53: What is Selective Hydration in React 18?
**Answer:**
- In React 17 SSR, hydration was **all-or-nothing**: the entire HTML tree had to download and hydrate before any part of the page became interactive.
- In React 18 with `<Suspense>`, React enables **Selective Hydration**:
  1. Parts of the page wrapped in `<Suspense>` can stream and hydrate independently.
  2. **User Interaction-Driven Priority:** If a user clicks a button inside a component that hasn't hydrated yet, React **prioritizes hydrating that specific component first**, making it interactive ahead of other background components!

---

### Q54: What happens if a high-priority update interrupts a transition update in Fiber?
**Answer:**
1. React was midway through reconciling a `TransitionLane` (WIP tree).
2. A `SyncLane` event occurs (user types in an input).
3. React aborts the WIP tree traversal.
4. It resets `workInProgress` to the current tree state and immediately reconciles the `SyncLane` update.
5. It commits the `SyncLane` update to the real DOM.
6. Once the main thread is clear, React restarts or resumes the `TransitionLane` calculation with the latest state.

---

### Q55: What are the flags / effect tags on a Fiber node (`Placement`, `Update`, `ChildDeletion`)?
**Answer:**
- During the Render phase, React calculates what needs to happen to real DOM nodes and sets bitwise flags on the fiber's `flags` property:
  - `Placement (0b0000000000000000000000000000010)`: Insert new DOM node into parent.
  - `Update (0b0000000000000000000000000000100)`: Mutate existing DOM attributes or text content.
  - `ChildDeletion (0b0000000000000000000000000001000)`: Remove DOM node from parent.
- During the Commit phase, React simply iterates over fibers with flags and applies the exact DOM mutations in a single pass.

---

### Q56: Why did React move from `requestIdleCallback` to `MessageChannel` for its Scheduler?
**Answer:**
1. **Low Frequency:** `requestIdleCallback` only fires when the browser has idle time, capping execution frequency to ~20fps (insufficient for smooth 60fps animations).
2. **Browser Inconsistency:** Safari never supported `requestIdleCallback`.
3. **Tab Throttling:** `requestIdleCallback` is heavily throttled or halted when switching browser tabs.
- `MessageChannel` provides macro-task scheduling that runs with near-zero latency (~0ms delay) across all browsers.

---

### Q57: What is the difference between Fiber reconciliation and Virtual DOM diffing?
**Answer:**
- **Virtual DOM diffing:** The conceptual comparison between two JSON-like component trees.
- **Fiber reconciliation:** The actual operational implementation. It combines virtual DOM diffing with a stateful heap-allocated graph of Fiber nodes that manages component instances, hooks, scheduling priority, incremental time slicing, and DOM mutation flags.

---

### Q58: What is `flushSync` and when is it strictly necessary?
**Answer:**
- `flushSync(() => { setState(...) })` forces React to immediately flush any pending updates inside the callback **synchronously** to the real DOM.
- **Use Case:** When you must immediately measure or manipulate the DOM based on state (e.g. scrolling to the bottom of a chat log immediately after adding a message):

```javascript
import { flushSync } from "react-dom";

function sendMessage(msg) {
  flushSync(() => {
    setMessages(prev => [...prev, msg]);
  });
  // DOM is guaranteed to be updated synchronously here:
  chatEndRef.current.scrollIntoView({ behavior: "smooth" });
}
```

---

### Q59: What is the Root Fiber (`FiberRootNode`) vs `HostRoot`?
**Answer:**
- **`FiberRootNode`**: The root of the entire React runtime instance (created by `createRoot`). Contains the pointer to `current`, the scheduler queues, and lane bitmasks.
- **`HostRoot`**: The top-level Fiber node of the component tree representing the container DOM element (`<div id="root">`).

---

### Q60: Can you explain React's `bailout` mechanism during reconciliation?
**Answer:**
- When React visits a Fiber node during the render phase:
  1. It checks: `oldProps === newProps` and `fiber.lanes` has no pending updates.
  2. If both conditions are met, React triggers a **Bailout**: it clones the old fiber node, skips invoking the component function, and does not re-render that component or traverse into unchanged children, saving significant CPU cycles.
