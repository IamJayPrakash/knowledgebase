# -*- coding: utf-8 -*-
"""
Generator for Track 3: React & Next.js Deep Dive & Interview Questions
Generates:
1. 03-react/03_virtual_dom_jsx_and_diffing.md
2. 03-react/05_effect_hooks_useeffect_uselayouteffect.md
3. 03-react/06_memoization_usememo_usecallback_react_memo.md
4. 03-react/07_context_api_and_state_management.md
5. 03-react/08_custom_hooks_patterns.md
6. 03-react/09_suspense_and_streaming_ssr.md
7. 03-react/10_react19_actions_use_hook_compiler.md
8. 03-react/interview-questions/top_react_interview_questions.md
9. 03-react/interview-questions/machine_coding_autocomplete_search.md
10. 03-react/interview-questions/machine_coding_virtualized_list.md
11. 04-frontend-frameworks/nextjs/02_server_actions_and_mutations.md
12. 04-frontend-frameworks/nextjs/03_caching_and_revalidation_deep_dive.md
13. 04-frontend-frameworks/nextjs/04_middleware_and_authentication.md
14. 04-frontend-frameworks/nextjs/interview-questions/nextjs_top_interview_questions.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "03-react", "03_virtual_dom_jsx_and_diffing.md"): """# Virtual DOM, JSX Compilation, and the Reconciliation Diffing Algorithm

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Socho aapko apne ghar ka interior renovate karna hai.
Real DOM ek **Asli Eent-Patthar ka Ghar** hai: Agar aap seedhe wall girane lagoge, toh bohot dhool udegi, kharcha hoga, aur padosi pareshan honge (Browser Layout reflow and Repaint is very expensive!).
Virtual DOM ek **Architect ka 3D Blue-Print Model** hai jo laptop ki memory mein rehta hai. Architect purane blueprint aur naye blueprint ko compare karta hai (**Diffing Algorithm**). Wo dekhta hai ki sirf hall ka parda badalna hai, kitchen ko chhedne ki zaroorat nahi. Fir wo carpenter ko bolta hai: "Jaakar sirf parda badal do" (**Batched Minimal Real DOM update**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **JSX is Syntactic Sugar**: JSX does not run in the browser. Babel/SWC compiles `<div className="box">Hi</div>` into `_jsx("div", { className: "box", children: "Hi" })`.
2. **React Elements are Plain Objects**: A React element is an immutable JS object containing `$$typeof: Symbol.for('react.element')` (to prevent XSS injection via JSON), `type`, `props`, and `key`.
3. **The Heuristic Diffing Algorithm**: An optimal tree diff is $O(N^3)$. React achieves $O(N)$ based on two assumptions:
   - Elements of different types produce completely different subtrees (React tears down the old tree completely).
   - The developer can hint at which child elements are stable across renders with a unique `key` prop.
4. **The `key` Prop Traps**:
   - Using array index as `key` breaks component local state when sorting, inserting, or deleting items from the middle or front of an array.
   - Keys must be stable, unique among siblings, and predictable.
5. **Fiber Work Phases**:
   - **Render Phase (Reconciliation)**: Pure, asynchronous, can be paused/aborted. Calculates the effect list.
   - **Commit Phase**: Synchronous, mutates the real DOM, executes layout effects.

---

## 📊 3. Visual Architecture Diagram

```
                 REACT RECONCILIATION PIPELINE
                 
   Component State Change ──► Re-render invoked
                                   │
                                   ▼
                       Generate New VDOM Tree
                                   │
                                   ▼
         [ Old VDOM Fiber Tree ] vs [ New VDOM Elements ]
                                   │
               (React Heuristic O(N) Diffing Algorithm)
                                   │
                                   ▼
                    Generate Fiber Mutation List
                        (Placement, Update, Deletion)
                                   │
                                   ▼
                       [ SYNCHRONOUS COMMIT PHASE ]
                                   │
                    Batch Update to Host Real DOM
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```jsx
import React, { useState } from "react";

// Line 4: Component demonstrating the Danger of Index as Key
export function BuggyTodoList() {
  // Line 6: State with initial tasks
  const [todos, setTodos] = useState([
    { id: "todo-1", title: "Write Unit Tests" },
    { id: "todo-2", title: "Review PR #42" }
  ]);

  const prependTask = () => {
    // Line 13: Inserting a new item at the FRONT (index 0)
    const newTask = { id: `todo-${Date.now()}`, title: "Urgent Hotfix" };
    setTodos([newTask, ...todos]);
  };

  return (
    <div>
      <button onClick={prependTask}>Prepend Task</button>
      
      {/* ANTI-PATTERN: Using index as key */}
      <h4>Buggy List (index as key - local state bleeds!)</h4>
      <ul>
        {todos.map((todo, index) => (
          // Line 26: If child has an uncontrolled input, index 0 retains old input state!
          <li key={index}>
            <span>{todo.title}</span>
            <input placeholder="Personal task notes" />
          </li>
        ))}
      </ul>

      {/* GOLD STANDARD: Using stable, unique entity ID */}
      <h4>Correct List (stable unique id as key)</h4>
      <ul>
        {todos.map((todo) => (
          // Line 39: Fiber reconciliation accurately moves DOM nodes without destroying state
          <li key={todo.id}>
            <span>{todo.title}</span>
            <input placeholder="Personal task notes" />
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "The Virtual DOM is a lightweight, in-memory representation of the real DOM tree composed of plain JavaScript objects. When state updates occur, React generates a new Virtual DOM tree and executes reconciliation using a heuristic $O(N)$ diffing algorithm. If element types differ, React destroys and recreates the subtree. If types match, it updates only the changed attributes. Keys are critical because they give sibling elements persistent identities across renders. Using array indices as keys creates severe UI bugs when arrays are mutated, as React erroneously maps state to the index position rather than the specific entity."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a live stock trading dashboard, traders reported that buy/sell input quantities were unexpectedly shifting to the wrong ticker rows whenever new stock alerts were prepended to the top of the table.
- **Task**: Eliminate input state misalignment without causing expensive full-table re-renders.
- **Action**: We audited the table component and found `key={index}` on table rows. When a new stock alert arrived at index 0, React preserved the input DOM nodes at each index and simply changed the row labels, causing user inputs to detach from their original stocks. We switched the key to `key={stock.isinCode}`.
- **Result**: Completely eradicated input bleeding bugs, protected traders from executing erroneous stock orders, and improved list reconciliation performance by 35%.
""",

    os.path.join(BASE_DIR, "03-react", "05_effect_hooks_useeffect_uselayouteffect.md"): """# `useEffect` vs `useLayoutEffect`: Execution Timing & Screen Flicker Prevention

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Socho aap ek theatre play ke director ho.
`useLayoutEffect` **Parda Uthne Se Pehle (Before Browser Paint)** ka kaam hai: Agar stage par kisi actor ki cap tedi hai, toh director parda uthne se pehle hi use theek kar deta hai taaki audience ko kuch ajeeb na dikhe (Zero visual flicker).
`useEffect` **Parda Uthne Ke Baad (After Browser Paint)** ka kaam hai: Play chal raha hai, parda uth chuka hai, aur background mein sound team speaker ki volume check kar rahi hai ya lighting log save kar rahi hai (Asynchronous non-blocking network calls / logging).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`useEffect` (Asynchronous & Non-blocking)**:
   - Runs **after** the browser has painted the DOM changes to the screen.
   - Recommended for 99% of side effects: data fetching, event subscriptions, timers, logging.
2. **`useLayoutEffect` (Synchronous & Render-Blocking)**:
   - Runs synchronously **after DOM mutations but before the browser paints**.
   - Use exclusively when reading layout measurements (`getBoundingClientRect`) and mutating the DOM synchronously to prevent visual flickering.
3. **SSR Warning**: `useLayoutEffect` causes warnings during Server-Side Rendering (Next.js) because the server has no layout or paint phase. Use `useEffect` or safe layout hooks for SSR.
4. **Cleanup Execution**:
   - The cleanup function runs **before** the effect re-runs with new dependencies, and during component unmounting.
   - Crucial for aborting fetch requests (`AbortController`), clearing intervals, and removing listeners.
5. **Strict Mode Double Invocation**: In React 18+ development mode, effects are mounted -> unmounted -> remounted immediately to ensure cleanup resilience.

---

## 📊 3. Visual Architecture Diagram

```
                    BROWSER RENDER TIMELINE
                    
  [ React Commit Phase ] ──► Real DOM mutated in memory
                                  │
                                  ▼
                     [ useLayoutEffect executes ] ◄── (BLOCKS BROWSER PAINT!)
                                  │
                                  ▼
                     [ Browser Paints Screen (User sees UI) ]
                                  │
                                  ▼
                     [ useEffect executes ] ◄── (NON-BLOCKING, ASYNCHRONOUS)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```jsx
import React, { useState, useRef, useLayoutEffect, useEffect } from "react";

// Line 4: Tooltip component demonstrating useLayoutEffect to prevent flicker
export function SmartTooltip({ targetRect, content }) {
  const tooltipRef = useRef(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  // Line 10: useLayoutEffect measures tooltip DOM dimensions BEFORE the browser paints
  useLayoutEffect(() => {
    if (!tooltipRef.current) return;

    // Line 14: Measure exact rendered tooltip height and width
    const { height, width } = tooltipRef.current.getBoundingClientRect();

    // Line 17: Calculate repositioned coordinates (e.g. flip above if screen bottom reached)
    const calculatedTop = targetRect.bottom + height > window.innerHeight
      ? targetRect.top - height - 8
      : targetRect.bottom + 8;

    const calculatedLeft = targetRect.left + (targetRect.width / 2) - (width / 2);

    // Line 25: Synchronously update state BEFORE paint; user never sees the misplaced tooltip!
    setPosition({ top: calculatedTop, left: calculatedLeft });
  }, [targetRect]);

  // Line 29: useEffect handles analytics tracking asynchronously AFTER paint
  useEffect(() => {
    console.log("Tooltip displayed to user at:", new Date().toISOString());
    // Line 32: Cleanup function
    return () => {
      console.log("Tooltip unmounted");
    };
  }, []);

  return (
    <div
      ref={tooltipRef}
      style={{
        position: "fixed",
        top: `${position.top}px`,
        left: `${position.left}px`,
        backgroundColor: "#333",
        color: "#fff",
        padding: "8px 12px",
        borderRadius: "4px"
      }}
    >
      {content}
    </div>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "`useEffect` and `useLayoutEffect` have identical signatures but fundamentally different execution timings. `useEffect` is scheduled after the browser layout and paint phases, ensuring that side effects like API requests, event listeners, and timers never block user interactions or visual frame rendering. In contrast, `useLayoutEffect` executes synchronously immediately after DOM mutations but before the browser paints the pixels. It is reserved for reading layout geometry—such as scroll position or bounding rect dimensions—and mutating the DOM to eliminate visual jumping or flickering before the user sees the screen."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a responsive enterprise dashboard, users noticed a jarring visual pop/flicker where dynamic dropdown menus initially rendered in the top-left corner (0, 0) and jumped to their anchored button after 1 frame.
- **Task**: Eliminate the visual layout shift (CLS score penalty) on dropdown menus across all browsers.
- **Action**: We inspected the dropdown hook and identified that popup coordinates were being calculated inside `useEffect`. Because `useEffect` runs post-paint, the browser painted the initial `top: 0, left: 0` before the hook updated state. We swapped the positioning calculation to `useLayoutEffect`.
- **Result**: Completely eliminated visual pop-in (CLS dropped from 0.18 to 0.00), resulting in a flawless 60 FPS transition and raising user satisfaction scores.
""",

    os.path.join(BASE_DIR, "03-react", "06_memoization_usememo_usecallback_react_memo.md"): """# React Memoization: `React.memo`, `useMemo`, and `useCallback`

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Har baar jab parent component re-render hota hai, JavaScript uske andar ke har function aur object ko ek **Naye Memory Address** par recreate karta hai (`{} !== {}`).
`React.memo` ek **Security Guard** ki tarah hai jo component ke gate par khada rehta hai: Agar parent re-render hua lekin props change nahi huye, toh guard bolta hai: "Andar sab wahi hai, dobara paint mat karo".
`useCallback` ek **Function Reference Locker** hai jo function ka purana memory address reuse karta hai taaki guard ko bewakoof na banaya jaye.
`useMemo` ek **Heavy Calculation Calculator** hai: Agar aapne $100 + $200 calculate kar liya hai, toh jab tak input numbers change na hon, wo purana answer hi return karega.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`React.memo(Component, arePropsEqual?)`**:
   - Higher Order Component (HOC) that memoizes a component's rendered output.
   - Performs a **shallow comparison** of props (`Object.is`).
2. **`useCallback(fn, deps)`**:
   - Caches the **function instance** between renders.
   - `useCallback(fn, deps)` is syntactic sugar for `useMemo(() => fn, deps)`.
3. **`useMemo(calculateValue, deps)`**:
   - Caches the **computed result** of a function between renders.
4. **The Cost of Memoization**:
   - Memoization is NOT free! It allocates memory for dependency arrays and executes comparison checks on every single render.
   - Do NOT memoize trivial calculations (e.g. `2 + 2` or string concatenation).
5. **Referential Equality Problem**:
   - Passing an inline object `style={{ color: 'red' }}` or inline callback `onClick={() => {}}` to a `React.memo` component completely defeats memoization because new references are generated on every render.

---

## 📊 3. Visual Architecture Diagram

```
                 PARENT RE-RENDER EVALUATION
                 
  Parent Component State Updates ──► Parent Re-renders
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [ Plain Child Component ]                     [ React.memo(Child) ]
                  │                                               │
           Always Re-renders!                              Shallow Compare Props
                                                                  │
                                            ┌─────────────────────┴─────────────────────┐
                                            ▼                                           ▼
                                    Props are identical                       Props reference changed
                                            │                                           │
                                    SKIP Re-render! (0 cost)                    Trigger Child Re-render
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```jsx
import React, { useState, useMemo, useCallback } from "react";

// Line 4: Memoized pure presentational component with custom comparator
const ExpensiveListItem = React.memo(function ExpensiveListItem({ item, onDelete }) {
  console.log(`Rendering Item ID: ${item.id}`);
  return (
    <li>
      <span>{item.name} - ${item.price}</span>
      {/* Line 10: Passes onDelete callback; must be referentially stable! */}
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  );
});

export function ProductCatalog() {
  const [products, setProducts] = useState([
    { id: 1, name: "MacBook Pro", price: 2499 },
    { id: 2, name: "Mechanical Keyboard", price: 150 },
    { id: 3, name: "4K Monitor", price: 450 }
  ]);
  const [darkTheme, setDarkTheme] = useState(false);

  // Line 24: useMemo caches expensive aggregate calculation
  const totalPrice = useMemo(() => {
    console.log("Recalculating total price...");
    return products.reduce((acc, curr) => acc + curr.price, 0);
  }, [products]); // Recalculates ONLY when products array changes

  // Line 30: useCallback preserves function reference across theme toggles
  const handleDelete = useCallback((idToDelete) => {
    setProducts((prev) => prev.filter((item) => item.id !== idToDelete));
  }, []); // Empty deps because state updater function form `prev => ...` is used!

  return (
    <div style={{ backgroundColor: darkTheme ? "#222" : "#fff" }}>
      <button onClick={() => setDarkTheme(!darkTheme)}>Toggle Theme</button>
      <h3>Total Price: ${totalPrice}</h3>
      <ul>
        {products.map((item) => (
          // Line 42: Passing stable item object and stable handleDelete callback
          <ExpensiveListItem key={item.id} item={item} onDelete={handleDelete} />
        ))}
      </ul>
    </div>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "Memoization in React aims to preserve referential equality and avoid unnecessary re-render cycles of subtrees. `React.memo` wraps a component to shallowly compare incoming props against previous props. However, `React.memo` is rendered useless if the parent passes un-memoized object literals or inline arrow functions, because new memory references invalidate shallow equality on every render. We pair `React.memo` with `useCallback` to stabilize function references and `useMemo` to stabilize complex transformed data or expensive calculations. We apply memoization selectively where profiling in React DevTools demonstrates actual render bottlenecks."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an interactive analytics dashboard displaying a table of 2,000 rows with real-time WebSocket ticker updates, typing into an unrelated search input caused massive 120ms frame drops and input lag.
- **Task**: Eliminate input typing lag and keep typing response time under 16ms (60 FPS).
- **Action**: Profiling with the React DevTools Profiler revealed that every keystroke in the search bar triggered re-renders of all 2,000 table rows because the row action callback was declared inline. We wrapped each row in `React.memo`, stabilized the row action callback using `useCallback`, and memoized the filtered dataset using `useMemo`.
- **Result**: Typing re-render time plummeted from 120ms to 4ms per keystroke, row re-renders dropped from 2,000 to 0 on keystrokes, and CPU utilization decreased by 78%.
""",

    os.path.join(BASE_DIR, "03-react", "07_context_api_and_state_management.md"): """# Context API vs State Management (Redux Toolkit, Zustand)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Prop Drilling** ek bucket brigade ki tarah hai: Aag bujhane ke liye 10 log khade hain, paani 1st se 2nd, 2nd se 3rd hota hua 10th bande tak jata hai. Beech ke 8 logo ko paani se koi matlab nahi hai.
**Context API** ek **Society Notice Board** hai: Notice board par kuch bhi change hota hai, toh society ke sabhi 500 flat ke log notice board dekhne daudte hain (All consumers re-render even if they only needed 1 sentence).
**Zustand / Redux Toolkit** ek **Personalized SMS Alert Service** hai: Sirf us flat ke resident ka phone bajega jisse us transaction se matlab hai (**Atomic Selectors & Fine-Grained Subscriptions**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Context API is for Dependency Injection, NOT High-Frequency State**:
   - When a Context Provider's `value` reference changes, **every component that calls `useContext(MyContext)` re-renders unconditionally**, bypassing `React.memo`.
2. **Context Splitting**:
   - Best practice: Separate state and dispatchers into separate contexts (`AuthContext` and `AuthDispatchContext`) to prevent dispatch-only consumers from re-rendering on state changes.
3. **Zustand (Micro-State Manager)**:
   - Uses external store pattern based on closures outside the React tree.
   - Components subscribe via selectors (`const user = useStore(state => state.user)`).
   - Component only re-renders when the selected slice changes (`Object.is` check).
4. **Redux Toolkit (RTK)**:
   - Built on Immer for immutable updates via mutating syntax (`state.push()`).
   - Standardized architectural pattern for enterprise predictability with Redux DevTools time-travel debugging.

---

## 📊 3. Visual Architecture Diagram

```
       REACT CONTEXT (Coarse-Grained)           ZUSTAND / RTK (Fine-Grained Selectors)
       
        [ Context Provider ]                                 [ External Store ]
                 │ (Value changes)                                   │
       ┌─────────┴─────────┐                                ┌────────┴────────┐
       ▼                   ▼                                ▼                 ▼
  [ Consumer A ]     [ Consumer B ]                    [ Selector: User ] [ Selector: Theme ]
  (Both re-render    (Both re-render                   (Re-renders only   (SKIPS re-render!
   unconditionally!)  unconditionally!)                 when user changes) 0 cost)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
// ==========================================
// 1. Context Splitting Pattern (Production Standard)
// ==========================================
import React, { createContext, useContext, useReducer, useMemo } from "react";

// Line 7: Separate state context from dispatch context
const CounterStateContext = createContext(null);
const CounterDispatchContext = createContext(null);

function counterReducer(state, action) {
  switch (action.type) {
    case "INCREMENT": return { count: state.count + 1 };
    default: throw new Error(`Unknown action: ${action.type}`);
  }
}

export function CounterProvider({ children }) {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });

  return (
    // Line 22: Dispatch reference is stable and never changes
    <CounterDispatchContext.Provider value={dispatch}>
      {/* Line 24: State context changes when count updates */}
      <CounterStateContext.Provider value={state}>
        {children}
      </CounterStateContext.Provider>
    </CounterDispatchContext.Provider>
  );
}

// Custom hooks ensuring safe usage
export const useCounterState = () => {
  const context = useContext(CounterStateContext);
  if (!context) throw new Error("useCounterState must be used within CounterProvider");
  return context;
};

export const useCounterDispatch = () => {
  const context = useContext(CounterDispatchContext);
  if (!context) throw new Error("useCounterDispatch must be used within CounterProvider");
  return context;
};


// ==========================================
// 2. Modern Zustand Store with Selectors
// ==========================================
import { create } from "zustand";

// Line 49: Create Zustand external store
export const useAppStore = create((set) => ({
  user: { name: "Jay", role: "admin" },
  theme: "dark",
  notifications: [],
  setTheme: (theme) => set({ theme }),
  addNotification: (msg) =>
    set((state) => ({ notifications: [...state.notifications, msg] }))
}));

// Inside Component:
// Line 60: Subscribes ONLY to theme slice; ignores notifications and user updates!
function ThemeSwitcher() {
  const theme = useAppStore((state) => state.theme);
  const setTheme = useAppStore((state) => state.setTheme);
  return <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>Theme: {theme}</button>;
}
```

---

## 🎯 5. The "Interview Pitch"
> "React Context is a dependency injection mechanism designed for low-frequency global data such as themes, localization, or authenticated user profiles. It is fundamentally unsuitable as a high-frequency state management engine because any change to the provider's value triggers an unconditional re-render of every consumer down the tree, bypassing `React.memo`. For high-frequency, complex, or relational state, we use external store solutions like Zustand or Redux Toolkit. These libraries maintain state outside the React fiber tree and use selector subscriptions to trigger re-renders strictly on the specific components consuming the mutated state slice."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A collaborative whiteboarding canvas app stored cursor positions and drawing coordinates in a root React Context. As multiple users moved their cursors, the entire application suffered severe lag, frame drops down to 10 FPS, and CPU throttling.
- **Task**: Restore 60 FPS real-time cursor tracking for up to 50 concurrent users.
- **Action**: We profiled the app and observed that 300+ canvas elements were re-rendering on every cursor coordinate dispatch because they all consumed the single monolithic context. We migrated cursor positions to a Zustand store with atomic selector subscriptions (`useStore(s => s.cursors[userId])`). We also split low-frequency room metadata into a separate static context.
- **Result**: Canvas re-renders dropped by 96%, frame rates stabilized at 60 FPS, and collaborative lag was completely eliminated.
""",

    os.path.join(BASE_DIR, "03-react", "08_custom_hooks_patterns.md"): """# Custom Hook Design Patterns and Reusability Architecture

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
""",

    os.path.join(BASE_DIR, "03-react", "09_suspense_and_streaming_ssr.md"): """# React Suspense, Selective Hydration, and Streaming SSR

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**Traditional SSR (Old School)**: Ek restaurant jahan jab tak starter, main course, aur dessert teeno ek sath ready nahi hote, tab tak waiter table par ek glass paani bhi nahi rakhta! Customer bhooka baitha rehta hai (**All-or-Nothing Waterfall Bottleneck**).
**Streaming SSR with Suspense**: Jaise hi roti bani, waiter table par roti rakh deta hai; daal ban rahi hai toh uski jagah ek card rakh deta hai: "Daal 2 minute mein aa rahi hai" (`<Suspense fallback={<Skeleton />}>`). Aur sabse mazedaar baat: Agar customer pehle roti khana chahta hai, toh waiter pehle usi par ghee lagata hai (**Selective Hydration based on User Interaction**)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **How Suspense Works Under the Hood**:
   - A component suspended during render **throws a Promise**.
   - React catches the thrown Promise at the nearest `<Suspense>` boundary ancestor, pauses rendering that subtree, and renders the `fallback` UI.
   - When the Promise resolves, React restarts rendering the suspended component.
2. **Streaming Server-Side Rendering (HTTP 1.1 Chunked Transfer)**:
   - Node.js sends the initial shell HTML immediately via `renderToPipeableStream`.
   - As slower asynchronous data chunks resolve on the server, React streams replacement `<template>` script tags down the open HTTP pipe to swap skeletons with content in real time.
3. **Selective Hydration**:
   - Components wrapped in separate `<Suspense>` boundaries hydrate independently.
   - If a user clicks on an un-hydrated interactive widget, React **prioritizes hydrating that specific widget immediately** ahead of other background tasks.

---

## 📊 3. Visual Architecture Diagram

```
                 STREAMING SSR & SELECTIVE HYDRATION
                 
  Client Request ──► Server begins renderToPipeableStream()
                           │
                           ▼
  Send Initial HTML Shell: [ Header ] + [ Post Skeleton ] + [ Comments Skeleton ]
                           │ (Immediate First Contentful Paint!)
                           ▼
  Post Data Resolves ──► Stream chunk: <template> replacing Post Skeleton
                           │
                           ▼
  User clicks on Comments ──► React reprioritizes: HYDRATE COMMENTS FIRST!
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```jsx
import React, { Suspense } from "react";

// Line 4: Simulated async resource fetching that throws a promise for Suspense
function createResource(promise) {
  let status = "pending";
  let result;
  let suspender = promise.then(
    (res) => {
      status = "success";
      result = res;
    },
    (err) => {
      status = "error";
      result = err;
    }
  );

  return {
    read() {
      // Line 20: Suspense mechanic: Throw promise while pending
      if (status === "pending") throw suspender;
      if (status === "error") throw result;
      return result;
    }
  };
}

// Line 28: Component that consumes suspended data
function PostFeed({ resource }) {
  const posts = resource.read();
  return (
    <div>
      {posts.map((post) => (
        <article key={post.id}><h3>{post.title}</h3></article>
      ))}
    </div>
  );
}

// Line 40: Application with Suspense boundaries for independent streaming
export function AppShell({ postResource, commentsResource }) {
  return (
    <main>
      <h1>Tech News Portal</h1>
      
      {/* Post section streams independently */}
      <Suspense fallback={<div className="skeleton">Loading News Articles...</div>}>
        <PostFeed resource={postResource} />
      </Suspense>

      {/* Comments stream later without blocking post reading */}
      <Suspense fallback={<div className="skeleton">Loading Discussion Threads...</div>}>
        <PostFeed resource={commentsResource} />
      </Suspense>
    </main>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "React 18's Streaming SSR and Suspense overhaul the traditional all-or-nothing SSR paradigm. Previously, SSR required fetching all server data, rendering the entire HTML document, and loading all JavaScript before hydrating the page. With `renderToPipeableStream` and Suspense boundaries, the server streams the initial UI shell instantly using HTTP chunked transfer. Slower data sections stream progressively as HTML replacement scripts. Furthermore, Selective Hydration allows React to hydrate distinct Suspense subtrees independently, reprioritizing hydration on-the-fly based on user interaction clicks."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: An e-commerce product detail page suffered an abysmal Time to First Byte (TTFB: 2.8s) and Time to Interactive (TTI: 5.4s) because server rendering waited for a slow personalized recommendation engine (2,200ms latency) before emitting any HTML.
- **Task**: Reduce TTFB to under 300ms and allow users to view product images and purchase buttons instantly.
- **Action**: We migrated the Node.js SSR pipeline to `renderToPipeableStream` and wrapped the recommendation carousel in a `<Suspense fallback={<ProductSkeleton />}>` boundary. The critical product details streamed immediately, while the recommendations streamed down the open HTTP stream 2 seconds later.
- **Result**: TTFB dropped from 2,800ms to 180ms (a 93% improvement), LCP dropped to 850ms, and conversion rates increased by 14.2%.
""",

    os.path.join(BASE_DIR, "03-react", "10_react19_actions_use_hook_compiler.md"): """# React 19 Architecture: Actions, `use()`, `useOptimistic`, and the React Compiler

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
React 19 React history ka sabse bada paradigm shift hai.
Pehle developers ko har form ke liye `isSubmitting`, `error`, `useCallback`, `useMemo` ka jhanjhat paalna padta tha.
React 19 ka **React Compiler (Forget)** ek **Invisible Auto-Tuner** ki tarah hai: Aapko code mein manually `useMemo` ya `useCallback` lagane ki zaroorat hi nahi hai; compiler AST level par dekh leta hai ki kahan calculation cache karni hai.
`useOptimistic` WhatsApp message ke **Single Tick** ki tarah hai: Jaise hi aapne send dabaya, message turant screen par chala jata hai bina server confirmation ka wait kiye!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Actions & `useActionState`**:
   - Native async transitions that handle pending states, optimistic updates, and server errors automatically.
   - Works seamlessly with HTML forms (`<form action={formAction}>`).
2. **The `use()` Hook**:
   - Can unwrap Promises and Context **conditionally** inside render blocks and loops, breaking the historical rule that hooks cannot be conditional.
3. **`useOptimistic`**:
   - Allows rendering an optimistic UI state while an async action is in flight, automatically rolling back if the action rejects.
4. **The React Compiler (Project Forget)**:
   - Automated memoization at build time. Analyzes JavaScript semantics and auto-memoizes JSX subtrees and object references, rendering `useMemo`, `useCallback`, and `React.memo` obsolete in greenfield React 19 apps.
5. **Direct Ref Passing**:
   - `ref` is now a standard prop; `forwardRef` is deprecated and no longer needed in React 19.

---

## 📊 3. Visual Architecture Diagram

```
                 REACT 19 ACTION LIFECYCLE
                 
  User Submits Form ──► Form Action triggers async Transition
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
  [ useOptimistic ]                            [ useActionState ]
  Instantly updates UI with                    Sets isPending = true
  provisional data (0ms latency!)              Executes async server mutation
           │                                           │
           │ (Server confirms success)                 ▼
           └──────────────────────────────────► Syncs confirmed DB record
                                                Sets isPending = false
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```jsx
import { useActionState, useOptimistic, useRef } from "react";

// Line 4: Server action simulation
async function updateUsernameAction(previousState, formData) {
  const newName = formData.get("username");
  // Simulate network latency
  await new Promise((resolve) => setTimeout(resolve, 1000));

  if (newName === "admin") {
    return { error: "Username 'admin' is reserved!", username: previousState.username };
  }
  return { error: null, username: newName };
}

export function UserProfileCard({ currentUsername }) {
  // Line 17: useActionState manages pending status, form action dispatch, and state
  const [state, formAction, isPending] = useActionState(updateUsernameAction, {
    username: currentUsername,
    error: null
  });

  // Line 23: useOptimistic provides instant UI update while async transition is in flight
  const [optimisticUsername, setOptimisticUsername] = useOptimistic(
    state.username,
    (current, update) => update
  );

  return (
    <div>
      <h2>Profile: {optimisticUsername} {isPending && "(Saving...)"}</h2>
      
      {state.error && <p style={{ color: "red" }}>{state.error}</p>}

      {/* Line 35: Native form action integration in React 19 */}
      <form
        action={async (formData) => {
          const tentativeName = formData.get("username");
          // Update optimistic UI immediately
          setOptimisticUsername(tentativeName);
          // Dispatch action state transition
          await formAction(formData);
        }}
      >
        <input name="username" defaultValue={state.username} />
        <button type="submit" disabled={isPending}>
          {isPending ? "Updating..." : "Save"}
        </button>
      </form>
    </div>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "React 19 represents a monumental evolution in developer experience and performance. Core innovations include Actions and `useActionState`, which natively manage pending states, error handling, and form lifecycle transitions without manual boolean flags. The `use()` API allows conditional Promise and Context consumption directly inside components. With `useOptimistic`, optimistic UI state rollbacks are handled declaratively. Finally, the React Compiler eliminates manual memoization ceremonies (`useMemo`, `useCallback`, `React.memo`) by compiling fine-grained memoization directly into the emitted JavaScript at build time."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a social network feed, users felt the 'Like' and 'Bookmark' buttons were sluggish because updates waited 450ms for the API roundtrip before toggling the heart icon. In contrast, manual optimistic state logic was buggy and frequently desynchronized on network errors.
- **Task**: Deliver an instantaneous 0ms perceived response time on engagement actions with 100% reliable rollback on server failure.
- **Action**: We refactored the like button to React 19 Actions using `useOptimistic` and `useActionState`. When clicked, `useOptimistic` toggles the heart icon instantly while the server mutation runs in the background. If the request fails with a 500 error, React automatically rolls back the optimistic state without writing manual revert reducers.
- **Result**: Perceived interaction latency dropped from 450ms to 0ms, user engagement increased by 19%, and 200+ lines of custom rollback reducer boilerplate were deleted.
""",

    os.path.join(BASE_DIR, "03-react", "interview-questions", "top_react_interview_questions.md"): """# Top Senior React Interview Questions (Architecture & Diagnostics)

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

## 3. Explain how the `useId()` hook works in SSR hydration.
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
""",

    os.path.join(BASE_DIR, "03-react", "interview-questions", "machine_coding_autocomplete_search.md"): """# Machine Coding: High-Performance Autocomplete Search with Debounce & Cache

---

## 🐣 1. Layman's Analogy
Autocomplete search Google search bar ki tarah hai. Agar user "A-P-P-L-E" type kar raha hai, toh har letter par backend ko hit karna bewakoofi hai. Aap thoda intezaar karte ho jab tak user ruka na ho (`Debounce`). Aur agar user ne pehle "Apple" search kiya tha, toh dobara server par jaane ke bajaye memory drawer (`LRU Cache`) se turant dikha dete ho!

---

## 💻 2. Line-by-Line Commented Code Solution

```jsx
import React, { useState, useEffect, useRef, useCallback } from "react";

// Line 4: Simple in-memory cache to avoid duplicate network fetches
const searchCache = new Map();

export function AutocompleteSearch({ fetchSuggestionsUrl }) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  // Line 14: AbortController reference to cancel inflight requests
  const abortControllerRef = useRef(null);

  // Line 17: Fetch suggestions with cache and abort mechanism
  const fetchResults = useCallback(async (searchTerm) => {
    if (!searchTerm.trim()) {
      setSuggestions([]);
      return;
    }

    // Check cache hit
    if (searchCache.has(searchTerm)) {
      setSuggestions(searchCache.get(searchTerm));
      return;
    }

    // Cancel previous ongoing fetch
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    setIsLoading(true);
    try {
      const response = await fetch(
        `${fetchSuggestionsUrl}?q=${encodeURIComponent(searchTerm)}`,
        { signal: abortControllerRef.current.signal }
      );
      const data = await response.json();
      
      // Cache the result
      searchCache.set(searchTerm, data.results || []);
      setSuggestions(data.results || []);
    } catch (error) {
      if (error.name !== "AbortError") {
        console.error("Autocomplete search error:", error);
      }
    } finally {
      setIsLoading(false);
    }
  }, [fetchSuggestionsUrl]);

  // Line 57: Debounce typing effect
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchResults(query);
    }, 300);

    return () => clearTimeout(timer);
  }, [query, fetchResults]);

  // Keyboard Navigation (Arrow Up, Arrow Down, Enter)
  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setSelectedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : prev));
    } else if (e.key === "ArrowUp") {
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : prev));
    } else if (e.key === "Enter" && selectedIndex >= 0) {
      setQuery(suggestions[selectedIndex]);
      setIsOpen(false);
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  return (
    <div style={{ position: "relative", width: "320px" }}>
      <input
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setIsOpen(true);
        }}
        onKeyDown={handleKeyDown}
        placeholder="Search products..."
        style={{ width: "100%", padding: "8px", boxSizing: "border-box" }}
      />
      {isLoading && <span style={{ position: "absolute", right: 8, top: 8 }}>⏳</span>}

      {isOpen && suggestions.length > 0 && (
        <ul
          style={{
            position: "absolute",
            width: "100%",
            margin: 0,
            padding: 0,
            listStyle: "none",
            border: "1px solid #ccc",
            backgroundColor: "#fff",
            zIndex: 10
          }}
        >
          {suggestions.map((item, idx) => (
            <li
              key={item}
              onClick={() => {
                setQuery(item);
                setIsOpen(false);
              }}
              style={{
                padding: "8px",
                cursor: "pointer",
                backgroundColor: idx === selectedIndex ? "#e0f2fe" : "#fff"
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```
""",

    os.path.join(BASE_DIR, "03-react", "interview-questions", "machine_coding_virtualized_list.md"): """# Machine Coding: Custom Virtualized List (DOM Windowing from Scratch)

---

## 🐣 1. Layman's Analogy
Agar ek list mein 100,000 items hain, toh browser mein 100,000 `<div>` elements create karna browser ko freeze kar dega.
Virtualization ek **Cinema Screen** ki tarah hai: Screen par sirf wahi 10 actors dikhte hain jo camera ke samne hain. Jaise hi camera scroll karta hai, bahar gaye actors ko hata diya jata hai aur naye aane wale actors ko screen par draw kiya jata hai. Browser mein hamesha sirf 15-20 DOM nodes rehte hain!

---

## 💻 2. Line-by-Line Commented Code Solution

```jsx
import React, { useState, useRef } from "react";

/**
 * High-performance Virtualized List
 * Renders ONLY the visible items in the viewport plus a small buffer
 */
export function VirtualizedList({
  items,
  itemHeight = 40,
  windowHeight = 400
}) {
  const [scrollTop, setScrollTop] = useState(0);

  // Line 14: Total calculated height of full list to keep scrollbar accurate
  const totalHeight = items.length * itemHeight;

  // Line 17: How many items fit into view window
  const visibleCount = Math.ceil(windowHeight / itemHeight);

  // Line 20: Overscan buffer to ensure smooth scrolling without blank flashes
  const buffer = 3;

  // Line 23: Calculate start and end indices
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - buffer);
  const endIndex = Math.min(items.length - 1, Math.floor((scrollTop + windowHeight) / itemHeight) + buffer);

  // Line 27: Slice visible data window
  const visibleItems = items.slice(startIndex, endIndex + 1);

  // Line 30: Handle scroll event to update scroll offset
  const onScroll = (e) => {
    setScrollTop(e.currentTarget.scrollTop);
  };

  return (
    <div
      onScroll={onScroll}
      style={{
        height: `${windowHeight}px`,
        overflowY: "auto",
        position: "relative",
        border: "1px solid #ccc"
      }}
    >
      {/* Invisible container giving the browser correct scrollbar thumb height */}
      <div style={{ height: `${totalHeight}px`, position: "relative" }}>
        {visibleItems.map((item, index) => {
          const actualIndex = startIndex + index;
          return (
            <div
              key={actualIndex}
              style={{
                position: "absolute",
                top: `${actualIndex * itemHeight}px`,
                left: 0,
                right: 0,
                height: `${itemHeight}px`,
                padding: "0 12px",
                display: "flex",
                alignItems: "center",
                borderBottom: "1px solid #eee",
                boxSizing: "border-box"
              }}
            >
              Row {actualIndex}: {item}
            </div>
          );
        })}
      </div>
    </div>
  );
}
```
""",

    os.path.join(BASE_DIR, "04-frontend-frameworks", "nextjs", "02_server_actions_and_mutations.md"): """# Next.js Server Actions: Type-Safe RPC Mutations & Form Handling

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purane zamane mein frontend se backend database update karne ke liye aapko pehle ek REST API endpoint banana padta tha (`POST /api/update-user`), controller likhna padta tha, client side par `fetch()` likhna padta tha aur URL sync rakhna padta tha.
Server Action ek **Direct Teleportation Tube** ki tarah hai: Aap frontend component ke andar seedhe likhte ho `"use server"`, aur wo function bina kisi manual API endpoint banaye seedhe server ke Node.js environment mein securely execute hota hai!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`"use server"` Directive**: Marks an async function as a callable Server Action (RPC endpoint generated automatically by Next.js bundler).
2. **Security & Data Sanitization**:
   - Server Actions are public POST endpoints under the hood. Always authenticate the session and validate inputs using `zod` inside the action body.
3. **Cache Revalidation**:
   - `revalidatePath('/dashboard')`: Purges and refreshes the cached HTML/data for a route.
   - `revalidateTag('products')`: On-demand tag-based cache invalidation across all routes sharing the tag.
4. **Form Handling with `useActionState`**:
   - Manages pending status, server-side validation error messages, and form state without manual `fetch`.
5. **Optimistic Updates**: Works in tandem with `useOptimistic` for instant perceived mutations.

---

## 📊 3. Visual Architecture Diagram

```
                 NEXT.JS SERVER ACTION DISPATCH
                 
   [ Client Component Form ] ──► Submits <form action={createPost}>
                                         │
                                         ▼
   Next.js Client RPC Engine ──► POST request with encrypted Action ID
                                         │
                                         ▼
   [ Server Environment ]
   1. Verify JWT Session
   2. Validate with Zod
   3. Execute Database Query (Prisma/Drizzle)
   4. Call revalidatePath("/posts")
                                         │
                                         ▼
   Stream Back: New UI Tree chunk + Cache Invalidation updates!
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// app/actions/createPost.ts
"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { z } from "zod";

// Line 7: Define strict schema validation
const PostSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters"),
  content: z.string().min(10, "Content must be at least 10 characters")
});

export async function createPostAction(prevState: any, formData: FormData) {
  // Line 14: Extract raw form values
  const rawData = {
    title: formData.get("title"),
    content: formData.get("content")
  };

  // Line 20: Validate against Zod schema
  const validation = PostSchema.safeParse(rawData);
  if (!validation.success) {
    return {
      errors: validation.error.flatten().fieldErrors,
      success: false
    };
  }

  try {
    // Line 30: Perform database mutation (Prisma/SQL)
    console.log("Saving post to DB:", validation.data);
    
    // Line 33: Invalidate route cache so users immediately see the new post
    revalidatePath("/posts");
    revalidateTag("posts-feed");

    return { success: true, errors: {} };
  } catch (error) {
    return { success: false, errors: { global: ["Database error occurred"] } };
  }
}
```

---

## 🎯 5. The "Interview Pitch"
> "Next.js Server Actions provide a type-safe RPC mutation model directly embedded into React Server Components. By annotating an async function with `'use server'`, Next.js automatically provisions an internal encrypted POST endpoint. Crucially, Server Actions eliminate API routing boilerplate and integrate directly with Next.js's caching layer via `revalidatePath` and `revalidateTag`. Because Server Actions are public endpoints, production security demands strict authorization checks and schema validation via Zod inside every action."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In a Next.js 14 B2B portal, an engineer created a Server Action to update organization billing tiers without verifying the caller's session permissions inside the action, relying solely on client-side button hiding.
- **Task**: Secure the vulnerability and establish a security-first Server Action architecture.
- **Action**: We implemented a higher-order authenticated action wrapper `createSafeAction` that enforces session retrieval via `getServerSession()`, verifies RBAC permissions, and parses payloads through Zod before passing control to the business logic.
- **Result**: Neutralized privilege escalation risks across all 45 Server Actions and made permission checks mandatory across the engineering organization.
""",

    os.path.join(BASE_DIR, "04-frontend-frameworks", "nextjs", "03_caching_and_revalidation_deep_dive.md"): """# Next.js Caching Architecture & Revalidation Deep Dive

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Next.js App Router ka Caching System ek **4-Tier Smart Fridge** ki tarah hai:
1. **Request Memoization (Table top)**: Ek hi khana 3 log mang rahe hain, toh kitchen mein ek hi baar banta hai.
2. **Data Cache (Freezer)**: Server par API response freeze ho jata hai taaki baar-baar bahar market (database) na jana pade.
3. **Full Route Cache (Ready-made Lunchbox)**: Pura HTML page pehle se pack hai, aate hi de do.
4. **Router Cache (Customer ka Bag)**: Client ke browser memory mein recent pages store rehte hain taaki Back button dabane par 0ms mein page load ho!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Four Next.js Caches**:
   - **Request Memoization**: Deduplicates identical `fetch(url)` calls within a single React render pass.
   - **Data Cache**: Persistent server-side cache that survives requests and deployments (`fetch(url, { next: { revalidate: 3600 } })`).
   - **Full Route Cache**: Static HTML and React Server Component (RSC) payload rendered at build time or revalidated.
   - **Router Cache**: In-memory client-side cache storing RSC payloads during user navigation session.
2. **Opting Out of Caching**:
   - Use `export const dynamic = 'force-dynamic'`.
   - Set `fetch(url, { cache: 'no-store' })`.
   - Accessing dynamic functions like `cookies()`, `headers()`, or search parameters automatically triggers dynamic rendering.
3. **Time-based Revalidation vs On-Demand Revalidation**:
   - Time-based: `next: { revalidate: 60 }` (Stale-While-Revalidate).
   - On-Demand: Triggered explicitly via `revalidateTag()` or `revalidatePath()`.

---

## 📊 3. Visual Architecture Diagram

```
                 NEXT.JS 4-TIER CACHING PIPELINE
                 
  Client Navigation
          │
          ▼
  [ 1. Router Cache (Client Memory) ] ──(Hit: 0ms Instant Load)
          │ (Miss)
          ▼
  [ 2. Full Route Cache (Server HTML/RSC) ] ──(Hit: Static Page)
          │ (Miss/Dynamic)
          ▼
  [ 3. Request Memoization (Single Render) ] ──(Deduplicates Fetch)
          │ (Unique Fetch)
          ▼
  [ 4. Data Cache (Persistent Server Cache) ] ──(Hit: Return Cached DB JSON)
          │ (Miss / Stale)
          ▼
  [ Origin Data Source / Database Query ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// app/products/page.tsx
import { revalidateTag } from "next/cache";

// Line 4: Time-based ISR: Page revalidates at most once every 60 seconds
export const revalidate = 60;

export default async function ProductsPage() {
  // Line 8: Fetch tagged with 'products' for on-demand invalidation
  const res = await fetch("https://api.example.com/products", {
    next: { tags: ["products"] }
  });
  
  const products = await res.json();

  return (
    <div>
      <h1>Product Catalog (ISR Cached)</h1>
      <ul>
        {products.map((p: any) => (
          <li key={p.id}>{p.name} - ${p.price}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 🎯 5. The "Interview Pitch"
> "Next.js App Router implements a multi-tier caching architecture spanning both server and client runtimes. It operates across four distinct layers: Request Memoization, which deduplicates identical fetch requests within a single render cycle; the Data Cache, which persists API responses across requests; the Full Route Cache, which stores pre-rendered HTML and RSC payloads; and the Client Router Cache, which accelerates client-side navigation. We control this behavior through segment configurations like `export const dynamic = 'force-dynamic'` and leverage on-demand revalidation via `revalidateTag` to purge stale caches instantly upon database mutations."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: An e-commerce flash sale portal crashed during high-traffic drops because the product detail page executed 14 distinct database queries per request, causing PostgreSQL connection pool exhaustion.
- **Task**: Survive 50,000 requests per minute without database degradation while keeping inventory counts fresh within 10 seconds.
- **Action**: We refactored product pages to utilize Incremental Static Regeneration (ISR) with `next: { revalidate: 10, tags: ['inventory'] }`. When a product went out of stock, a webhook triggered `revalidateTag('inventory')` for instantaneous cache invalidation.
- **Result**: Database queries plummeted by 99.4%, response times dropped from 850ms to 24ms at the edge, and the platform handled the Black Friday flash sale with zero downtime.
""",

    os.path.join(BASE_DIR, "04-frontend-frameworks", "nextjs", "04_middleware_and_authentication.md"): """# Next.js Middleware: Edge Routing, Auth Guards, and Response Rewrites

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Next.js Middleware ek **Airport Security Gate (Edge Border Guard)** ki tarah hai. Passenger (HTTP Request) plane mein baithne (Server Components/Page render) se pehle security gate par rukta hai. Guard uska passport (JWT Cookie) check karta hai. Agar passport invalid hai, toh guard use gate se hi bahar nikal deta hai (`NextResponse.redirect('/login')`). Agar destination change ho gaya hai, toh guard chupke se route badal deta hai (`NextResponse.rewrite()`).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Edge Runtime Execution**:
   - Middleware runs on the V8 Edge runtime (not full Node.js). It does NOT have access to native Node.js APIs like `fs` or native C++ modules.
2. **Matcher Configuration**:
   - Use the `matcher` config to strictly filter which paths trigger middleware, excluding static assets (`_next/static`, `favicon.ico`, images) to avoid catastrophic performance overhead.
3. **`NextResponse.redirect` vs `NextResponse.rewrite`**:
   - `redirect`: Changes browser URL and issues HTTP 307/308 redirect.
   - `rewrite`: Proxies request internally to a different route **without changing the URL displayed in the user's browser address bar** (essential for multi-tenant subdomains).
4. **Header and Cookie Mutation**:
   - Can append custom request headers (`x-user-id`) to pass contextual data directly to downstream Server Components.

---

## 📊 3. Visual Architecture Diagram

```
                 NEXT.JS EDGE MIDDLEWARE PIPELINE
                 
   Client HTTP Request
            │
            ▼
   [ Middleware at the Edge ] ◄── (Runs BEFORE route renders!)
            │
      Is Authenticated?
      ├──► NO  ──► NextResponse.redirect("/login")
      │
      └──► YES ──► Append Request Header (x-user-id)
                   NextResponse.next()
                        │
                        ▼
            [ Server Component Page ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Line 6: Read session cookie
  const sessionToken = request.cookies.get("session_token")?.value;
  const { pathname } = request.nextUrl;

  // Line 10: Define protected routes
  const isProtectedRoute = pathname.startsWith("/dashboard") || pathname.startsWith("/settings");

  // Line 13: Redirect unauthenticated requests to login
  if (isProtectedRoute && !sessionToken) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Line 20: Forward request and inject tenant headers
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-pathname", pathname);

  return NextResponse.next({
    request: {
      headers: requestHeaders
    }
  });
}

// Line 31: Strict Matcher to exclude static files and image assets
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"]
};
```

---

## 🎯 5. The "Interview Pitch"
> "Next.js Middleware operates at the Edge before a request is processed by the route cache or server renderers. Because it runs on the lightweight Edge runtime, it lacks full Node.js module support, necessitating pure JavaScript libraries like `jose` for JWT verification. In production, middleware is primarily utilized for session authentication guards, geo-location redirects, A/B testing rewrites, and multi-tenant subdomain routing. Configuring an accurate regex `matcher` is critical to prevent middleware execution on static assets and API routes."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A multi-tenant SaaS application experienced latency spikes of +200ms per request across all image and font assets after a developer deployed a global middleware without a path filter.
- **Task**: Eliminate the 200ms latency penalty on static assets and restore sub-20ms edge routing.
- **Action**: We profiled Edge requests and saw that every `.png`, `.css`, and `favicon.ico` fetch was executing session cookie validation. We introduced an optimized negative lookahead regex matcher `matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)']`.
- **Result**: Middleware executions dropped by 74%, static asset response time returned to 12ms CDN delivery, and Edge compute costs fell by 60%.
""",

    os.path.join(BASE_DIR, "04-frontend-frameworks", "nextjs", "interview-questions", "nextjs_top_interview_questions.md"): """# Top Next.js Senior Interview Questions (App Router & Production Architecture)

---

## 1. What is the fundamental difference between React Server Components (RSC) and Client Components?
- **Server Components**:
  - Run **only on the server**.
  - Zero impact on client JavaScript bundle size.
  - Can directly query databases, read filesystem, and access server secrets.
  - Cannot use client interactivity hooks (`useState`, `useEffect`, event listeners).
- **Client Components** (`"use client"`):
  - Pre-rendered to static HTML on the server and **hydrated** with JavaScript on the client.
  - Support interactivity, state, lifecycle hooks, and browser APIs.

---

## 2. Does `"use client"` mean a component runs ONLY on the client?
- **NO!** This is a universal interview misconception.
- A component marked with `"use client"` is still pre-rendered into static HTML on the server during the initial page load for fast First Contentful Paint.
- `"use client"` simply denotes the **cut-off boundary** between the server-only module graph and the client-hydrated module graph.

---

## 3. How do you pass data from a Server Component to a Client Component without waterfalls?
- Fetch data directly in the Server Component async function.
- Pass the resolved serializable data as props to the Client Component.
- Pass Server Components as `children` into Client Components to prevent client bundle contamination.

---

## 4. What is the difference between `revalidatePath` and `revalidateTag`?
- `revalidatePath(path)` invalidates all cached data associated with a specific route path string.
- `revalidateTag(tag)` invalidates all fetch requests across the entire application that share that specific cache tag, providing fine-grained, decoupled cache purging.

---

## 5. What are Parallel Routes and Intercepting Routes used for?
- **Parallel Routes** (`@modal`, `@analytics`): Render multiple pages simultaneously in the same layout independently.
- **Intercepting Routes** (`(..)photos/[id]`): Load a route within the current layout (e.g. displaying a photo in a modal overlay while updating the URL), while direct refresh loads the full standalone page.
"""
}

def main():
    print(f"Generating {len(FILES)} Track 3 React & Next.js deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 3 React & Next.js generation complete!")

if __name__ == "__main__":
    main()
