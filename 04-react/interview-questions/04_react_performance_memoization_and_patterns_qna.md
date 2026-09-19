# React Master Interview Bank: Part 4 (Q61 - Q80)
## Performance Optimization, Memoization & State Management

---

### Q61: What causes a React component to re-render? List all triggers.
**Answer:**
A React component re-renders if and only if:
1. **State Update:** Internal component state changes via `useState` setter or `useReducer` dispatch.
2. **Parent Component Re-renders:** When a parent re-renders, **all of its children re-render by default**, regardless of whether their props changed (unless wrapped in `React.memo`).
3. **Context Value Change:** A context value consumed by the component via `useContext` changes.
4. **Custom Hook State Update:** A custom hook called inside the component triggers a state update.
5. **Forced Update:** In class components via `this.forceUpdate()`.

*Note: Props changing does NOT independently cause a re-render; it is the parent re-rendering and passing new props that triggers child rendering.*

---

### Q62: How does `React.memo` work and how do you write a custom `arePropsEqual` comparison?
**Answer:**
- `React.memo(Component, arePropsEqual)` wraps a component. If its incoming props have not changed, React skips rendering the component and reuses the last rendered output.
- **Default Comparison:** Performs a shallow equality check (`prevProps[key] === nextProps[key]`).
- **Custom Comparison:**
  - *Caution:* Unlike `shouldComponentUpdate` (which returned `true` to re-render), `arePropsEqual` returns **`true` if props are equal (SKIP render)**, and **`false` if props are different (TRIGGER render)**.

```javascript
import React from "react";

function UserProfile({ user, onUpdate }) {
  return <div>{user.name} - {user.email}</div>;
}

function arePropsEqual(prevProps, nextProps) {
  // Only re-render if user ID, name, or email changed
  return (
    prevProps.user.id === nextProps.user.id &&
    prevProps.user.name === nextProps.user.name &&
    prevProps.user.email === nextProps.user.email
  );
}

export default React.memo(UserProfile, arePropsEqual);
```

---

### Q63: Why does `React.memo` frequently fail to prevent re-renders in practice?
**Answer:**
`React.memo` fails when parents pass **unstable references** as props:
1. **Inline Functions:** `<Child onClick={() => doSomething()} />` creates a brand-new function memory reference on every parent render. Shallow comparison `prevClick === nextClick` evaluates to `false`.
2. **Inline Objects or Arrays:** `<Child style={{ color: 'red' }} options={['a', 'b']} />` creates new object references on every render.
- **Solution:** Wrap callback functions in `useCallback`, wrap objects in `useMemo`, or hoist static objects outside the component body.

---

### Q64: What is the Context API Performance Bottleneck, and how do you optimize it?
**Answer:**
- **The Bottleneck:** When a Context Provider's `value` updates, **every single consumer component** that calls `useContext(MyContext)` will re-render, even if that component only cares about a single unchanged property of the context value.
- **3 Optimization Strategies:**
  1. **Split Contexts:** Separate state that changes often from state that changes rarely (e.g. `ThemeContext` vs `AuthContext` vs `CartContext`).
  2. **Separate State and Dispatch:** Put mutable state in `CartStateContext` and stable dispatch actions in `CartDispatchContext`. Components that only dispatch actions never re-render when cart items change!
  3. **Context Selectors / Zustand:** Migrate high-frequency state to libraries supporting fine-grained property selectors (`useStore(state => state.itemCount)`).

---

### Q65: Compare Redux Toolkit (RTK) vs Zustand vs Recoil/Jotai.
**Answer:**
| Dimension | Redux Toolkit (RTK) | Zustand | Jotai / Recoil |
| :--- | :--- | :--- | :--- |
| **Architecture** | **Flux (Single Store)**. Actions $\to$ Reducers $\to$ Store. | **Flux (Single Store)**. Hook-based with closures. | **Atomic**. Independent reactive atom state graph. |
| **Boilerplate** | Medium (Slices, Store setup, Typed hooks). | **Minimal (Zero boilerplate)**. Simple `create((set) => ({ ... }))`. | Low (Define atoms `atom(0)`). |
| **Selectors** | `useSelector(selectData)` with memoized reselect. | Native selector hooks: `useStore(s => s.foo)`. | Selectors derived via computed atoms. |
| **Bundle Size** | ~11 KB | **~1.1 KB** | ~3 KB |
| **Ideal For** | Large enterprise apps with complex middleware (RTK Query). | Modern apps of any size wanting clean, frictionless state. | Fine-grained independent widget state (canvas, SVG drawing apps). |

