# Machine Coding: High-Performance Autocomplete Search with Debounce & Cache

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
