# Custom Hook Design Patterns and Reusability Architecture

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Custom Hook ek **Modular Power-Tool Attachment** ki tarah hai: Jaise ek drill machine (React Component) mein aap chahe toh lakdi ka bit laga lo (`useDebounce`), lohe ka bit laga lo (`useLocalStorage`), ya concrete ka bit laga lo (`useMediaQuery`). Drill machine ka motor wahi rehta hai, lekin attachment change karke aap naye superpower extract kar lete ho without touching UI presentation.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Rules of Hooks Enforced**: Custom hooks must start with `use` and must follow all rules of hooks (only call at the top level, never call conditionally or in loops).
2. **State Isolation**: Every invocation of a custom hook receives an **isolated, independent instance of state**. Calling `useCounter()` in Component A and Component B does not share state.
3. **Composability**: Custom hooks can consume other built-in or custom hooks (`useState`, `useEffect`, `useRef`).
4. **Returning Ergonomic APIs**:
   - Return a **tuple** (`[value, setter]`) when consumers will likely rename the returned variables (like `useState`).
   - Return an **object** (`{ data, error, isLoading, refetch }`) when returning 3+ properties to allow flexible destructuring.
5. **Handling Memory Leaks & Component Unmounts**: Always handle cleanup in internal `useEffect` hooks and use `AbortController` for network requests.

---

## 📊 3. Visual Architecture Diagram

```
                 CUSTOM HOOK COMPOSITION PIPELINE
                 
      [ Component A: SearchInput ]      [ Component B: FilterDrawer ]
                    │                                 │
                    ▼                                 ▼
      [ useDebounce(query, 300) ]       [ useDebounce(filter, 300) ]
                    │                                 │
                    ▼                                 ▼
       (Isolated Timer Instance 1)       (Isolated Timer Instance 2)
                    │                                 │
                    ▼                                 ▼
       Delayed State Update              Delayed State Update
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
import { useState, useEffect, useRef, useCallback } from "react";

// ==========================================
// 1. Production useDebounce Hook
// ==========================================
export function useDebounce<T>(value: T, delayMs: number = 300): T {
  // Line 8: State to store debounced value
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Line 12: Set timer to update value after delay
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    // Line 17: Cleanup timer if value or delay changes before timeout completes
    return () => {
      clearTimeout(timer);
    };
  }, [value, delayMs]);

  return debouncedValue;
}

// ==========================================
// 2. Production useLocalStorage Hook with Event Sync
// ==========================================
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  // Line 31: Lazy initializer reading from localStorage
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Line 42: Stable setter function
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        setStoredValue((prev) => {
          const nextValue = value instanceof Function ? value(prev) : value;
          window.localStorage.setItem(key, JSON.stringify(nextValue));
          return nextValue;
        });
      } catch (error) {
        console.error(`Error saving localStorage key "${key}":`, error);
      }
    },
    [key]
  );

  return [storedValue, setValue];
}
```

---

## 🎯 5. The "Interview Pitch"
> "Custom hooks are the fundamental abstraction primitive in modern React for encapsulating and sharing stateful logic across components without mutating component hierarchies or relying on Higher-Order Components. They allow composing primitive hooks into domain-specific workflows—such as debouncing values, synchronizing local storage, or orchestrating data fetches with automatic abort controllers. To design robust custom hooks, we maintain strict dependency arrays, return objects for extensible APIs, and guarantee proper teardown cleanup upon unmount."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: Multiple development teams duplicated data-fetching code across 40 different dashboard pages. Several components failed to abort inflight requests on unmount, resulting in race conditions where slow responses from old searches overwrote newer search results.
- **Task**: Unify data-fetching logic and permanently eliminate asynchronous race conditions.
- **Action**: We engineered an internal `useFetch<T>(url, options)` custom hook with integrated `AbortController` cancellation, caching, and retry backoff. When the URL changed or the component unmounted, the previous controller called `.abort()`.
- **Result**: Eliminated 100% of data race conditions and reduced redundant network traffic by 28% through built-in request deduplication.