---

### Q66: How does Zustand avoid unnecessary re-renders without a Context Provider?
**Answer:**
- Zustand stores live **outside the React component tree** in a pure JavaScript closure (Module Singleton).
- Components subscribe to store changes using a **selector**: `const count = useStore(state => state.count);`.
- Zustand uses `useSyncExternalStoreWithSelector`. When the store mutates, Zustand runs the component's selector function. If the selected return value has not changed (`Object.is`), React skips re-rendering that component entirely.

---

### Q67: What is DOM Virtualization (Windowing) and when should you use it?
**Answer:**
- **DOM Virtualization:** Rendering only the elements currently visible inside the user's viewport (plus a small overscan buffer), rather than rendering thousands of DOM nodes.
- **When to Use:** Lists or tables with $> 100$ items (e.g. data tables, infinite social feeds, search results).
- **Impact:** Reduces DOM node count from 50,000 to ~20 nodes, cutting memory usage from 200MB to 5MB and keeping scroll performance locked at 60 FPS.
- **Popular Libraries:** `react-window`, `tanstack-virtual`.

---

### Q68: How do you implement Code Splitting using `React.lazy` and `<Suspense>`?
**Answer:**
- By default, Webpack/Vite bundles an entire application into a single monolithic JavaScript file.
- `React.lazy(() => import('./HeavyComponent'))` dynamically loads component chunks on demand over the network via dynamic `import()`.

```javascript
import React, { Suspense, lazy } from "react";

const AnalyticsDashboard = lazy(() => import("./AnalyticsDashboard"));

function App() {
  return (
    <div>
      <Navbar />
      <Suspense fallback={<div>Loading Analytics Module...</div>}>
        <AnalyticsDashboard />
      </Suspense>
    </div>
  );
}
```

---

### Q69: What is the React Profiler API and what do `actualDuration` vs `baseDuration` signify?
**Answer:**
- `<Profiler id="App" onRender={callback}>` measures the rendering performance of a React component tree programmatically.
- **Callback Parameters:**
  - **`actualDuration`**: Time spent rendering the committed update for this subtree. Indicates how well memoization worked (low value = high memoization efficiency).
  - **`baseDuration`**: Estimated time to render the entire subtree from scratch with zero memoization. Comparing `actualDuration` against `baseDuration` reveals the performance gain of your `useMemo`/`React.memo` optimizations.

---

### Q70: What is Structural Sharing in Immutable State and why is it essential for React?
**Answer:**
- **Structural Sharing:** When updating an immutable nested object or array, only the modified nodes and their direct ancestors are re-allocated with new memory references; all untouched sibling branches **share their existing memory references**.
- **Why Essential:** Enables $O(1)$ shallow reference equality checks (`prevObj === nextObj`). Without structural sharing, checking if an object changed would require an expensive deep recursive traversal $O(N)$.

---

### Q71: How does Immer simplify immutable state updates?
**Answer:**
- Immer uses JavaScript **`Proxy`** objects to track mutations on a temporary "draft" state.
- You write natural, mutating code (`draft.user.posts[0].likes++`), and Immer intercepts the modifications to produce a brand-new immutable copy using structural sharing under the hood.
- Built directly into Redux Toolkit (`createSlice`).

---

