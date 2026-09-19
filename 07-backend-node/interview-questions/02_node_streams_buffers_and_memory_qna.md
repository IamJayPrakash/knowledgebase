# Node.js Master Interview Bank: Part 2 (Q21 - Q40)
## Streams, Backpressure, Buffers & Memory Management

---

### Q21: What are the 4 types of Streams in Node.js?
**Answer:**
1. **Readable:** Streams from which data can be consumed (`fs.createReadStream()`, `http.IncomingMessage`, `process.stdin`).
2. **Writable:** Streams to which data can be written (`fs.createWriteStream()`, `http.ServerResponse`, `process.stdout`).
3. **Duplex:** Streams that are both Readable and Writable (e.g. `net.Socket` TCP connection). Reads and writes operate independently.
4. **Transform:** A Duplex stream where output is computed from input (e.g. `zlib.createGzip()` compression, `crypto.createCipher()`).

---

### Q22: What is Backpressure in Node.js Streams and how do you handle it?
**Answer:**
- **Backpressure:** Occurs when a Readable stream produces data faster than a Writable stream can write it to disk or network socket (e.g. reading a 10GB file from SSD and sending it over a slow 3G network).
- If unmanaged, the incoming chunks accumulate in RAM, exhausting the V8 heap and crashing the server with OOM!
- **Handling with `highWaterMark` and `drain`:**
  - `writable.write(chunk)` returns `false` when internal buffer reaches `highWaterMark` (default: 16KB for object streams, 64KB for byte streams).
  - When `false` is returned, the Readable stream **MUST pause**: `readable.pause()`.
  - When the Writable stream finishes draining its buffer, it emits the **`'drain'` event**.
  - On `'drain'`, resume reading: `readable.resume()`.

```javascript
function streamWithBackpressure(readable, writable) {
  readable.on('data', (chunk) => {
    const canAcceptMore = writable.write(chunk);
    if (!canAcceptMore) {
      readable.pause(); // Pause reading!
    }
  });

  writable.on('drain', () => {
    readable.resume(); // Resume reading!
  });
}
```

---

### Q23: Why should you ALWAYS use `stream.pipeline()` instead of `readable.pipe()`?
**Answer:**
- **`readable.pipe(writable)` Flaw:**
  If the destination stream or source stream encounters an error, `pipe()` **does NOT automatically destroy the other streams**!
  - File descriptors and socket handles remain open in memory indefinitely, causing severe memory leaks.
- **`stream.pipeline(source, ...transforms, destination, callback)` (Standard):**
  - Properly forwards errors.
  - **Automatically closes and destroys all streams** in the pipeline if any stream throws an error or completes prematurely, guaranteeing zero resource leaks.

```javascript
const { pipeline } = require('node:stream/promises');
const fs = require('node:fs');
const zlib = require('node:zlib');

async function run() {
  await pipeline(
    fs.createReadStream('input.txt'),
    zlib.createGzip(),
    fs.createWriteStream('input.txt.gz')
  );
  console.log('Pipeline succeeded!');
}
```

---

### Q24: What is the difference between `Buffer.alloc()` and `Buffer.allocUnsafe()`?
**Answer:**
- **`Buffer.alloc(size)` (Safe):**
  Allocates a new buffer of specified size and **initializes all bytes to zero (`0x00`)**. Slower because every byte must be zeroed out.
- **`Buffer.allocUnsafe(size)` (Unsafe):**
  Allocates raw uninitialized memory segment. Extremely fast, but **retains old sensitive data that previously occupied that RAM block** (e.g. passwords, private keys, database credentials)!
  - *Security Vulnerability:* Sending an uninitialized buffer over a network socket leaks sensitive memory to attackers!

---

### Q25: How do Buffers relate to the V8 Garbage Collector?
**Answer:**
- Instances of `Buffer` represent raw binary data allocated **outside the V8 JavaScript Heap** in C++ native memory space (managed by `ArrayBuffer` in libuv).
- Because they are stored off-heap, large buffers do not increase V8 garbage collection pause times.
- However, the small JavaScript wrapper object resides inside the V8 heap. When the JS wrapper is garbage-collected, V8 triggers a C++ finalizer to free the native off-heap memory.

---

### Q26: How do you implement a Custom Transform Stream?
**Answer:**
Subclass `Transform` and implement `_transform(chunk, encoding, callback)`:

```javascript
const { Transform } = require('node:stream');

class UpperCaseTransform extends Transform {
  _transform(chunk, encoding, callback) {
    try {
      const upper = chunk.toString().toUpperCase();
      this.push(upper); // Output transformed chunk
      callback();       // Signal ready for next chunk
    } catch (err) {
      callback(err);    // Propagate error
    }
  }
}
```

---

### Q27: What are the 4 most common causes of Memory Leaks in Node.js?
**Answer:**
1. **Global Variables & Unbounded Caches:** Storing user session data or cache entries in plain JavaScript objects (`const cache = {}`) without TTL or size limits.
2. **Uncleared Timers:** `setInterval` holding references to large closures.
3. **Forgotten Event Listeners:** Attaching listeners to long-lived objects (`process.on('message')`) inside short-lived request handlers without calling `removeListener()`.
4. **Closures Retaining Parent Context:** Retaining references to large buffers or request objects in long-lived background callbacks.

---

### Q28: How do you take and analyze a Heap Snapshot in Node.js?
**Answer:**
1. Use the native `node:v8` module to write a snapshot programmatically:
   ```javascript
   const v8 = require('node:v8');
   const fs = require('node:fs');

   function takeSnapshot() {
     const stream = v8.getHeapSnapshot();
     stream.pipe(fs.createWriteStream(`heap-${Date.now()}.heapsnapshot`));
   }
   ```
