# Top Java & Spring Boot Senior Interview Questions

---

## 1. What is the difference between Virtual Threads and Platform Threads in Java 21?

- **Platform Threads**: Direct 1:1 mappings to OS kernel threads. Heavy ($\sim 1  ext{ MB}$ stack), expensive context switching, limited to $\sim 5,000$ concurrent threads per JVM.
- **Virtual Threads**: Managed by the JVM runtime in user-space. Lightweight ($\sim 1  ext{ KB}$ heap memory), run on top of carrier threads, unmounted during blocking I/O, allowing millions of concurrent threads.

---

## 2. Explain Spring Bean Scopes and Thread-Safety

- **Singleton** (Default): Exactly one instance per Spring IoC container. **Not thread-safe** if it holds mutable instance variables! Must be stateless.
- **Prototype**: A fresh new instance created every time the bean is requested.
- **Request**: Scoped to the lifecycle of a single HTTP request (Web apps).
- **Session**: Scoped to an HTTP Session.

---

## 3. How does `@Transactional` work in Spring Boot, and what causes it to fail silently?

- **How it works**: Uses Spring AOP dynamic proxies. The proxy intercepts the method call, opens a database transaction, invokes the target method, and commits upon completion (or rolls back on `RuntimeException`).
- **Common Failure Scenarios**:
  - **Self-Invocation**: Calling a `@Transactional` method from another method within the **same class** (`this.doWork()`) bypasses the Spring AOP proxy; transactions are completely ignored!
  - **Checked Exceptions**: By default, transactions roll back **only** for unchecked exceptions (`RuntimeException` and `Error`). Checked exceptions (`Exception`) commit unless specified: `@Transactional(rollbackFor = Exception.class)`.
  - **Non-Public Methods**: Applying `@Transactional` to `private` or `protected` methods is ignored by default proxies.

---

## 4. What is the difference between `@Controller` and `@RestController`?

- `@Controller`: Traditional Spring MVC annotation used for returning HTML view templates (JSP, Thymeleaf).
- `@RestController`: Convenience annotation combining `@Controller` and `@ResponseBody`. Automatically serializes returned objects into JSON/XML HTTP response bodies.

---

## 5. What are the key enhancements of Spring Boot 3 over Spring Boot 2?

- Requires **Java 17 baseline** (supports Java 21 Virtual Threads natively).
- Upgraded to **Jakarta EE 10** (namespace changed from `javax.*` to `jakarta.*`).
- Native compilation via **GraalVM Native Image** support for sub-second startup and low memory footprints.
- Observability overhaul with **Micrometer Tracing** and OpenTelemetry integration.
