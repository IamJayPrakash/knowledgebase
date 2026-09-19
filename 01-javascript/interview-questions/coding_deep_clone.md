# Machine Coding: Deep Clone with Circular References & Special Types

---

## 🐣 1. Layman's Analogy
Shallow clone photo copy machine ki tarah hai: agar paper par kisi dusre document ka reference link likha hai, toh copy mein bhi wahi link aayega. Agar link wala original page phat gaya, toh copy bhi bekar.
Deep clone 3D printer ki tarah hai: wo object ke har child, nested structure, date, regex aur circular loop ko bilkul naye fresh memory address pe recreate karta hai.

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
/**
 * Deep clones any JavaScript object handling:
 * 1. Primitives (numbers, strings, booleans, null, undefined, symbols, bigints)
 * 2. Circular references (via WeakMap memory hash)
 * 3. Dates & RegExp instances
 * 4. Maps & Sets
 * 5. Arrays & Plain Objects
 * 6. Symbol-keyed properties
 */
function deepClone(target, hash = new WeakMap()) {
  // Line 12: Primitives & functions are returned as-is (immutable or shared by reference)
  if (target === null || typeof target !== "object") {
    return target;
  }

  // Line 17: Special object type: Date
  if (target instanceof Date) {
    return new Date(target.getTime());
  }

  // Line 22: Special object type: RegExp
  if (target instanceof RegExp) {
    return new RegExp(target.source, target.flags);
  }

  // Line 27: Circular reference check
  // If we already cloned this object in this path, return existing cloned reference
  if (hash.has(target)) {
    return hash.get(target);
  }

  // Line 33: Handle Set data structure
  if (target instanceof Set) {
    const cloneSet = new Set();
    hash.set(target, cloneSet);
    target.forEach((value) => {
      cloneSet.add(deepClone(value, hash));
    });
    return cloneSet;
  }

  // Line 43: Handle Map data structure
  if (target instanceof Map) {
    const cloneMap = new Map();
    hash.set(target, cloneMap);
    target.forEach((value, key) => {
      cloneMap.set(deepClone(key, hash), deepClone(value, hash));
    });
    return cloneMap;
  }

  // Line 53: Initialize clone with identical prototype chain
  const cloneObj = Array.isArray(target)
    ? []
    : Object.create(Object.getPrototypeOf(target));

  // Line 58: Store cloned instance in hash map BEFORE traversing children to resolve cycles
  hash.set(target, cloneObj);

  // Line 61: Retrieve all own property keys, including non-enumerable and Symbol keys
  const allKeys = [
    ...Object.getOwnPropertyNames(target),
    ...Object.getOwnPropertySymbols(target)
  ];

  // Line 67: Recursively copy property descriptors and values
  for (const key of allKeys) {
    const descriptor = Object.getOwnPropertyDescriptor(target, key);
    
    // Only copy if configurable or writable (skip getters/setters unless defined as value)
    if (descriptor && "value" in descriptor) {
      descriptor.value = deepClone(target[key], hash);
    }
    
    // Line 76: Define property preserving original property flags (enumerable, writable)
    Object.defineProperty(cloneObj, key, descriptor);
  }

  return cloneObj;
}

// ==========================================
// Test Cases & Verification
// ==========================================
const original = {
  num: 42,
  str: "hello",
  date: new Date("2026-01-01"),
  regex: /^[a-z]+$/gi,
  set: new Set([1, 2, 3]),
  map: new Map([["key1", { nested: "val" }]]),
  [Symbol("id")]: 999
};

// Create Circular Reference
original.self = original;

const copy = deepClone(original);

console.log(copy !== original); // true
console.log(copy.self === copy); // true (circular link preserved!)
console.log(copy.date instanceof Date); // true
console.log(copy.map.get("key1") !== original.map.get("key1")); // true (deeply cloned)
```

---

## 🎯 3. The "Interview Pitch"
> "While `structuredClone()` is the modern native browser and Node.js standard for deep cloning, it has key limitations: it cannot clone functions or DOM nodes. In senior technical interviews, writing a custom `deepClone` demonstrates mastery of memory models. The essential technical requirements are: checking for null and primitives first, handling constructors like `Date` and `RegExp`, maintaining a `WeakMap` memo cache to prevent infinite stack overflows from circular references, cloning `Map` and `Set` collections, and extracting all keys via `Object.getOwnPropertyNames` and `Object.getOwnPropertySymbols` while preserving descriptor attributes with `Object.defineProperty`."
