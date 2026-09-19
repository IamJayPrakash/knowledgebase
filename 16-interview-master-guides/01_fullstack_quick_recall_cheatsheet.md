# Fullstack Senior Engineer Quick Recall Cheat Sheet (5-Minute Review)

---

## 🚀 1. JavaScript & Web Core

- **Event Loop Order**: Call Stack ➔ Microtasks (`Promise.then`, `queueMicrotask`, `process.nextTick`) ➔ Browser Render/Paint ➔ Macrotasks (`setTimeout`, `setInterval`, `setImmediate`, I/O).
- **Prototypal Inheritance**: `obj.__proto__ === Constructor.prototype`. `Object.prototype.__proto__ === null`.
- **`this` Binding Priority**: `new` binding ➔ Explicit (`bind`/`apply`/`call`) ➔ Implicit (Object method dot) ➔ Default (Global or `undefined` in strict). Arrow functions capture `this` lexically at creation time.
- **Core Web Vitals Targets**:
  - **LCP** (Largest Contentful Paint): $\le 2.5s$.
  - **INP** (Interaction to Next Paint): $\le 200ms$.
  - **CLS** (Cumulative Layout Shift): $\le 0.1$.

---

## ⚛️ 2. React & Next.js

- **Reconciliation Diffing**: Types differ ➔ Tear down subtree. Same types ➔ Update changed props. Keys provide stable identity across sibling renders.
- **`useEffect` vs `useLayoutEffect`**: `useEffect` runs async after browser paint. `useLayoutEffect` runs synchronously before paint (for layout measurements & anti-flicker).
- **Next.js App Router**: Server Components by default (0 client bundle). Server Actions (`"use server"`) provide RPC mutations with `revalidatePath()` and `revalidateTag()`.

---

## 🅰️ 3. Modern Angular 21

- **Signals**: `signal()`, `computed()`, `effect()`. Fine-grained synchronous reactivity without Zone.js.
- **Zoneless Architecture**: Angular 21 is zoneless by default. Change detection is triggered via signal notifications and `ChangeDetectorRef`.
- **`@defer` Block**: Template-level lazy loading (`@defer (on viewport) { <HeavyComp /> } @placeholder { <Skeleton /> }`).

---

## 🐍 4. Python FastAPI & Node.js

- **Node.js**: Libuv event loop. 4-thread pool for `fs`, `crypto`, `zlib`, `dns`. Never use synchronous I/O or block event loop.
- **FastAPI**: Pydantic V2 (Rust core). `async def` runs on asyncio event loop (use only async non-blocking calls); regular `def` runs in a background threadpool.
