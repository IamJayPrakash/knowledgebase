# Machine Coding: Custom Virtualized List (DOM Windowing from Scratch)

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
