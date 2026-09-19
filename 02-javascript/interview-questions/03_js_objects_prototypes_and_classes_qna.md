# JavaScript Master Interview Bank: Part 3 (Q41 - Q60)
## Objects, Prototypes, Inheritance & ES6 Classes

---

### Q41: What is the Prototype Chain in JavaScript?
**Answer:**
- In JavaScript, objects have an internal hidden property `[[Prototype]]` (accessible via `Object.getPrototypeOf()` or legacy `__proto__`).
- When accessing a property on an object:
  1. The engine checks if the property exists as an **own property** on that object.
  2. If not found, it traverses the object's `[[Prototype]]`.
  3. It continues ascending up the chain until it finds the property or reaches `Object.prototype.[[Prototype]]`, which is `null`.
  4. If `null` is reached without finding the property, it returns `undefined`.

```javascript
const parent = { greet() { return "Hello from parent"; } };
const child = Object.create(parent);

console.log(child.greet()); // "Hello from parent" (delegated through prototype)
console.log(child.hasOwnProperty("greet")); // false
```

---

### Q42: What is the difference between `__proto__` and `prototype`?
**Answer:**
- **`prototype`**: A property that exists **only on functions** (specifically constructor functions and ES6 classes, but NOT arrow functions). It defines what object will become the `[[Prototype]]` of instances created using `new MyFunction()`.
- **`__proto__`**: An accessor property on `Object.prototype` (getter/setter) that exposes the internal `[[Prototype]]` of **every object instance**.

```javascript
function Person(name) {
  this.name = name;
}
Person.prototype.sayHi = function() { return `Hi, ${this.name}`; };

const alice = new Person("Alice");

console.log(alice.__proto__ === Person.prototype); // true
console.log(Person.__proto__ === Function.prototype); // true
console.log(Person.prototype.constructor === Person); // true
```

---

### Q43: What does the `new` keyword actually do under the hood? Write a polyfill for `new`.
**Answer:**
When `new Constructor(...args)` is executed, 4 distinct operations happen:
1. A new, empty plain object is created.
2. The new object's `[[Prototype]]` is set to `Constructor.prototype`.
3. `Constructor` is invoked with its `this` bound to the newly created object.
4. If `Constructor` returns an object, that object is returned. Otherwise, the newly created object from Step 1 is returned.

```javascript
function customNew(Constructor, ...args) {
  // Step 1 & 2: Create object linked to constructor prototype
  const obj = Object.create(Constructor.prototype);

  // Step 3: Invoke constructor with newly created context
  const result = Constructor.apply(obj, args);

  // Step 4: Return result if it is an object, else fallback to obj
  return (typeof result === "object" && result !== null) ? result : obj;
}
```

---

### Q44: What is `Object.create(null)` and why is it preferred over `{}` for dictionaries/lookup maps?
**Answer:**
- `{}` (or `new Object()`) inherits from `Object.prototype`, which includes default properties and methods like `toString`, `valueOf`, `constructor`, `hasOwnProperty`.
- **Vulnerability:** If user-supplied keys are placed into a plain object, keys matching built-in prototype names can corrupt lookups or cause prototype pollution bugs.
- `Object.create(null)` creates a truly bare object with `[[Prototype]] === null`. It has **zero inherited properties**, making it a clean, unpollutable dictionary.

```javascript
const dict = Object.create(null);
console.log(dict.toString); // undefined (pure key-value container)
```

---

### Q45: How does ES6 `class` syntax desugar to Prototypal Inheritance?
**Answer:**
ES6 classes are **syntactic sugar** over constructor functions and prototypal inheritance:
- The class body becomes the constructor function.
- Methods defined inside the class body are added to `Class.prototype`.
- `static` methods are added directly to the constructor function itself (`Class.method`).
- `extends` sets up the prototype chain between child and parent prototypes using `Object.setPrototypeOf(Child.prototype, Parent.prototype)` and `Object.setPrototypeOf(Child, Parent)`.

```javascript
// ES6 Class:
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} makes a noise.`; }
}

// Desugared ES5 Prototype Equivalent:
function AnimalES5(name) {
  this.name = name;
}
AnimalES5.prototype.speak = function() {
  return this.name + " makes a noise.";
};
```

---

### Q46: What happens if a constructor function returns a primitive vs an object?
**Answer:**
- If a constructor explicitly returns a **primitive** (e.g. `return 42`, `return "error"`, `return null`), the return statement is **completely ignored** and the newly created `this` instance is returned.
- If it explicitly returns an **object** (e.g. `return { custom: true }`), that returned object **replaces** `this` and becomes the result of `new`.

```javascript
function Foo() {
  this.value = 1;
  return 100; // Primitive ignored!
}
console.log(new Foo().value); // 1

