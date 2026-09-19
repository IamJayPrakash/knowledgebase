# Top Next.js Senior Interview Questions (App Router & Production Architecture)

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
