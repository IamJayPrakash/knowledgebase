# React Memoization: `React.memo`, `useMemo`, and `useCallback`

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
>
> "Memoization in React aims to preserve referential equality and avoid unnecessary re-render cycles of subtrees. `React.memo` wraps a component to shallowly compare incoming props against previous props. However, `React.memo` is rendered useless if the parent passes un-memoized object literals or inline arrow functions, because new memory references invalidate shallow equality on every render. We pair `React.memo` with `useCallback` to stabilize function references and `useMemo` to stabilize complex transformed data or expensive calculations. We apply memoization selectively where profiling in React DevTools demonstrates actual render bottlenecks."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an interactive analytics dashboard displaying a table of 2,000 rows with real-time WebSocket ticker updates, typing into an unrelated search input caused massive 120ms frame drops and input lag.
- **Task**: Eliminate input typing lag and keep typing response time under 16ms (60 FPS).
- **Action**: Profiling with the React DevTools Profiler revealed that every keystroke in the search bar triggered re-renders of all 2,000 table rows because the row action callback was declared inline. We wrapped each row in `React.memo`, stabilized the row action callback using `useCallback`, and memoized the filtered dataset using `useMemo`.
- **Result**: Typing re-render time plummeted from 120ms to 4ms per keystroke, row re-renders dropped from 2,000 to 0 on keystrokes, and CPU utilization decreased by 78%.