function Bar() {
  this.value = 1;
  return { custom: 99 }; // Object replaces instance!
}
console.log(new Bar().value); // undefined (returns { custom: 99 })
```

---

### Q47: What are Property Descriptors (`writable`, `enumerable`, `configurable`)?
**Answer:**
Every property on an object is backed by a Property Descriptor with attributes:
- **`value`**: The actual data stored.
- **`writable`**: If `true`, the property value can be modified using an assignment operator.
- **`enumerable`**: If `true`, the property shows up in `for...in` loops and `Object.keys()`.
- **`configurable`**: If `true`, the property can be deleted from the object, and its descriptor attributes (other than `value` and turning `writable` false) can be modified.

```javascript
const obj = {};
Object.defineProperty(obj, "apiKey", {
  value: "SECRET_KEY",
  writable: false,     // Cannot reassign
  enumerable: false,   // Hidden from Object.keys()
  configurable: false  // Cannot delete or redefine
});

console.log(Object.keys(obj)); // [] (enumerable: false)
// obj.apiKey = "NEW"; // Throws TypeError in strict mode
// delete obj.apiKey;  // Throws TypeError in strict mode
```

---

### Q48: What is Prototype Pollution and how can you defend against it?
**Answer:**
- **Prototype Pollution** is a vulnerability where an attacker exploits unvalidated user input (like merging recursive JSON objects) to inject properties directly onto `Object.prototype`.
- Once polluted, the injected property automatically becomes accessible on **all objects** across the application.
- **Defenses:**
  1. Use `Object.create(null)` or `new Map()` for arbitrary key lookups.
  2. Freeze the base prototype at startup: `Object.freeze(Object.prototype)`.
  3. Validate property keys and reject keys named `"__proto__"`, `"constructor"`, or `"prototype"`.

```javascript
// Vulnerable recursive merge:
function insecureMerge(target, source) {
  for (let key in source) {
    if (typeof target[key] === "object" && typeof source[key] === "object") {
      insecureMerge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}
// Payload: JSON.parse('{"__proto__": {"isAdmin": true}}')
```

---

### Q49: How do Private Class Fields (`#field`) differ from TypeScript `private`?
**Answer:**
- **TypeScript `private`:** Enforced only at **compile-time**. At runtime, it compiles to standard public properties that can be inspected and modified by anyone.
- **JavaScript Native Private Fields (`#`):** Enforced by the **engine at runtime** using internal slots (Hard Privacy). Accessing `#field` outside the class throws a syntax error. It cannot be accessed via reflection, `Object.keys()`, or `getOwnPropertyNames()`.

```javascript
class BankAccount {
  #balance = 1000; // True private runtime field

  getBalance() {
    return this.#balance;
  }
}

const account = new BankAccount();
// console.log(account.#balance); // SyntaxError: Private field '#balance' must be declared
```

---

### Q50: How do Getters and Setters work in JavaScript classes and objects?
**Answer:**
Getters and setters bind an object property to a function that will be called when that property is looked up or assigned:
- **`get prop()`**: Computed property that returns a value on access. Takes 0 parameters.
- **`set prop(value)`**: Invoked on property assignment. Accepts exactly 1 parameter.

```javascript
class Temperature {
  constructor(celsius) {
    this._celsius = celsius;
  }

  get fahrenheit() {
    return (this._celsius * 9) / 5 + 32;
  }

  set fahrenheit(f) {
    this._celsius = ((f - 32) * 5) / 9;
  }
}

const temp = new Temperature(25);
console.log(temp.fahrenheit); // 77
temp.fahrenheit = 32;
console.log(temp._celsius);   // 0
```

---

### Q51: What is the `super` keyword and how does it work in constructor and method contexts?
**Answer:**
- **In Subclass Constructor:** Must be called before accessing `this` (`super(...)`). It invokes the parent constructor, which initializes `this` based on the parent class.
- **In Method Context:** References methods on the prototype of the parent class (`super.speak()`), enabling method overriding while preserving access to base implementations.

---

### Q52: What is the difference between `Object.assign()` and the Object Spread operator (`...`)?
**Answer:**
- **`Object.assign(target, ...sources)`:**
  - Mutates and returns the `target` object.
  - Triggers **setters** on the `target` object.
- **Spread Operator (`{ ...source }`):**
  - Always creates and returns a **new plain object**.
  - Defines properties on the new object (does not invoke prototype setters).
  - Both perform shallow copies.

---

### Q53: How do you implement Multiple Inheritance / Mixins in JavaScript?
**Answer:**
JavaScript supports single prototypal inheritance only. To combine capabilities from multiple sources, use the **Mixin Pattern**:

```javascript
const Timestampable = (Base) => class extends Base {
  getCreatedAt() { return this.createdAt || (this.createdAt = new Date()); }
};

const Serializable = (Base) => class extends Base {
  toJSON() { return JSON.stringify(this); }
};

class Entity {
  constructor(id) { this.id = id; }
}

// Compose mixins:
class User extends Timestampable(Serializable(Entity)) {
  constructor(id, name) {
    super(id);
    this.name = name;
  }
}

const user = new User(1, "Alice");
console.log(user.getCreatedAt());
console.log(user.toJSON());
```

---

### Q54: What is `instanceof` and how can its behavior be overridden?
**Answer:**
- `a instanceof B` checks whether `B.prototype` appears anywhere in the prototype chain of `a`.
- **Overriding:** In ES6, `instanceof` delegates to the static well-known symbol `Symbol.hasInstance`:

```javascript
class SpecialArray {
  static [Symbol.hasInstance](instance) {
    return Array.isArray(instance);
  }
}

console.log([] instanceof SpecialArray); // true!
```

---

### Q55: What is the `in` operator vs `hasOwnProperty()` vs `Object.hasOwn()`?
**Answer:**
- **`prop in obj`**: Returns `true` if `prop` exists on `obj` **or anywhere in its prototype chain**.
- **`obj.hasOwnProperty(prop)`**: Returns `true` only if `prop` is an **own property** of `obj`. *Flaw:* Fails on `Object.create(null)` or if overridden as an own property.
- **`Object.hasOwn(obj, prop)` (ES2022 Standard):** Static method that safely checks own properties, replacing `hasOwnProperty`. Works on objects with `null` prototype.

---

### Q56: How do Static Blocks in ES2022 classes work?
**Answer:**
- Static initialization blocks (`static { ... }`) execute once when the class is loaded/evaluated.
- They have access to private fields and methods of the class, allowing complex initialization and sharing of private internals with external helpers.

```javascript
class Database {
  static #connection;

  static {
    try {
      this.#connection = "mongodb://localhost:27017";
    } catch (e) {
      this.#connection = "fallback://memory";
    }
  }
}
```

---

### Q57: What is the difference between an Object and a JSON string?
**Answer:**
- **JavaScript Object:** In-memory runtime data structure that can contain functions, undefined, Symbols, cyclic references, and prototypes.
- **JSON (JavaScript Object Notation):** Text-based data-interchange specification. Keys must be double-quoted strings. Values are restricted to strings, numbers, booleans, arrays, objects, and null. Cannot store functions, `undefined`, or circular references.

---

### Q58: What is Polymorphism in JavaScript and how is it demonstrated?
**Answer:**
Polymorphism allows different objects to respond to the same method call with behavior tailored to their specific type:
```javascript
class Shape {
  area() { throw new Error("Method not implemented"); }
}
class Circle extends Shape {
  constructor(r) { super(); this.r = r; }
  area() { return Math.PI * this.r ** 2; }
}
class Square extends Shape {
  constructor(s) { super(); this.s = s; }
  area() { return this.s ** 2; }
}

const shapes = [new Circle(5), new Square(4)];
shapes.forEach(s => console.log(s.area())); // Polymorphic dispatch
```

---

### Q59: What is `Object.seal()` vs `Object.freeze()` with respect to nested objects?
**Answer:**
Both methods are **shallow**. Neither method seals or freezes nested child objects.
To ensure complete immutability, you must implement a `deepFreeze` function:

```javascript
function deepFreeze(obj) {
  Object.keys(obj).forEach(prop => {
    if (typeof obj[prop] === "object" && obj[prop] !== null && !Object.isFrozen(obj[prop])) {
      deepFreeze(obj[prop]);
    }
  });
  return Object.freeze(obj);
}
```

---

### Q60: Explain `Symbol.toPrimitive` and custom object coercion.
**Answer:**
When an object is coerced to a primitive (e.g. in `+obj` or `obj + ""`), the engine checks for `[Symbol.toPrimitive]` with a `hint`.
The `hint` argument can be `"number"`, `"string"`, or `"default"`.


```javascript
const money = {
  amount: 50,
  currency: "USD",
  [Symbol.toPrimitive](hint) {
    if (hint === "number") return this.amount;
    if (hint === "string") return `${this.amount} ${this.currency}`;
    return this.amount; // default
  }
};

console.log(+money);        // 50 (hint: number)
console.log(`${money}`);    // "50 USD" (hint: string)
console.log(money + 10);    // 60 (hint: default)
```