### Q72: What is the difference between Container and Presentational components?
**Answer:**
- **Container Components:** Focus on *how things work*. Responsible for fetching data, subscribing to global stores, handling lifecycle logic, and managing state. Rarely have HTML markup or styles.
- **Presentational Components:** Focus on *how things look*. Stateless pure functions that receive data exclusively through `props` and render UI markup and styles.
- *Modern note:* Custom hooks have largely absorbed container responsibilities.

---

### Q73: Why should you avoid defining components inside other components?
**Answer:**
```javascript
// ❌ CRITICAL ANTI-PATTERN:
function Parent() {
  const Child = () => <div>Hello</div>; // Declared inside render!
  return <Child />;
}
```
**Why it's fatal:**
Every time `Parent` re-renders, a **brand-new component function reference** for `Child` is allocated in memory. React treats different component references as different component types (Heuristic 1 of reconciliation).
- React unmounts and remounts `Child` on every render, resetting all internal state, dropping DOM focus, and destroying performance.

---

### Q74: What are Compound Components in React?
**Answer:**
- A design pattern where components work together to form a cohesive UI unit while sharing implicit state (e.g. `<Select>` and `<Select.Option>`, or `<Tabs>` and `<Tab.Panel>`).
- Built using React Context to provide shared active index and toggle handlers transparently to child elements without manual prop passing.

---

### Q75: How do you prevent layout thrashing inside React components?
**Answer:**
- **Layout Thrashing:** Repeatedly reading from the DOM (e.g. `offsetHeight`, `scrollTop`) and immediately writing to the DOM (e.g. `style.height = ...`), forcing the browser to recalculate layout multiple times within a single frame.
- **Prevention in React:**
  1. Batch all DOM reads together first inside `useLayoutEffect`.
  2. Perform all DOM writes together afterwards.
  3. Or use `requestAnimationFrame` to decouple writes until the next frame.

---

### Q76: What is the difference between Throttling and React 18 `useTransition`?
**Answer:**
- **Throttling:** Limits the number of times a function executes over time (e.g., at most once every 100ms). The rendering work is still synchronous and will block the main thread during execution.
- **`useTransition`:** Does **not** throttle or drop updates; instead, it renders the work **asynchronously in the background with time slicing**, immediately pausing or discarding work if a user interacts with the UI.

---

### Q77: How do you profile React apps in production without DevTools?
**Answer:**
Use the native `<Profiler>` component with a telemetry beacon:
```javascript
function onRenderCallback(id, phase, actualDuration) {
  if (actualDuration > 50) { // Long task > 50ms
    navigator.sendBeacon("/telemetry/perf", JSON.stringify({ id, phase, actualDuration }));
  }
}

<Profiler id="CheckoutFlow" onRender={onRenderCallback}>
  <Checkout />
</Profiler>
```

---

### Q78: Why should you avoid using anonymous arrow functions in JSX props?
**Answer:**
- While modern V8 engines allocate closures very quickly, anonymous arrow functions create a **new function reference** on every render.
- If passed to an unmemoized component, the impact is minimal.
- However, if passed to a component wrapped in `React.memo` or used in a `useEffect` dependency array, it completely invalidates memoization and causes unnecessary cascading re-renders.

---

### Q79: What is React DevTools "Highlight updates when components render"?
**Answer:**
- A diagnostic setting in React DevTools that draws colored rectangular outlines around components on screen whenever they re-render.
- Green indicates low-frequency renders, while yellow/red indicates rapid re-render frequency.
- Invaluable for identifying unintended cascading re-renders and unnecessary parent-to-child render waterfalls.

---

### Q80: How does `useCallback` prevent unnecessary re-renders in a child component?
**Answer:**
```javascript
// Parent component:
const handleDelete = useCallback((id) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []); // Stable reference!

// Child component:
const ItemRow = React.memo(({ item, onDelete }) => {
  return <div>{item.name} <button onClick={() => onDelete(item.id)}>Delete</button></div>;
});
```
Because `handleDelete` retains the identical memory address across parent re-renders, `ItemRow`'s shallow prop comparison passes (`prevOnDelete === nextOnDelete`), and `ItemRow` skips re-rendering when unrelated parent state updates.
