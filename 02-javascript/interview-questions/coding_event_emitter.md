# Machine Coding: Production-Ready Custom `EventEmitter`

---

## 🐣 1. Layman's Analogy

`EventEmitter` ek newspaper publishing agency ki tarah hai. Readers aate hain aur kisi topic ke liye subscribe karte hain (`emitter.on('sports', callback)`). Jab bhi sports department nayi khabar print karta hai (`emitter.emit('sports', news)`), agency har subscribed reader ke ghar newspaper bhej deti hai. Agar koi reader subscription cancel kare (`emitter.off('sports', callback)`), use aage se khabar nahi milti.

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
/**
 * Production EventEmitter with on, once, off, emit, and listener count
 */
class EventEmitter {
  constructor() {
    // Line 8: Internal storage for events: { [eventName: string]: Function[] }
    this._events = Object.create(null);
    // Line 10: Default max listener limit to prevent accidental memory leaks
    this._maxListeners = 10;
  }

  // Line 14: Subscribe a listener to an event
  on(eventName, listener) {
    if (typeof listener !== "function") {
      throw new TypeError("Listener must be a function");
    }

    // Line 20: Initialize listener array if not present
    if (!this._events[eventName]) {
      this._events[eventName] = [];
    }

    // Line 25: Memory leak warning detection
    if (this._events[eventName].length >= this._maxListeners) {
      console.warn(
        `[Warning] Possible EventEmitter memory leak detected. ` +
        `${this._events[eventName].length + 1} ${String(eventName)} listeners added.`
      );
    }

    // Line 33: Add listener to event queue
    this._events[eventName].push(listener);

    // Line 36: Return unsubscription function for ergonomic cleanup
    return () => this.off(eventName, listener);
  }

  // Line 40: Subscribe a one-time listener that self-removes after single trigger
  once(eventName, listener) {
    if (typeof listener !== "function") {
      throw new TypeError("Listener must be a function");
    }

    // Line 46: Create wrapper that unregisters itself before executing callback
    const onceWrapper = (...args) => {
      this.off(eventName, onceWrapper);
      listener.apply(this, args);
    };

    // Line 52: Save original reference so .off(eventName, listener) still works
    onceWrapper.originalListener = listener;

    return this.on(eventName, onceWrapper);
  }

  // Line 58: Trigger all listeners registered under eventName with arguments
  emit(eventName, ...args) {
    const listeners = this._events[eventName];
    if (!listeners || listeners.length === 0) {
      return false;
    }

    // Line 65: Clone listener array with .slice() to prevent mutation issues
    // if a listener calls .off() during execution
    const handlers = listeners.slice();

    for (let i = 0; i < handlers.length; i++) {
      try {
        handlers[i].apply(this, args);
      } catch (error) {
        // Line 73: Isolate handler exceptions so other listeners still execute
        console.error(`Error in event listener for ${String(eventName)}:`, error);
      }
    }

    return true;
  }

  // Line 81: Unsubscribe a specific listener
  off(eventName, listener) {
    const listeners = this._events[eventName];
    if (!listeners || listeners.length === 0) {
      return this;
    }

    // Line 88: Filter out target listener or matching onceWrapper
    this._events[eventName] = listeners.filter(
      (fn) => fn !== listener && fn.originalListener !== listener
    );

    // Line 93: Clean up empty event keys to prevent memory fragmentation
    if (this._events[eventName].length === 0) {
      delete this._events[eventName];
    }

    return this;
  }

  // Line 101: Remove all listeners for a specific event or all events
  removeAllListeners(eventName) {
    if (eventName) {
      delete this._events[eventName];
    } else {
      this._events = Object.create(null);
    }
    return this;
  }

  // Line 111: Get count of active listeners for an event
  listenerCount(eventName) {
    return this._events[eventName] ? this._events[eventName].length : 0;
  }
}

// ==========================================
// Verification Tests
// ==========================================
const bus = new EventEmitter();

const onOrder = (id, amount) => console.log(`Order placed: ${id}, Amount: $${amount}`);
const unsubscribe = bus.on("order", onOrder);

bus.emit("order", "ORD-101", 250); // Order placed: ORD-101, Amount: $250

bus.once("greet", (name) => console.log(`Welcome, ${name}!`));
bus.emit("greet", "Jay"); // Welcome, Jay!
bus.emit("greet", "Jay"); // (Nothing prints, single-fire executed)

unsubscribe();
bus.emit("order", "ORD-102", 500); // (Nothing prints, successfully unsubscribed)
```
