# React Master Interview Bank: Part 2 (Q21 - Q40)
## Hooks Internals, State Batching & Lifecycle Synchronization

---

### Q21: Why must React Hooks only be called at the top level? How are Hooks stored internally in Fiber?
**Answer:**
- **The Rule:** Don't call Hooks inside loops, conditions, or nested functions.
- **Under the Hood:**
  - React does **not** identify hooks by names or string keys.
  - In each Fiber node, hooks are stored as a **singly linked list** on the `fiber.memoizedState` property:
    `Hook 1 -> next -> Hook 2 -> next -> Hook 3 -> null`.
  - React maintains an internal pointer `workInProgressHook`. On each render, React walks this linked list sequentially from the head node.
  - If a hook is placed inside an `if` condition and skipped on a subsequent render, the hook index pointer shifts: Hook 3 reads state intended for Hook 2, corrupting component state and throwing an internal invariant error.

```
FiberNode.memoizedState
   │
   ▼
[ Hook 1: useState ] ──next──► [ Hook 2: useEffect ] ──next──► [ Hook 3: useRef ] ──► null
```

---

### Q22: What is Automatic Batching in React 18, and how does it differ from React 17?
**Answer:**
- **Batching:** Grouping multiple state updates into a single re-render to prevent unnecessary intermediate paints.
- **In React 17:**
  - Updates were batched **only inside native React event handlers** (`onClick`, `onChange`).
  - Updates inside `setTimeout`, `fetch` promises, or native DOM listeners were **not batched** (each `setState` triggered an independent synchronous re-render).
- **In React 18 (Automatic Batching with `createRoot`):**
  - **All** state updates are batched automatically regardless of origin (Promises, `setTimeout`, intervals, async/await, or native event handlers).
  - To opt out of batching for emergency synchronous DOM reads, use `flushSync(() => setState(...))`.

```javascript
// Inside a fetch promise in React 18:
fetch("/api/user").then(() => {
  setIsLoading(false);
  setUser(data);
  // In React 17: 2 separate re-renders!
  // In React 18: Exactly 1 single batched re-render!
});
```

---

### Q23: What is the difference between passing a direct value vs a functional update to `setState`?
**Answer:**
- **Direct Value (`setCount(count + 1)`):** Reads `count` from the current render's closure. If called multiple times within the same event loop tick, each call references the same snapshot:
  ```javascript
  setCount(count + 1); // count = 0 -> sets to 1
  setCount(count + 1); // count = 0 -> sets to 1
  setCount(count + 1); // count = 0 -> sets to 1 (Result: 1, not 3!)
  ```
- **Functional Update (`setCount(prev => prev + 1)`):** React queues update functions into an internal update queue (`fiber.updateQueue`). During reconciliation, React passes the latest pending state from the previous update to the next, guaranteeing correct incremental updates:
  ```javascript
  setCount(prev => prev + 1); // prev = 0 -> 1
  setCount(prev => prev + 1); // prev = 1 -> 2
  setCount(prev => prev + 1); // prev = 2 -> 3 (Result: 3!)
  ```

---

### Q24: What is Lazy State Initialization in `useState`?
**Answer:**
- If you pass an expression directly to `useState`: `useState(computeExpensiveValue())`, the expensive function executes on **every single re-render**, even though React only uses the initial value on mount.
- **Lazy Initialization:** Pass a function definition: `useState(() => computeExpensiveValue())`. React will execute this callback **strictly once during the initial mount phase** and ignore it on all subsequent re-renders.

```javascript
// ❌ EXPENSIVE: Parses localStorage on every render!
const [token, setToken] = useState(localStorage.getItem("auth_token"));

// ✅ OPTIMAL: Evaluated once on mount only!
const [token, setToken] = useState(() => localStorage.getItem("auth_token"));
```

---

### Q25: What are the differences between `useEffect`, `useLayoutEffect`, and `useInsertionEffect`?
**Answer:**
```
                     RENDER PHASE
                          │
                          ▼
            DOM Mutated (Virtual DOM applied)
                          │
                          ▼
             [ 1. useInsertionEffect ]  ──► Injects CSS-in-JS styles before layout calculation
                          │
                          ▼
                 Browser Layout Computed
                          │
                          ▼
              [ 2. useLayoutEffect ]   ──► Runs SYNCHRONOUSLY before browser paints (DOM measurement)
                          │
                          ▼
                   BROWSER PAINTS UI
                          │
                          ▼
                 [ 3. useEffect ]      ──► Runs ASYNCHRONOUSLY after browser paints (I/O, APIs)
```

