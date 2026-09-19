# React Master Interview Bank: Part 5 (Q81 - Q100)
## React 19, Server Components (RSC) & Fullstack Architecture

---

### Q81: What are React Server Components (RSC) and how do they fundamentally differ from Traditional SSR?
**Answer:**
| Dimension | Traditional SSR (Pages Router / React 17) | React Server Components (RSC - React 19) |
| :--- | :--- | :--- |
| **Execution** | Runs once on server to produce initial HTML string, then **must download entire JavaScript bundle to hydrate** on the client. | Executes **exclusively on the server**. Component code **never ships to client bundles** (0 KB JavaScript). |
| **State & Effects** | Can use `useState`, `useEffect`, and browser event handlers. | Cannot use hooks (`useState`, `useEffect`) or browser event handlers (`onClick`). |
| **Data Access** | Requires special lifecycle functions (`getServerSideProps`). | Direct `async/await` access to databases, internal microservices, and file systems. |
| **Re-rendering** | Re-renders on the client when state changes. | Can re-fetch and re-render on the server without wiping client-side state. |

---

### Q82: What is the RSC Wire Protocol (Payload format)?
**Answer:**
- When an RSC re-renders, the server does NOT send HTML or raw JSON.
- It streams a specialized line-delimited JSON-like serialization format called the **RSC Payload**:
  - Contains references to React component types.
  - Contains serialized props and data trees.
  - Contains placeholders (`$`) for Suspense boundaries and Client Component module references.
- **Client Processing:** The client reconciles this streaming payload directly into the active client-side Virtual DOM tree **without blowing away active client DOM focus, text selection, or input state**!

---

### Q83: When should a component have the `"use client"` directive?
**Answer:**
`"use client"` is **not** a command to execute code exclusively on the client; it marks the **boundary** between the Server Component module graph and the Client Component module graph.
You **must** add `"use client"` if the component:
1. Uses state or lifecycle hooks (`useState`, `useReducer`, `useEffect`, `useLayoutEffect`).
2. Uses custom hooks that depend on client state or browser APIs.
3. Uses browser-only APIs (`window`, `localStorage`, `navigator`, geolocation).
4. Uses interactive event listeners (`onClick`, `onChange`, `onSubmit`).

*Everything else should remain a Server Component by default.*

---

### Q84: How do Server Actions (`"use server"`) work in React 19?
**Answer:**
- **Server Action:** An asynchronous function declared with `"use server"` that executes securely on the server.
- **Under the hood:**
  When passed to a form action (`<form action={myServerAction}>`), React generates a POST endpoint behind the scenes.
  - When the user submits the form, React performs an RPC (Remote Procedure Call) fetch request sending `FormData`.
  - **Progressive Enhancement:** Server actions work even if JavaScript is disabled or still downloading in the browser!

```javascript
// app/actions.js
"use server";

export async function updateUsername(formData) {
  const newName = formData.get("username");
  await db.user.update({ where: { id: 1 }, data: { name: newName } });
}
```

---

### Q85: What is the `useActionState` hook in React 19?
**Answer:**
- Replaces the experimental `useFormState`.
- Manages the state of an asynchronous Server Action (such as form submission results, validation errors, and pending status):

```javascript
"use client";
import { useActionState } from "react";
import { updateUsername } from "./actions";

function ProfileForm() {
  const [state, formAction, isPending] = useActionState(updateUsername, { error: null });

  return (
    <form action={formAction}>
      <input name="username" defaultValue="Alice" />
      <button disabled={isPending}>{isPending ? "Saving..." : "Save"}</button>
      {state.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

---

### Q86: What is the `useOptimistic` hook in React 19?
**Answer:**
- Enables **Optimistic UI Updates**: displaying updated state on screen immediately before a background network request/Server Action confirms success.
- If the server action succeeds, the real data replaces the optimistic data.
- If the server action fails, React automatically rolls back the UI to the previous state.

```javascript
"use client";
import { useOptimistic } from "react";

function LikeButton({ initialLikes, onLikeAction }) {
  const [optimisticLikes, setOptimisticLikes] = useOptimistic(
    initialLikes,
    (current, update) => current + update
  );

  const handleLike = async () => {
    setOptimisticLikes(1); // Immediate instant UI feedback!
    await onLikeAction();  // Network request
  };

  return <button onClick={handleLike}>❤️ {optimisticLikes}</button>;
}
```

---

### Q87: What is the `use()` API in React 19, and how does it break the Rules of Hooks?
**Answer:**
- The `use(resource)` API allows reading the value of a resource (a **Promise** or a **Context**) inside a component.
- **Breaks Traditional Rules of Hooks:**
  Unlike all other hooks, **`use()` can be called conditionally inside `if` statements and loops**!
- **With Promises:** If the promise is pending, the component suspends at the nearest `<Suspense>` boundary until the promise resolves.

```javascript
import { use, Suspense } from "react";

