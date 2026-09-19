# React Master Interview Bank: Part 1 (Q1 - Q20)
## Foundations, JSX, Virtual DOM & Component Architecture

---

### Q1: What is JSX and how does the React compiler transform it under the hood?
**Answer:**
- JSX (JavaScript XML) is a syntax extension for JavaScript that allows writing HTML-like markup inside JavaScript files.
- Browsers cannot execute JSX natively; it must be compiled into standard JavaScript by Babel or SWC.
- **Classic Runtime (pre-React 17):**
  `<h1>Hello</h1>` transformed into `React.createElement("h1", null, "Hello")`.
- **Modern Automatic Runtime (React 17+):**
  Uses the `_jsx` runtime (`react/jsx-runtime`). The compiler automatically imports `jsx` and transforms elements directly into lightweight React element descriptor objects without needing `import React from 'react'`.

```javascript
// Input JSX:
const element = <button className="btn" onClick={handleClick}>Click</button>;

// Compiled output:
import { jsx as _jsx } from "react/jsx-runtime";
const element = _jsx("button", {
  className: "btn",
  onClick: handleClick,
  children: "Click"
});
```

---

### Q2: What is the Virtual DOM and what is its architectural purpose?
**Answer:**
- The **Virtual DOM (VDOM)** is a lightweight in-memory representation of the real browser DOM tree consisting of plain JavaScript objects (React Elements).
- **Architectural Purpose:**
  Direct DOM manipulation is slow because modifying the real DOM triggers expensive browser engine pipeline stages: CSS recalculation, Layout (reflow), and Repaint.
  The Virtual DOM allows React to:
  1. Compute state updates in pure JavaScript memory.
  2. Perform diffing (reconciliation) between the previous and new virtual trees.
  3. Batch minimal required DOM mutations into a single atomic browser paint operation.

---

### Q3: How does React's Reconciliation Diffing Algorithm work? What are its heuristic assumptions?
**Answer:**
Comparing two arbitrary trees has an algorithmic complexity of $O(N^3)$ (where $N$ is the number of nodes).
React reduces this to an $O(N)$ linear algorithm based on **two heuristic assumptions**:
1. **Different Component Types produce Different Trees:** If an element changes from `<div>` to `<span>`, React dismantles the entire old subtree and builds a new one from scratch (unmounting old components and state).
2. **Stable Keys for Lists:** In child lists, elements with matching `key` props are treated as stable across renders. The algorithm can identify insertions, deletions, and moves without reconstructing matching siblings.

---

### Q4: Why is using array `index` as a `key` considered an anti-pattern? When is it acceptable?
**Answer:**
- **Why it's an Anti-Pattern:**
  If elements in a list can be reordered, inserted at the beginning, or filtered, using the array index binds component state to the **index position** rather than the **underlying item data**.
  - *Symptom:* Form inputs retain values from deleted items, uncontrolled component state drifts, and CSS animations glitch.
- **When is it Acceptable?**
  Only if ALL three conditions are satisfied:
  1. The list is completely static (read-only; never reordered, filtered, or prepended).
  2. The items have no IDs in their data structure.
  3. The list items contain zero internal state (pure presentational items).

---

### Q5: What is the difference between Controlled and Uncontrolled Components?
**Answer:**
| Dimension | Controlled Component | Uncontrolled Component |
| :--- | :--- | :--- |
| **State Source of Truth** | Stored in **React State** (`useState`). | Stored directly in the **Browser DOM** element. |
| **Data Access** | Value updated via `onChange` handler (`value={state}`). | Value queried on-demand using a React ref (`ref.current.value`). |
| **Instant Validation** | Trivially easy (state updates on every keystroke). | Difficult; requires querying DOM nodes. |
| **Ideal Use Case** | Dynamic forms, instant formatting, disabled submit buttons based on valid input. | Simple submit-only forms, integration with non-React DOM libraries, file upload inputs (`<input type="file" />`). |

---

