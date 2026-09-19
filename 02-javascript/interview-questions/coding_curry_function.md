# Machine Coding: Infinite Currying & Generalized Currying

---

## 🐣 1. Layman's Analogy

Currying ek assembly line pizza counter ki tarah hai. Ek bar mein pura pizza lene ke bajaye, aap pehle crust select karte ho `order('thin')`, fir agle counter pe cheese `('mozzarella')`, fir agle counter pe toppings `('jalapeno')`. Jab sare mandatory ingredients poore ho jate hain, chef pizza deliver kar deta hai!

---

## 💻 2. Line-by-Line Commented Code Solutions

### Variant A: Generalized Currying based on Function Arity (`fn.length`)

```javascript
/**
 * Transforms a multi-argument function into a curried function
 * that executes once all expected parameters (arity) are supplied.
 */
function curry(fn) {
  // Line 8: Return a wrapper function that collects arguments
  return function curried(...args) {
    // Line 10: Compare collected arguments count with target function arity
    if (args.length >= fn.length) {
      // Line 12: If we have enough arguments, execute the original function
      return fn.apply(this, args);
    } else {
      // Line 15: If not enough, return a new function that accumulates further args
      return function(...nextArgs) {
        // Line 17: Recursively collect and merge arguments
        return curried.apply(this, args.concat(nextArgs));
      };
    }
  };
}

// Testing Generalized Currying
function sum3(a, b, c) {
  return a + b + c;
}

const curriedSum = curry(sum3);
console.log(curriedSum(1)(2)(3)); // 6
console.log(curriedSum(1, 2)(3)); // 6
console.log(curriedSum(1)(2, 3)); // 6
```

---

### Variant B: Infinite Currying with Value Extraction (`sum(1)(2)...(n)()`)

```javascript
/**
 * Infinite currying terminating on empty parentheses invocation ()
 */
function infiniteCurry(a) {
  // Line 38: Return internal collector function
  return function(b) {
    // Line 40: Check if empty argument passed to terminate
    if (b === undefined) {
      return a;
    }
    // Line 44: Recursively return new curry with accumulated sum
    return infiniteCurry(a + b);
  };
}

console.log(infiniteCurry(1)(2)(3)(4)()); // 10
console.log(infiniteCurry(5)(10)());      // 15
```

---

### Variant C: Infinite Currying via `valueOf` / `toString` Override

```javascript
/**
 * Infinite currying that automatically coerces to a primitive number
 * when used in comparisons or arithmetic (e.g. sum(1)(2)(3) == 6)
 */
function autoSum(a) {
  let currentSum = a;

  function inner(b) {
    currentSum += b;
    return inner;
  }

  // Override primitive coercion hooks
  inner.valueOf = function() {
    return currentSum;
  };

  inner.toString = function() {
    return String(currentSum);
  };

  return inner;
}

console.log(autoSum(1)(2)(3) == 6); // true
console.log(Number(autoSum(5)(10)(20))); // 35
```
