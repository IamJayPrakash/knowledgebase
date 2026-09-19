# Node.js Master Interview Bank: Part 3 (Q41 - Q60)
## Express.js, Security, Fastify & Production Scaling

---

### Q41: How does the Express.js Middleware Pipeline work under the hood?
**Answer:**
- In Express, an application is essentially a stack of middleware functions.
- Every middleware has the signature: `function(req, res, next)`:
  - `req`: HTTP request wrapper.
  - `res`: HTTP response wrapper.
  - `next()`: Passes control to the **next middleware in the stack**.
- **The Internal Mechanism:**
  Express iterates through an array of layer objects (`app._router.stack`). Calling `next()` advances the stack pointer and executes the next matched route handler.
  - If a middleware fails to call `next()` AND does not send a response (`res.send()`), the **HTTP request hangs indefinitely** until client socket timeout!

---

### Q42: Why must Express Error-Handling Middleware have EXACTLY 4 arguments?
**Answer:**
```javascript
// ✅ MUST have exactly 4 parameters: (err, req, res, next)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});
```
**Why:**
Express inspects the function's arity using **`fn.length`** (the number of declared arguments).
- If `fn.length === 4`, Express registers it as an **Error-Handling Middleware**.
- When any preceding middleware calls `next(err)` with an argument, Express **bypasses all normal 3-argument middleware** and jumps straight to the first 4-argument error handler!
- If you declare `(err, req, res)` with only 3 arguments, `fn.length` is 3, Express treats it as a normal middleware, and errors bypass it completely!

---

### Q43: How do you implement a robust Graceful Shutdown in Node.js?
**Answer:**
```javascript
const server = app.listen(3000);

async function gracefulShutdown(signal) {
  console.log(`Received ${signal}. Initiating graceful shutdown...`);

  // 1. Stop accepting new HTTP connections
  server.close(async () => {
    console.log('HTTP server closed.');

    try {
      // 2. Close database connection pools
      await dbPool.end();
      // 3. Disconnect from Redis / Kafka
      await redisClient.quit();
      console.log('Database and cache connections closed cleanly.');
      process.exit(0); // Exit with success
    } catch (err) {
      console.error('Error during cleanup:', err);
      process.exit(1);
    }
  });

  // 4. Force termination if connections don't drain within 25 seconds
  setTimeout(() => {
    console.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 25000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

### Q44: What is ReDoS (Regular Expression Denial of Service) and how do you prevent it?
**Answer:**
- **ReDoS:** Occurs when an insecure regular expression with exponential backtracking is evaluated against crafted user input:
  - *Vulnerable Regex:* `/^(a+)+$/`
  - *Payload:* `"aaaaaaaaaaaaaaaaaaaaaaaaaaaa!"`
  - The regex engine takes **billions of computational steps**, pinning the single-threaded CPU at 100% and freezing the entire Node.js server for all users!
- **Prevention:**
  1. Avoid nested quantifiers (`(a+)+` or `(a|a)+`).
  2. Use linters like `eslint-plugin-regexp`.
  3. Use non-backtracking regular expression engines (e.g. Google's `re2`).

---

### Q45: What security HTTP headers does `helmet` configure in Express?
**Answer:**
`app.use(helmet())` automatically sets 11+ security headers:
1. **`Content-Security-Policy` (CSP):** Mitigates XSS by restricting allowed script sources.
2. **`Strict-Transport-Security` (HSTS):** Enforces HTTPS connections.
3. **`X-Frame-Options: DENY`:** Prevents **Clickjacking** by disallowing the page inside iframes.
4. **`X-Content-Type-Options: nosniff`:** Prevents MIME-type sniffing attacks.
5. **`X-DNS-Prefetch-Control`:** Controls browser DNS prefetching.
6. **`Referrer-Policy`:** Restricts sensitive URL paths in Referer headers.

---

### Q46: Compare Express vs Fastify architectural differences.
**Answer:**
| Dimension | Express.js | Fastify |
| :--- | :--- | :--- |
| **Routing Algorithm**| Linear regex matching across route stack ($O(N)$). | **Radix Tree routing** ($O(K)$ where $K$ is URL path length). |
| **JSON Serialization**| Standard `JSON.stringify()` (pure V8, slow). | **`fast-json-stringify`** (compiles JSON schema into optimized code; 2x faster). |
| **Async Support** | Express 4 requires third-party wrapper for async route errors. | **Native `async/await`** support with built-in promise error handling. |
| **Logging** | Requires manual Morgan/Winston setup. | Built-in high-performance **Pino logger**. |
| **Throughput** | ~20,000 req/sec | **~50,000+ req/sec** |

---

### Q47: How does PM2 manage Node.js processes in Production?
**Answer:**
- **Cluster Mode (`pm2 start app.js -i max`):**
  Uses the native `node:cluster` module to spawn one worker process per CPU core, sharing port 80/443 with built-in round-robin load balancing.
- **Zero-Downtime Reload (`pm2 reload all`):**
  Restarts worker processes **one by one in a rolling fashion**. The old process is only killed after the new process signals it is listening, eliminating downtime during deployments!

---

### Q48: How do you prevent Cross-Site Scripting (XSS) in Node.js?
**Answer:**
1. **Never Render Raw User HTML:** Always sanitize user input using libraries like `DOMPurify` or `sanitize-html`.
2. **HttpOnly Cookies:** Store sensitive JWT tokens in `HttpOnly` cookies so JavaScript cannot access them via `document.cookie`.
3. **Strict Content-Security-Policy (CSP):** Disallow inline script execution (`'unsafe-inline'`).

---

### Q49: What is the difference between Authentication and Authorization in Express?
**Answer:**
- **Authentication (AuthN):** Verifying *who the user is* (e.g. validating JWT signature, verifying username and password). Middleware: `authenticateJwt`.
- **Authorization (AuthZ):** Verifying *what the user is permitted to do* (e.g. checking if `user.role === 'ADMIN'`). Middleware: `requireRole('ADMIN')`.

---

### Q50: How do you implement Rate Limiting in Express?
**Answer:**
Use `express-rate-limit` backed by Redis:
```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                  // Limit each IP to 100 requests per window
  standardHeaders: true,     // Return standard RateLimit headers
  legacyHeaders: false,
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
});

