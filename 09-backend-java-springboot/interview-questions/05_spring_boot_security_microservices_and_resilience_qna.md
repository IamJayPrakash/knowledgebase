# Java 21 & Spring Boot Master Interview Bank: Part 5 (Q81 - Q100)
## Spring Security 6, Microservices, Resilience4j & Production Ops

---

### Q81: Diagram and explain the Spring Security 6 Filter Chain architecture.
**Answer:**

```
HTTP Request
     │
     ▼
[ DelegatingFilterProxy ] ──► Bridges standard Servlet Container (Tomcat) to Spring Context
     │
     ▼
[ FilterChainProxy ] ──► Manages SecurityFilterChain instances
     │
     ▼
[ SecurityFilterChain (Ordered List of Security Filters) ]
  ├── 1. CorsFilter
  ├── 2. CsrfFilter
  ├── 3. HeaderWriterFilter
  ├── 4. LogoutFilter
  ├── 5. JwtAuthenticationFilter (Custom filter extracting Bearer token)
  ├── 6. UsernamePasswordAuthenticationFilter
  ├── 7. SecurityContextHolderAwareRequestFilter
  ├── 8. AnonymousAuthenticationFilter
  ├── 9. ExceptionTranslationFilter (Catches AccessDeniedException / AuthenticationException)
  └── 10. AuthorizationFilter (Enforces URL path request matchers & roles)
     │
     ▼
[ DispatcherServlet ] ──► RestController
```

---