1. **`useEffect`**: Asynchronous. Fires **after** the browser paints the screen. Non-blocking; ideal for data fetching, event subscriptions, and analytics.
2. **`useLayoutEffect`**: Synchronous. Fires **after DOM mutation but before the browser paints**. Used to read DOM layout (e.g. element dimensions/positions via `getBoundingClientRect`) and mutate the DOM before the user sees a flicker.
3. **`useInsertionEffect`**: Fires **before any DOM mutations occur**. Strictly designed for CSS-in-JS library authors (e.g. Styled Components, Emotion) to inject `<style>` tags before React reads layout.

---

### Q26: How does `useRef` work and why does mutating `.current` not trigger a re-render?
**Answer:**
- `useRef(initialValue)` returns a mutable plain JavaScript object: `{ current: initialValue }`.
- React persists this exact same object instance across every render of the component on the Fiber node's hook list.
- **Why no re-render:** Unlike `useState`, mutating `ref.current = newValue` is a simple property assignment in memory. It does **not** call React's scheduling engine (`scheduleUpdateOnFiber`), so React has no awareness that an update occurred and does not trigger reconciliation.
- **Use Cases:** Storing DOM element references, tracking previous prop/state values, storing interval IDs or timeout handles.

---

### Q27: How do you store the previous state or props using `useRef`?
**Answer:**
Because `useEffect` runs **after** render and paint, we can capture the current state inside an effect so it becomes the "previous" state on the subsequent render:

```javascript
import { useRef, useEffect } from "react";

function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value; // Updated after render
  }, [value]);

  return ref.current; // Returns value from previous render
}
```

---

### Q28: What is a Stale Closure in React hooks, and how do you fix it?
**Answer:**
- **Stale Closure:** Occurs when a closure (inside `useEffect`, `useCallback`, or a timer) captures variables from a specific render snapshot and does not update when those variables change in future renders.
- **Common Cause:** Omitting variables from the dependency array (`[]`).
- **Fixes:**
  1. Add missing dependencies to the dependency array.
  2. Use functional state updates: `setCount(prev => prev + 1)` instead of `setCount(count + 1)`.
  3. Store changing mutable values in a `useRef`.

```javascript
// ❌ BUG (Stale Closure): count is frozen at 0 forever!
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1); // Always 0 + 1 = 1!
  }, 1000);
  return () => clearInterval(id);
}, []); // Missing count!

// ✅ FIX: Functional update accesses latest pending state
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1);
  }, 1000);
  return () => clearInterval(id);
}, []);
```

---

### Q29: When should you prefer `useReducer` over `useState`?
**Answer:**
Use `useReducer` when:
1. **Complex State Logic:** The state object has multiple sub-values (e.g. multi-step wizard, form with 15 fields).
2. **Co-dependent State Updates:** Updating one piece of state depends on the values of other pieces of state.
3. **Predictable State Transitions:** Wanting to enforce state transitions via explicit action types (`FETCH_INIT`, `FETCH_SUCCESS`, `FETCH_ERROR`).
4. **Deep Prop Passing Optimization:** `dispatch` is guaranteed to have a **stable identity across renders**, allowing you to pass `dispatch` down via Context instead of individual callback functions.

---

### Q30: What is `useImperativeHandle` and why should it be used sparingly?
**Answer:**
- `useImperativeHandle(ref, createHandle, [deps])` customizes the instance value that is exposed to parent components when using `ref` with `forwardRef`.
- **Purpose:** Restricts what parents can do with a DOM node, exposing a clean, limited API (e.g. exposing only `.focus()` or `.scrollIntoView()` instead of the entire raw DOM node).
- **Why use sparingly:** Violates declarative principles; forces imperative child manipulation from parents.

```javascript
import { forwardRef, useImperativeHandle, useRef } from "react";

const CustomInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ""; }
  }));

  return <input ref={inputRef} />;
});
```

---

