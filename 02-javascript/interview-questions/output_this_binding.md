# Tricky Output Questions: `this` Binding & Arrow Functions

---

## Problem 1: Object Method vs Detached Callback

### Code:
```javascript
const user = {
  name: "Jay",
  getName() {
    return this.name;
  },
  getArrowName: () => {
    return this.name;
  }
};

const extracted = user.getName;

console.log(user.getName());
console.log(extracted());
console.log(user.getArrowName());
```

### Output:
```
Jay
undefined (or Window name in non-strict browser)
undefined
```

### Explanation:
1. `user.getName()`: Method invocation with dot notation. The object left of the dot (`user`) becomes the `this` context. Returns `"Jay"`.
2. `extracted()`: The function reference was copied to a standalone variable and invoked without dot notation. Default binding applies: in strict mode `this` is `undefined`, in non-strict browser it is `window`. Returns `undefined`.
3. `user.getArrowName()`: Arrow functions do **not** have their own `this`. They capture `this` lexically from the enclosing lexical scope at declaration time. Here, the enclosing scope of the object literal is the global/module scope (not the `user` object!), where `name` is undefined.

---

## Problem 2: Nested Arrow Functions & Arguments

### Code:
```javascript
const obj = {
  count: 10,
  regular() {
    return function() {
      console.log("A:", this.count);
    };
  },
  arrow() {
    return () => {
      console.log("B:", this.count);
    };
  }
};

obj.regular()();
obj.arrow()();
```

### Output:
```
A: undefined
B: 10
```

### Explanation:
- `obj.regular()` returns a standard function. When invoked as `()`, it has default binding (`this` = `global` or `undefined`). Hence `this.count` is `undefined`.
- `obj.arrow()` was invoked with `obj` as `this`. Inside `arrow()`, `this` points to `obj`. The returned arrow function lexically captures this exact `this` reference. When invoked as `()`, it retains `obj` as `this`, printing `10`.