### Q82: How do you configure a modern, stateless `SecurityFilterChain` in Spring Security 6?
**Answer:**
`WebSecurityConfigurerAdapter` is completely removed in Spring Security 6. You declare a `@Bean SecurityFilterChain`:

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http, JwtAuthFilter jwtAuthFilter) throws Exception {
        return http
            .csrf(csrf -> csrf.disable()) // Disabled for stateless REST APIs
            .cors(Customizer.withDefaults())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**", "/actuator/health").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

---

### Q83: Why is CSRF (Cross-Site Request Forgery) protection disabled in Stateless REST APIs?
**Answer:**
- **How CSRF Works:** An attacker tricks a victim's browser into submitting an unauthorized request to a trusted site where the victim is logged in via **automatic browser session cookies**.
- **Stateless REST APIs with JWT:**
  - Modern REST APIs do not use browser session cookies; clients pass a JSON Web Token (JWT) in the **`Authorization: Bearer <token>` HTTP header**.
  - Browsers **NEVER automatically send headers across cross-origin requests**.
  - Because an attacker site cannot force the browser to attach the custom `Authorization` header, CSRF attacks are fundamentally impossible, making CSRF tokens redundant.

---

### Q84: How do you implement Method-Level Security with `@PreAuthorize`?
**Answer:**
Enabled via `@EnableMethodSecurity` on a configuration class:
- Uses SpEL (Spring Expression Language) to evaluate permissions before method execution:

```java
@Service
public class DocumentService {

    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    public Document getDocument(Long docId, Long userId) {
        return documentRepository.findById(docId).orElseThrow();
    }
}
```

---

### Q85: How does Spring Boot 3.2+ natively support Java 21 Virtual Threads?
**Answer:**
In Spring Boot 3.2+ running on Java 21:
- Add a single property to `application.properties`:
  ```properties
  spring.threads.virtual.enabled=true
  ```
- **What this does:**
  1. **Tomcat Web Server:** Automatically configures embedded Tomcat to dispatch **every incoming HTTP request onto a new Virtual Thread** instead of using a fixed thread pool of 200 platform threads!
  2. **`@Async` and TaskExecutors:** Automatically sets `applicationTaskExecutor` to use `Executors.newVirtualThreadPerTaskExecutor()`.
  3. **Performance:** Supports 100,000+ concurrent blocking requests with minimal RAM footprint and near-zero context-switching cost.

---

### Q86: How does Resilience4j CircuitBreaker integrate with Spring Boot?
**Answer:**
1. Add dependency: `org.springframework.cloud:spring-cloud-starter-circuitbreaker-resilience4j`.
2. Annotate methods with `@CircuitBreaker` and provide a fallback method:

```java
@Service
public class PaymentGatewayClient {

    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    public PaymentResponse charge(PaymentRequest request) {
        return restTemplate.postForObject("https://external-bank.com/api", request, PaymentResponse.class);
    }

    // Fallback signature MUST match original parameters + Throwable
    public PaymentResponse paymentFallback(PaymentRequest request, Throwable ex) {
        log.warn("Bank gateway is down! Routing to offline queue. Error: {}", ex.getMessage());
        return new PaymentResponse("QUEUED_FOR_RETRY", request.getId());
    }
}
```

---

### Q87: What is Spring Cloud Gateway and why is it built on Project Reactor / Netty?
**Answer:**
- Legacy Spring Cloud Zuul 1.x was built on blocking Servlet threads (1 thread per connection), causing connection pool starvation during slow downstream outages.
- **Spring Cloud Gateway:**
  - Built on **Spring WebFlux, Project Reactor, and Netty**.
  - Non-blocking, event-driven reactive architecture.
  - A small pool of worker event-loop threads (e.g. 8 threads) can handle 50,000+ open connections.
  - Features: Path routing, rate limiting via Redis, token validation, dynamic load balancing with Eureka.

---

### Q88: How do you achieve Kafka Consumer Idempotency in Spring Boot?
**Answer:**
```java
@Component
public class OrderKafkaListener {

    @Autowired
    private ProcessedEventRepository eventRepo;

    @KafkaListener(topics = "orders-topic", groupId = "order-group")
    @Transactional
    public void handleOrderEvent(@Payload OrderEvent event, Acknowledgment ack) {
        // Atomic DB insertion to check if event was already processed
        if (eventRepo.existsById(event.getEventId())) {
            log.info("Duplicate event detected: {}. Skipping.", event.getEventId());
            ack.acknowledge();
            return;
        }

        // Process business logic...
        eventRepo.save(new ProcessedEvent(event.getEventId(), Instant.now()));
        ack.acknowledge();
    }
}
```

---

### Q89: What is Distributed Tracing in Spring Boot 3 using Micrometer Tracing?
**Answer:**
- In Spring Boot 2, Spring Cloud Sleuth was used.
- In **Spring Boot 3**, Sleuth is replaced by **Micrometer Tracing** (supporting OpenTelemetry and Brave/Zipkin):
  - Automatically generates and propagates `traceId` (global for the entire workflow) and `spanId` (for individual service operations).
  - Injects `traceId` into Logback/MDC for unified logging:
    `[OrderService,4bf92f3577b34da6,00f067aa0ba902b7]`
  - Exports spans to Prometheus, Tempo, or Jaeger for latency waterfall graphs.

---

### Q90: What is the difference between Spring WebFlux (Reactive) and Virtual Threads (Spring MVC)?
**Answer:**
| Dimension | Spring WebFlux (Reactive Streams) | Spring MVC + Virtual Threads (Java 21) |
| :--- | :--- | :--- |
| **Programming Model** | **Functional / Reactive** (`Mono<T>`, `Flux<T>`). Complex learning curve. | **Imperative / Synchronous** (Standard sequential code). Simple to read and write. |
| **Debugging** | Difficult (stack traces lose contextual execution frames across event loops). | **Trivial** (standard linear stack traces, standard debugger breakpoints). |
| **Backpressure** | Native reactive backpressure protocol. | Natural OS socket / thread pool backpressure. |
| **Ecosystem Support** | Requires 100% reactive drivers (R2DBC instead of JDBC). | Works with all existing blocking enterprise libraries (JDBC, Hibernate). |

---

### Q91: How do you configure a Graceful Shutdown in Spring Boot?
**Answer:**
In `application.properties`:
```properties
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```
- When a `SIGTERM` signal arrives (from Kubernetes during pod termination):
  1. The embedded web server stops accepting **new requests**.
  2. Active in-flight requests are given up to **30 seconds** to complete normally.
  3. Database connection pools and message consumers are closed safely without dropping transactions.

---

### Q92: What is the role of `SecurityContextHolder` in Spring Security?
**Answer:**
- `SecurityContextHolder` is where Spring Security stores details of the currently authenticated principal (`SecurityContext`).
- **Storage Strategies:**
  - **`MODE_THREADLOCAL` (Default):** Stores security context in a `ThreadLocal` variable bound to the current thread.
  - **`MODE_INHERITABLETHREADLOCAL`:** Child threads spawned by the current thread inherit the security context.
  - **`MODE_GLOBAL`:** Single security context across JVM (for standalone desktop apps).

---

### Q93: How do you secure Actuator endpoints in Spring Boot?
**Answer:**
By default, sensitive Actuator endpoints should never be exposed publicly to the internet:
```properties
management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=when_authorized
```
Inside `SecurityFilterChain`:
```java
auth.requestMatchers("/actuator/health", "/actuator/info").permitAll()
    .requestMatchers("/actuator/**").hasRole("ADMIN")
```

---

### Q94: How does Spring Cloud Config enable centralized externalized configuration?
**Answer:**
- Centralized configuration server backed by Git or HashiCorp Vault.
- Microservices fetch configuration on startup based on their application name and active profile (`application-prod.yml`).
- **Dynamic Refresh:** Microservices annotate beans with **`@RefreshScope`**. Sending a POST request to `/actuator/refresh` reloads modified configurations from Git into the running bean without restarting the JVM!

---

### Q95: What is Spring Boot `@Profile` and how is it used in multi-stage deployments?
**Answer:**
- `@Profile("dev")`, `@Profile("prod")` segregates configuration beans and properties by environment.
- Activated via:
  `java -jar app.jar --spring.profiles.active=prod` or environment variable `SPRING_PROFILES_ACTIVE=prod`.

---

### Q96: How do you prevent SQL Injection in Spring Boot and JPA?
**Answer:**
1. **Use Parameterized Queries:** Spring Data JPA `@Query` with named parameters automatically uses JDBC `PreparedStatement` with bind variables:
   ```java
   @Query("SELECT u FROM User u WHERE u.email = :email")
   User findByEmail(@Param("email") String email);
   ```
2. **Never Concatenate Raw Strings in Native Queries:**
   `// ❌ VULNERABLE: em.createNativeQuery("SELECT * FROM users WHERE name = '" + name + "'");`

---

### Q97: What is Spring Session and how does it solve Distributed Session clustering?
**Answer:**
- In microservice architectures behind load balancers, storing user sessions in local Tomcat memory breaks if the next request hits a different server node.
- **Spring Session:** Transparently replaces `HttpSession` with a distributed backend store (**Redis** or Hazelcast).
- Session data is stored in Redis under a session ID cookie, allowing any microservice instance to read the user session seamlessly.

---

### Q98: What is the difference between `@Mock` and `@MockBean` in Spring Boot testing?
**Answer:**
- **`@Mock` (Mockito):** Pure unit testing. Creates a Mockito mock instance in memory without starting any Spring ApplicationContext (fast, lightweight).
- **`@MockBean` (Spring Boot Test):** Integration testing. Creates a mock and **injects it directly into the Spring ApplicationContext**, replacing any existing real bean of that type.

---

### Q99: What is Testcontainers and why is it preferred over H2 In-Memory DB?
**Answer:**
- **The H2 Flaw:** H2 in-memory DB has different SQL dialects, missing JSON/PostGIS features, and different locking behaviors than real PostgreSQL/MySQL, creating bugs that pass local tests but fail in production!
- **Testcontainers:** A Java library that automatically spins up real **Docker containers** (e.g. real PostgreSQL, real Redis, real Kafka) during unit/integration tests, guaranteeing 100% parity with production.

---

### Q100: How do you tune a Spring Boot Application for Extreme High-Throughput Production?
**Answer:**
1. **JVM Runtime:** Run on Java 21 with Generational ZGC (`-XX:+UseZGC -XX:+ZGenerational`).
2. **Virtual Threads:** Enable `spring.threads.virtual.enabled=true`.
3. **Database Connection Pool:** Size HikariCP accurately: `maximumPoolSize = (2 * CPU Cores) + Disk Spindle Count` (typically 20-30 connections, avoiding over-allocation).
4. **Disable Open-Session-In-View:** `spring.jpa.open-in-view=false`.
5. **Compression & HTTP/2:** Enable GZip compression (`server.compression.enabled=true`) and HTTP/2.
6. **Stateless Auth:** Eliminate server-side HTTP sessions; use stateless JWTs with Redis token revocation blacklists.