function Comments({ commentsPromise }) {
  // Can be called conditionally!
  const comments = use(commentsPromise);
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}
```

---

### Q88: How does React 19 eliminate `forwardRef`?
**Answer:**
- In React 18 and earlier, passing a `ref` to a functional component required wrapping it with `forwardRef((props, ref) => ...)`.
- In **React 19**, `ref` is treated as a **standard prop** on functional components. `forwardRef` is deprecated and will eventually be removed!

```javascript
// React 19 Standard:
function MyInput({ placeholder, ref }) {
  return <input placeholder={placeholder} ref={ref} />;
}
```

---

### Q89: What is the React Compiler (formerly React Forget)?
**Answer:**
- An automatic optimizing compiler created by the React core team.
- Analyzes JavaScript semantics and component dependencies at build-time and automatically inserts fine-grained memoization (`useMemo`, `useCallback`, `React.memo`) directly into compiled code.
- **Impact:** Developers no longer need to manually manage dependency arrays or manually memoize functions and objects.

---

### Q90: How does React 19 natively support Document Metadata (`<title>`, `<meta>`)?
**Answer:**
- In legacy React, managing `<head>` tags required third-party libraries like `react-helmet`.
- In **React 19**, you can render `<title>`, `<link>`, and `<meta>` tags directly anywhere inside components. React automatically hoists them into the document `<head>` during rendering.

```javascript
function Article({ post }) {
  return (
    <article>
      <title>{post.title} | My Blog</title>
      <meta name="description" content={post.summary} />
      <h1>{post.title}</h1>
    </article>
  );
}
```

---

### Q91: What is the difference between Server Actions and API Routes?
**Answer:**
- **API Routes (`/api/users`):** Standard REST endpoints designed for third-party public consumption, mobile apps, and webhook listeners. Requires manual serialization and URL endpoint routing.
- **Server Actions:** Internal Remote Procedure Calls (RPC) tightly coupled with React components. They automatically handle serialization, mutation, form resets, and immediate server-side cache revalidation in a single network round-trip.

---

### Q92: What is the `useFormStatus` hook in React 19?
**Answer:**
- Gives child components access to the status of a parent `<form>` without prop drilling.
- Returns `{ pending, data, method, action }`.
- Must be rendered as a **child inside** a `<form>` element.

```javascript
"use client";
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "Submitting..." : "Submit"}</button>;
}
```

---

### Q93: Can you pass functions from a Server Component to a Client Component?
**Answer:**
- **Standard synchronous functions:** **NO**. Functions cannot be serialized across the network boundary in the RSC protocol.
- **Server Actions (`"use server"` functions):** **YES**. React serializes Server Actions as special signed cryptographic endpoint references that the client can safely invoke.

---

### Q94: What is the "Poisoning" / Module Boundary rule in Server Components?
**Answer:**
- If a server module contains sensitive logic (database passwords, private API keys) and is accidentally imported into a Client Component, bundlers might leak secrets to client browser bundles.
- **Solution:** Use the official **`server-only` package**:
  `import 'server-only';` at the top of server files. If any Client Component imports this file, the build fails immediately with a compile-time error.

---

### Q95: What is Streaming SSR with HTML and Suspense?
**Answer:**
- In traditional SSR, the server waits for ALL database queries to finish before sending a single byte of HTML (High TTFB).
- With **Streaming SSR**:
  1. The server immediately sends an HTML shell with loading spinners for suspended sections.
  2. As slow database queries resolve on the server, React streams additional HTML chunks and inline `<script>` tags to swap the spinners with real content in place.

---

### Q96: Why can't Server Components use Browser APIs like `window`?
**Answer:**
- Server Components execute strictly in Node.js, Bun, or Cloudflare V8 worker environments on the server.
- Globals like `window`, `document`, and `navigator` do not exist in these server runtimes; referencing them throws a fatal `ReferenceError: window is not defined`.

---

### Q97: What is Partial Prerendering (PPR) in Next.js 15 / React 19?
**Answer:**
- Combines the instant load speed of Static Site Generation (SSG) with the dynamic capabilities of Server-Side Rendering (SSR) in the **same HTTP response**.
- The static shell (Navbar, layout, product image) is pre-rendered at build time and served instantly from Edge CDN cache.
- The dynamic holes (User personalized cart, live pricing) stream in dynamically from the server within the same response.

---

### Q98: What are Asynchronous Scripts and Style support in React 19?
**Answer:**
- In React 19, rendering `<link rel="stylesheet">` or `<script async>` inside components causes React to manage precedence, deduplicate stylesheet links, and ensure styles are loaded into the DOM before revealing component content to prevent layout shifts.

---

### Q99: How does React 19 handle asset preloading (`preload`, `preinit`)?
**Answer:**
React 19 introduces native imperative resource hint functions from `react-dom`:
- `preload(href, { as: 'image' })`
- `preinit(href, { as: 'script' })`
- Guarantees critical assets begin downloading as early as possible during server rendering.

---

### Q100: How do you migrate an existing React 18 application to React 19?
**Answer:**
1. Upgrade dependencies: `npm install react@latest react-dom@latest`.
2. Run official React 19 codemod: `npx codemod@latest react/19/migration-recipe`.
3. Replace deprecated `forwardRef` with direct `ref` props.
4. Replace `useFormState` with `useActionState`.
5. Remove manual `useMemo`/`useCallback` if adopting the React Compiler.
6. Verify that `<Context.Provider>` is replaced with clean `<Context>` elements (supported in React 19).