### Q6: Why can't browsers read file input values in a Controlled manner?
**Answer:**
- An `<input type="file" />` is **always an uncontrolled component** in React.
- **Security Constraint:** For security reasons, JavaScript cannot set the `value` attribute of a file input programmatically (to prevent malicious websites from uploading arbitrary files from a user's hard drive). Its value can only be set by a direct user interaction via the OS file picker, and is read in React via `ref.current.files`.

---

### Q7: What are React Synthetic Events and how do they work in React 17/18/19?
**Answer:**
- **SyntheticEvent** is React's cross-browser wrapper around native browser events (`e.nativeEvent`), normalizing inconsistent browser APIs across Chrome, Safari, Firefox, and Edge.
- **Event Delegation Architecture:**
  - **In React 16 and earlier:** React attached a single global event listener at the root `document` level.
  - **In React 17+:** React attaches event listeners to the **root DOM container node** where the tree is mounted (`rootElement` passed to `createRoot`).
  - **Why changed:** Enables micro-frontends and multiple React applications with different React versions to coexist on the same page without synthetic events colliding at the `document` level.

---

### Q8: What is the difference between Element, Component, and Instance in React?
**Answer:**
- **React Element:** A plain, immutable JavaScript object describing what you want to see on screen: `{ type: 'button', props: { className: 'btn' } }`. Produced by JSX.
- **React Component:** A reusable blueprint (a function or class) that accepts `props` as input and returns a React Element tree.
- **React Instance:** The internal stateful entity created by React to track the component. In modern React, instances are internal **Fiber Nodes** representing component state, hooks, and DOM references.

---

### Q9: What are Pure Components and how do they optimize rendering?
**Answer:**
- In class components, `React.PureComponent` implements `shouldComponentUpdate()` with a **shallow prop and state comparison**.
- In functional components, wrapping a component in **`React.memo(Component, arePropsEqual)`** achieves the identical optimization: if props have not changed (via shallow `===` comparison), React skips rendering that component and reuses the previous virtual DOM snapshot.

---

### Q10: What are High-Order Components (HOCs) and what are their trade-offs?
**Answer:**
- A **Higher-Order Component (HOC)** is a pure function that takes a component as an argument and returns an enhanced component: `const EnhancedComponent = withAuth(BaseComponent);`.
- **Use Cases:** Cross-cutting concerns in legacy codebases (Authentication checks, Analytics logging, Theme injection).
- **Trade-offs / Drawbacks:**
  1. Prop collisions (silent name collisions between wrapped and wrapping props).
  2. "Wrapper Hell" in React DevTools (deeply nested component trees).
  3. Static methods must be manually copied over.
  *Modern Alternative:* **Custom Hooks** have largely superseded HOCs.

---

### Q11: What is the Render Props pattern?
**Answer:**
- A technique for sharing code between React components using a prop whose value is a function that returns a React Element: `<DataProvider render={(data) => <Chart data={data} />} />`.
- Solved HOC prop collisions by explicitly passing data down as function parameters.
- *Modern Status:* Largely replaced by custom hooks (`const data = useData()`), but still useful for headless UI components (e.g. Downshift, TanStack Table).

---

### Q12: What is the difference between Props and State?
**Answer:**
- **Props (Properties):** Immutable data passed from a parent component down to a child component (unidirectional data flow). A child cannot mutate its own props.
- **State:** Mutable data managed internally within a component that holds information that may change over the component's lifetime. Changing state triggers a re-render of the component and its children.

---

### Q13: What are React Fragments (`<React.Fragment>` or `<>...</>`) and why are they needed?
**Answer:**
- React components must return a **single root node** because a function can only return a single value, and reconciliation requires an anchor point.
- Fragments allow grouping a list of children without adding extra wrapper nodes (like redundant `<div>`s) to the real DOM tree.
- **`<React.Fragment key={id}>`**: Required when rendering a list of fragments that require a `key` prop (the short syntax `<>...</>` does not accept attributes or keys).

---

### Q14: What are Portals (`ReactDOM.createPortal`) and when must you use them?
**Answer:**
- `ReactDOM.createPortal(child, containerDOMNode)` renders a React child into a DOM node that exists **outside the DOM hierarchy of the parent component**.
- **When to Use:** Modals, tooltips, dialogs, and popovers that need to break out of parent containers with `overflow: hidden`, `z-index` stacking context traps, or transform constraints.
- **Event Bubbling Behavior:** Even though the portal node lives elsewhere in the real DOM, synthetic events **bubble up through the React component tree**, not the real DOM tree!

```javascript
import { createPortal } from "react-dom";

function Modal({ isOpen, children }) {
  if (!isOpen) return null;
  return createPortal(
    <div className="modal-overlay">{children}</div>,
    document.getElementById("modal-root") // Rendered at document root
  );
}
```

---

### Q15: What are Error Boundaries and what types of errors do they NOT catch?
**Answer:**
- An **Error Boundary** is a class component that catches JavaScript errors anywhere in its child component tree, logs the errors, and displays a fallback UI instead of crashing the entire application.
- Implemented via `static getDerivedStateFromError(error)` (to render fallback UI) and `componentDidCatch(error, errorInfo)` (to log errors to Sentry/Datadog).
- **Errors NOT Caught by Error Boundaries:**
  1. Asynchronous code (`setTimeout`, `requestAnimationFrame`, `Promise` rejections).
  2. Event handlers (`onClick`, `onSubmit` - must use standard `try...catch` inside the handler).
  3. Server-side rendering (SSR) errors.
  4. Errors thrown inside the Error Boundary component itself.

---

### Q16: How does Prop Drilling differ from Context API?
**Answer:**
- **Prop Drilling:** Passing props down through multiple layers of intermediate components that do not actually need the data, merely to deliver it to a deeply nested child.
- **React Context:** Provides a way to pass data through the component tree without having to pass props down manually at every level (Teleporting state).
- **Caution:** Context is designed for low-frequency global updates (Theme, Auth user, Locale). Storing high-frequency state (e.g. mouse coordinates, form inputs) in Context triggers unnecessary re-renders of all consuming components.

---

### Q17: What is Strict Mode (`<React.StrictMode>`) and why does it run effects twice?
**Answer:**
- StrictMode is a development-only tool that highlights potential problems in an application:
  1. Identifies components with unsafe lifecycles.
  2. Warns about legacy string refs and deprecated findDOMNode usage.
  3. Detects unexpected side effects by **intentionally double-invoking functions**:
     - Component render bodies.
     - `useState` and `useReducer` initializer functions.
     - `useEffect` setup and cleanup cycles (Mount $\to$ Unmount $\to$ Remount).
- **Why double-invoked:** Verifies that your effect cleanups correctly reset state, preventing memory leaks and preparing code for Concurrent Mode and future component re-mounting.

---

### Q18: What is the difference between Declarative and Imperative programming in React?
**Answer:**
- **Imperative Programming (Vanilla JS / jQuery):** You explicitly describe *every step* of how to mutate the DOM:
  `const btn = document.querySelector('button'); btn.classList.add('active'); btn.textContent = 'Saved';`
- **Declarative Programming (React):** You describe *what the UI should look like* for a given state:
  `<button className={isSaved ? "active" : ""}>{isSaved ? "Saved" : "Save"}</button>`.
  React handles all underlying DOM mutations automatically.

---

### Q19: How do you pass data from a Child Component to a Parent Component?
**Answer:**
In React's unidirectional data flow, data flows down via props. To send data upwards:
1. The Parent defines a callback function: `const handleSelect = (data) => { ... };`.
2. The Parent passes this function to the Child as a prop: `<Child onSelect={handleSelect} />`.
3. The Child invokes the callback with arguments: `props.onSelect(childData)`.

---

### Q20: What are Default Props in modern React functional components?
**Answer:**
- In legacy React, `Component.defaultProps = { theme: 'dark' }` was used.
- In modern functional components, `defaultProps` is deprecated. Use **native ES6 default parameter values** directly in the function signature:

```javascript
// Modern standard:
function Card({ title = "Untitled", padding = 16, children }) {
  return <div style={{ padding }}><h3>{title}</h3>{children}</div>;
}
```