### Q31: What is `useId` and what problem does it solve in SSR and Accessibility?
**Answer:**
- `const id = useId()` generates a unique, stable identifier across both client and server renders.
- **Problem Solved:** Prior to `useId`, using `Math.random()` or global counters created **Hydration Mismatch Errors** because the client and server generated different IDs for the same element.
- **Accessibility:** Generates stable IDs for linking `<label htmlFor={id}>` and `<input id={id} />` or `aria-describedby`.

---

### Q32: Why should you avoid updating state inside the body of a component render?
**Answer:**
- Updating state inside the component render body (outside of an effect or event handler) schedules an immediate re-render.
- If done unconditionally, it causes an **infinite render loop**, throwing `Error: Too many re-renders. React limits the number of renders to prevent an infinite loop`.

---

### Q33: How does React detect when to run the cleanup function in `useEffect`?
**Answer:**
- The cleanup function returned by `useEffect` executes in two scenarios:
  1. **Before the effect runs again:** If dependencies change between renders, React runs the **previous render's cleanup function** first, and then executes the new effect.
  2. **When the component unmounts:** React executes the final cleanup function before removing the Fiber node from the tree.

---

### Q34: Can `useEffect` callback be declared as `async`? Why or why not?
**Answer:**
**No.** The callback passed to `useEffect` must return either **nothing (`undefined`) or a cleanup function**.
If you declare it as `async`:
`useEffect(async () => { ... })`
An `async` function automatically returns a **Promise**. A Promise cannot be invoked as a cleanup function by React (`promise() is not a function`), throwing a runtime error.
- **Solution:** Declare an internal async function and invoke it immediately:

```javascript
useEffect(() => {
  let isMounted = true;

  async function loadData() {
    const data = await fetchUser();
    if (isMounted) setUser(data);
  }
  loadData();

  return () => { isMounted = false; }; // Clean up!
}, []);
```

---

### Q35: What is `useDebugValue` and when should custom hook authors use it?
**Answer:**
- `useDebugValue(value, formatFn)` displays a custom label for custom hooks inside the **React DevTools** component tree.
- It helps library authors (e.g. React Query, Zustand) display internal hook status (e.g. "Online", "Cached", "Pending") for easier developer debugging.

---

### Q36: What happens if an error occurs inside an effect cleanup function?
**Answer:**
- An error thrown inside a cleanup function is treated as a fatal unhandled error in the component lifecycle.
- It will bubble up to the nearest **Error Boundary**. If no Error Boundary catches it, the entire React component tree will unmount.

---

### Q37: How do you implement a custom `useDebounce` hook?
**Answer:**
```javascript
import { useState, useEffect } from "react";

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cancel timer if value or delay changes before timeout expires
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

---

### Q38: How do you implement a custom `useLocalStorage` hook with cross-tab synchronization?
**Answer:**
```javascript
import { useState, useEffect } from "react";

function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (e) {
      console.error(e);
    }
  };

  // Cross-tab synchronization via storage event:
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === key && e.newValue) {
        setStoredValue(JSON.parse(e.newValue));
      }
    };
    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, [key]);

  return [storedValue, setValue];
}
```

---

### Q39: What is the purpose of `useCallback` and when is it completely useless?
**Answer:**
- **Purpose:** Memoizes a callback function definition between renders, returning the same function memory reference as long as dependencies have not changed.
- **When Useful:**
  1. Passing callbacks to child components wrapped in `React.memo` (preserves shallow `prevProps === nextProps`).
  2. The function is used as a dependency in another hook's dependency array (e.g. `useEffect(..., [fetchData])`).
- **When Completely Useless:**
  1. Wrapping callbacks passed to native HTML elements (`<button onClick={useCallback(...)}>`). Native DOM elements do not perform shallow prop comparisons; allocating `useCallback` and dependency arrays here adds pure computational overhead with zero benefit.
  2. Passing callbacks to unmemoized child components (the child re-renders regardless).

---

### Q40: What is the purpose of `useMemo` and what is its cost?
**Answer:**
- **Purpose:** Caches the **result** of an expensive computation between renders: `const memoized = useMemo(() => compute(a), [a]);`.
- **Cost:**
  `useMemo` is not free. It consumes memory to store the cached value and dependency array, and spends CPU cycles comparing dependencies on every render.
  - *Rule of Thumb:* Only use `useMemo` for computationally heavy operations (e.g., sorting/filtering thousands of objects) or to maintain referential equality for objects passed to memoized children or dependencies.