2. Open Chrome browser $\to$ `chrome://inspect` $\to$ Open dedicated DevTools for Node.
3. In the **Memory** tab, click **Load** and upload the `.heapsnapshot` file.
4. Filter by **Retained Size** to pinpoint the exact object tree preventing garbage collection.

---

### Q29: What is `Buffer.concat()` and why is appending buffers in a loop an anti-pattern?
**Answer:**
```javascript
// ❌ ANTI-PATTERN: O(N^2) memory allocations!
let result = Buffer.alloc(0);
stream.on('data', chunk => {
  result = Buffer.concat([result, chunk]); // Allocates new buffer every time!
});
```
- **Why it's fatal:** Repeatedly calling `Buffer.concat` copies the entire accumulated buffer on every chunk, leading to quadratic memory churn and GC pauses.
- **Solution:** Push chunks into an array and call `Buffer.concat(chunks)` **once at the end**, or stream data directly to destination.

---

### Q30: How do Worker Threads communicate via `MessageChannel`?
**Answer:**
- `const { MessageChannel } = require('node:worker_threads');`
- Creates two interconnected communication ports: `port1` and `port2`.
- You can transfer `port2` to a worker thread via `postMessage()`, allowing direct, peer-to-peer thread communication without routing messages through the main parent thread.

---

### Q31: How do you share memory without copying between Worker Threads?
**Answer:**
Use **`SharedArrayBuffer`** and **`Atomics`**:
```javascript
// Main thread:
const sharedBuffer = new SharedArrayBuffer(1024); // 1KB shared memory
const sharedArray = new Int32Array(sharedBuffer);
worker.postMessage({ buffer: sharedBuffer }); // Zero-copy transfer!

// Worker thread:
Atomics.add(sharedArray, 0, 5); // Thread-safe atomic increment
```

---

### Q32: What is the difference between Paused Mode and Flowing Mode in Readable Streams?
**Answer:**
- **Flowing Mode:** Data is read from the underlying system automatically and provided to an application as quickly as possible via the `'data'` event or `pipe()`.
- **Paused Mode:** Data must be explicitly pulled from the stream by calling `readable.read()` on the `'readable'` event.
- Can switch between modes using `readable.pause()` and `readable.resume()`.

---

### Q33: What is the `StringDecoder` module and why should you use it over `chunk.toString()`?
**Answer:**
- Multi-byte UTF-8 characters (like emojis or non-English characters: `🎉`, `é`) occupy 2 to 4 bytes.
- When reading streams, a chunk boundary may split a multi-byte character in half!
  - Calling `chunk.toString()` on a partial byte produces corrupted characters (``).
- **`StringDecoder`**: Buffers incomplete multi-byte sequences internally and emits complete characters once the remaining bytes arrive in the next chunk.

---

### Q34: What is `process.hrtime.bigint()` and why is it preferred for performance benchmarking?
**Answer:**
- `Date.now()` is tied to the system clock, which can jump backward or forward during NTP synchronization.
- **`process.hrtime.bigint()`**: Monotonically increasing high-resolution timer measuring nanoseconds:
  ```javascript
  const start = process.hrtime.bigint();
  executeHeavyTask();
  const duration = process.hrtime.bigint() - start;
  console.log(`Took ${Number(duration) / 1e6} ms`);
  ```

---

### Q35: How do you handle graceful stream destruction on client disconnect?
**Answer:**
If an HTTP client disconnects while you are streaming a large file:
```javascript
res.on('close', () => {
  if (!res.writableEnded) {
    fileStream.destroy(); // Safely close file descriptor!
  }
});
```
Prevents leaking open disk file descriptors when clients abandon requests.

---

### Q36: What is the difference between `fs.promises` and standard callback `fs`?
**Answer:**
- `fs.promises` provides Promise-returning versions of all filesystem methods, enabling clean `async/await` syntax.
- Both use the underlying Libuv threadpool; performance is virtually identical, but `fs.promises` dramatically simplifies error handling.

---

### Q37: What is the purpose of `stream.Readable.from(iterable)`?
**Answer:**
- Converts any JavaScript Iterable, Async Iterable, or Array directly into a Readable stream:
  ```javascript
  const { Readable } = require('node:stream');

  async function* generate() {
    yield 'Hello ';
    yield 'World!';
  }

  const stream = Readable.from(generate());
  stream.pipe(process.stdout);
  ```

---

### Q38: How do you prevent prototype pollution in Node.js JSON parsing?
**Answer:**
- Pass a reviver function to `JSON.parse` or validate with JSON schemas (Zod / Joi):
  ```javascript
  function safeReviver(key, value) {
    if (key === '__proto__' || key === 'constructor') {
      return undefined; // Drop malicious prototype keys!
    }
    return value;
  }
  const cleanData = JSON.parse(rawPayload, safeReviver);
  ```

---

### Q39: What is `NODE_ENV=production` and what internal optimizations does it trigger?
**Answer:**
1. Disables verbose debugging stacks and hot-reloading watchers.
2. **Express View Caching:** Caches compiled view templates in memory.
3. **Database Drivers:** Disables query logging overhead.
4. **Third-Party Libraries:** Skips dev-only warnings and assertions (e.g. React/Vue SSR runs up to 3x faster).

---

### Q40: What is the `v8.getHeapSpaceStatistics()` API?
**Answer:**
- Returns statistics about the individual memory spaces in the V8 heap:
  `new_space`, `old_space`, `code_space`, `map_space`, `large_object_space`.
- Invaluable for monitoring memory growth in specific generational spaces before an Out-Of-Memory crash occurs.