app.use('/api/', limiter);
```

---

### Q51: What is the `cookie-parser` signed cookie feature?
**Answer:**
- `app.use(cookieParser('my-secret-key'))`
- When setting signed cookies (`res.cookie('user', '123', { signed: true })`), Express generates an HMAC-SHA256 signature of the cookie value.
- On subsequent requests, Express verifies the signature. If a user tampers with the cookie value in browser DevTools, the signature check fails and Express rejects the cookie.

---

### Q52: What is Parameter Pollution (HPP) and how do you protect against it?
**Answer:**
- Occurs when an attacker supplies multiple values for the same HTTP query parameter: `/search?role=user&role=admin`.
- In Express, `req.query.role` becomes an array `['user', 'admin']` instead of a string, which can bypass naive type checks:
  `if (req.query.role !== 'admin') allow();` (evaluates to true because `['user', 'admin'] !== 'admin'`).
- **Protection:** Use `hpp` middleware (`app.use(hpp())`), which sanitizes `req.query` to retain only the last parameter value.

---

### Q53: How do you handle file uploads in Express safely?
**Answer:**
- Use **`multer`** with disk storage or cloud streaming:
  ```javascript
  const multer = require('multer');
  const upload = multer({
    limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
    fileFilter: (req, file, cb) => {
      if (['image/jpeg', 'image/png'].includes(file.mimetype)) {
        cb(null, true);
      } else {
        cb(new Error('Invalid file type!'), false);
      }
    }
  });
  ```

---

### Q54: What is Server-Timing header and why is it useful?
**Answer:**
- An HTTP response header allowing the Node.js backend to communicate server-side execution timing directly to the browser DevTools:
  ```http
  Server-Timing: db;dur=45.2, auth;dur=12.1, cache;desc="miss"
  ```
- Appears directly in the Chrome DevTools **Network Waterfall Timing tab**, eliminating guesswork regarding backend latencies.

---

### Q55: What is the difference between `res.send()`, `res.json()`, and `res.end()`?
**Answer:**
- **`res.end()`:** Core Node.js method. Ends the response process immediately without sending any body or formatting headers.
- **`res.send(data)`:** Express helper. Automatically sets `Content-Type` based on argument type (sets `text/html` for strings, `application/json` for objects, `application/octet-stream` for buffers) and calculates `Content-Length`.
- **`res.json(obj)`:** Express helper. Explicitly formats data with `JSON.stringify()` and sets `Content-Type: application/json`.

---

### Q56: How do you configure HTTP Keep-Alive in Node.js HTTP servers?
**Answer:**
- By default, Node.js HTTP servers enable Keep-Alive to reuse persistent TCP connections across multiple HTTP requests.
- Configure timeouts:
  ```javascript
  const server = http.createServer(app);
  server.keepAliveTimeout = 65000;  // 65 seconds
  server.headersTimeout = 66000;    // 66 seconds (MUST be greater than keepAliveTimeout!)
  ```
  *(Keeping timeout higher than upstream AWS ALB 60s timeout prevents ALB 502 Bad Gateway race conditions).*

---

### Q57: What is Session Fixation and how do you prevent it?
**Answer:**
- An attack where an attacker forces a victim to use a known session ID (e.g. by sending a link with `sessionId=xyz`). When the victim logs in, the attacker hijacks their authenticated session.
- **Prevention:** Always **regenerate the session ID upon authentication**:
  `req.session.regenerate((err) => { ... });`.

---

### Q58: How do you prevent Node.js Timing Attacks in Cryptographic comparisons?
**Answer:**
- Comparing secret tokens with `===` or `==` exits at the first non-matching character, leaking secret length and prefix characters based on execution time.
- **Solution:** Always use **`crypto.timingSafeEqual(bufA, bufB)`**, which executes in constant time regardless of where mismatches occur.

---

### Q59: What is `NODE_OPTIONS` environment variable?
**Answer:**
- Allows passing command-line flags to the Node.js runtime without altering startup scripts:
  `NODE_OPTIONS="--max-old-space-size=4096 --inspect=0.0.0.0:9229" node server.js`.

---

### Q60: How do you implement Structured JSON Logging in Node.js for production?
**Answer:**
- Never use `console.log()` in production (it is synchronous when writing to files/ttys and lacks structured metadata).
- Use **`pino`**:
  ```javascript
  const logger = require('pino')();
  logger.info({ userId: '123', event: 'LOGIN_SUCCESS', durationMs: 42 });
  ```
  Writes high-speed, machine-readable JSON logs directly to `stdout`, easily parsed by Elasticsearch, Datadog, or Fluentd.
