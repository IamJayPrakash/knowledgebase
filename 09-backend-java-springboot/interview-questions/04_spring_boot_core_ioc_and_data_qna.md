# Java 21 & Spring Boot Master Interview Bank: Part 4 (Q61 - Q80)
## Spring Boot Core, IoC Container, AOP & Spring Data JPA

---

### Q61: Diagram and explain the Spring Bean Lifecycle from start to finish.
**Answer:**

```
[ 1. Instantiate ] ──► JVM allocates raw object (Constructor invoked)
         │
         ▼
[ 2. Populate Properties ] ──► Spring injects dependencies (@Autowired / setters)
         │
         ▼
[ 3. Aware Interfaces ] ──► BeanNameAware, BeanFactoryAware, ApplicationContextAware
         │
         ▼
[ 4. BeanPostProcessor.postProcessBeforeInitialization() ] ──► Custom initialization hooks
         │
         ▼
[ 5. Initialization Callbacks ] ──► @PostConstruct ──► InitializingBean.afterPropertiesSet() ──► custom initMethod
         │
         ▼
[ 6. BeanPostProcessor.postProcessAfterInitialization() ] ──► AOP Dynamic Proxy wrapping (CGLIB / JDK Proxy)
         │
         ▼
[ 7. Bean Ready for Use in Application ]
         │
         ▼ (ApplicationContext.close())
[ 8. Destruction Callbacks ] ──► @PreDestroy ──► DisposableBean.destroy() ──► custom destroyMethod
```

---

### Q62: Why is Field Injection (`@Autowired` on fields) considered an architectural anti-pattern?
**Answer:**
1. **Violates Encapsulation:** Fields cannot be `final`, allowing accidental mutation.
2. **Impedes Unit Testing:** To unit test the class, you cannot pass mock objects via constructor; you are forced to use reflection (`ReflectionTestUtils`) or launch a heavyweight Spring context.
3. **Hidden Dependencies:** With constructor injection, having 10 constructor arguments immediately warns you that the class violates the Single Responsibility Principle (SRP). Field injection hides this code smell.
4. **Circular Dependency Masking:** Constructor injection detects circular dependencies at startup; field injection can lead to runtime NullPointerExceptions.
- **Industry Standard:** **Constructor Injection** (or `@RequiredArgsConstructor` via Lombok).

---

### Q63: What are the Spring Bean Scopes and what happens when you inject a Prototype bean into a Singleton bean?
**Answer:**
- **Standard Scopes:** `singleton` (default, 1 instance per IoC container), `prototype` (new instance every time requested), `request` (HTTP request lifecycle), `session` (HTTP session), `application`.
- **The Prototype into Singleton Issue:**
  Because the Singleton bean is initialized **only once at startup**, its dependencies are injected only once.
  The injected Prototype bean remains the **same single instance forever**, never re-instantiating on subsequent calls!
- **Solutions:**
  1. Use **`@Lookup` method injection**.
  2. Inject `ObjectProvider<MyPrototypeBean>` or `ApplicationContext`.
  3. Use scoped proxy: `@Scope(value = "prototype", proxyMode = ScopedProxyMode.TARGET_CLASS)`.

---

### Q64: How does Spring Boot Auto-Configuration work under the hood?
**Answer:**
1. `@SpringBootApplication` includes **`@EnableAutoConfiguration`**.
2. At startup, Spring Boot inspects:
   `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (in Spring Boot 3+).
3. Reads hundreds of pre-configured AutoConfiguration classes (e.g. `DataSourceAutoConfiguration`).
4. Evaluates conditional annotations:
   - **`@ConditionalOnClass(DataSource.class)`**: Only loads if database driver JAR is present on classpath.
   - **`@ConditionalOnMissingBean(DataSource.class)`**: Only creates default data source if the developer has NOT already declared a custom `@Bean DataSource`.
   - **`@ConditionalOnProperty("app.feature.enabled")`**: Checks application properties.

---

### Q65: What is Spring AOP and how do JDK Dynamic Proxies differ from CGLIB Proxies?
**Answer:**
Spring Aspect-Oriented Programming (AOP) wraps beans with runtime proxies to intercept method calls (used for `@Transactional`, `@Async`, Security, and Logging):
- **JDK Dynamic Proxy:**
  - Built into native Java (`java.lang.reflect.Proxy`).
  - Can only proxy classes that **implement at least one interface**.
- **CGLIB Proxy:**
  - Uses bytecode manipulation to generate a dynamic subclass of the target class at runtime.
  - Can proxy concrete classes without interfaces. Cannot proxy `final` classes or `final` methods.
- **Spring Boot Default:** In Spring Boot 2.x and 3.x, **CGLIB is enabled by default** (`spring.aop.proxy-target-class=true`).

---

### Q66: Why does `@Transactional` self-invocation fail in Spring?
**Answer:**
```java
@Service
public class OrderService {
    public void processOrder() {
        // Self-invocation of transactional method:
        this.saveOrder(); // ❌ TRANSACTION IS COMPLETELY IGNORED!
    }

    @Transactional
    public void saveOrder() {
        // DB operations...
    }
}
```
**Why it fails:**
Spring `@Transactional` works via **AOP Proxies**. The transaction interceptor is in the outer proxy wrapper.
When `processOrder()` calls `this.saveOrder()`, it calls the method directly on the internal target object instance, **bypassing the proxy wrapper completely**.
- **Fixes:**
  1. Move `saveOrder()` to a separate `@Service` bean and inject it.
  2. Inject `OrderService` into itself (self-injection) and call `self.saveOrder()`.
  3. Programmatic transaction via `TransactionTemplate`.

---

### Q67: Explain `@Transactional` Propagation Types: `REQUIRED` vs `REQUIRES_NEW` vs `NESTED`.
**Answer:**
- **`REQUIRED` (Default):** Supports the current transaction; creates a new one if none exists. If an inner method fails, the entire outer transaction is rolled back.
- **`REQUIRES_NEW`:** Suspends the current transaction and creates a completely independent new transaction with its own database connection. The inner transaction commits or rolls back independently of the outer transaction.
  - *Use Case:* Audit logging (audit log must be committed even if the main purchase transaction fails and rolls back).
- **`NESTED`:** Executes within a nested transaction using database **Savepoints**. If the nested transaction fails, it rolls back to the savepoint without rolling back the parent transaction.

---

### Q68: What are the Default Rollback Rules of `@Transactional`?
**Answer:**
By default, Spring `@Transactional` rolls back transactions ONLY for **Unchecked Exceptions (`RuntimeException` and `Error`)**.
- If a method throws a **Checked Exception (`IOException`, `SQLException`)**, the transaction **COMMITS ANYWAY**!
- **Fix:** Always specify `rollbackFor = Exception.class`:
  ```java
  @Transactional(rollbackFor = Exception.class)
  public void transferFunds() throws BankException { ... }
  ```

---

### Q69: What is Hibernate First-Level Cache vs Second-Level Cache in Spring Data JPA?
**Answer:**
- **First-Level Cache (Session / EntityManager Cache):**
  - Enabled by default; cannot be disabled.
  - Scoped to the active **Persistence Context / Transaction**.
  - If you query `userRepository.findById(1L)` 3 times inside the same `@Transactional` method, Hibernate executes SQL once and returns the cached entity from memory for the other two queries.
- **Second-Level Cache (L2 Cache):**
  - Scoped to the entire **EntityManagerFactory / Application**.
  - Shared across all sessions and transactions. Requires external caching provider (e.g. Ehcache, Hazelcast, Redis).

---

### Q70: How does Hibernate Dirty Checking work?
**Answer:**
- When an entity is loaded into the Persistence Context, Hibernate creates a **snapshot copy of the entity's state**.
- When the transaction is about to commit, Hibernate performs **Dirty Checking**: it compares the current state of the entity against the original snapshot.
- If any fields have changed, Hibernate automatically generates and executes an `UPDATE` SQL statement before commit.
- **You do NOT need to call `repository.save(entity)`** inside a `@Transactional` method to persist changes to managed entities!

---

### Q71: How do you solve the JPA N+1 Query Problem?
**Answer:**
Occurs when querying an entity with a `@OneToMany` or `@ManyToOne` relationship, resulting in 1 query for parents + $N$ queries for children:
- **Solution 1: `JOIN FETCH` in JPQL**
  ```java
  @Query("SELECT u FROM User u JOIN FETCH u.orders")
  List<User> findAllUsersWithOrders();
  ```
- **Solution 2: `@EntityGraph` (Cleanest)**
  ```java
  @EntityGraph(attributePaths = {"orders"})
  List<User> findAll();
  ```
- **Solution 3: `@BatchSize(size = 50)`**: Groups queries using SQL `WHERE parent_id IN (...)`.

---

### Q72: What is the difference between `FetchType.LAZY` and `FetchType.EAGER`?
**Answer:**
- **`EAGER`:** Fetches the related entity immediately in the same initial query (often via SQL JOIN).
  - *Risk:* Massively degrades performance by loading entire database graphs unintentionally.
- **`LAZY` (Best Practice):** Loads the related entity on-demand only when its getter is explicitly called (`user.getOrders()`).
  - *Mechanism:* Hibernate injects a **Byte Buddy dynamic proxy** in place of the relation. When accessed, the proxy queries the database.
  - *Risk:* Throws `LazyInitializationException` if accessed outside an active transaction after the session has closed.

---

### Q73: What is `LazyInitializationException` and how do you resolve it cleanly?
**Answer:**
- **Cause:** Occurs when code tries to access a lazy-loaded relationship after the Hibernate `Session` / `EntityManager` has closed (typically in a controller or Jackson JSON serializer outside `@Transactional`).
- **Clean Solutions:**
  1. Fetch necessary associations eagerly inside the service layer using `@EntityGraph` or `JOIN FETCH`.
  2. Map entities to immutable **DTO records** inside the service layer before returning to controllers.
  - *Anti-Pattern to Avoid:* Enabling `spring.jpa.open-in-view=true` (keeps database connections open until the view renders, starving database connection pools).

---

### Q74: What is Optimistic Locking vs Pessimistic Locking in JPA?
**Answer:**
- **Optimistic Locking (`@Version`):**
  - Adds a version column (`@Version private Long version;`).
  - When updating, Hibernate appends: `WHERE id = ? AND version = 5`.
  - If another transaction modified the row concurrently, 0 rows are updated and Hibernate throws **`OptimisticLockException`**.
  - High performance; ideal for read-heavy systems with low collision probability.
- **Pessimistic Locking (`@Lock(LockModeType.PESSIMISTIC_WRITE)`):**
  - Translates to SQL `SELECT ... FOR UPDATE`.
  - Locks the database row at the database engine level until transaction commit.
  - Eliminates collisions, but degrades concurrency. Ideal for financial balance updates.

---

### Q75: What is Spring Data JPA Auditing (`@CreatedDate`, `@LastModifiedBy`)?
**Answer:**
- Automatically populates audit metadata on entity persistence:
  - `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy`.
- Enabled via **`@EnableJpaAuditing`** and creating an `AuditorAware<String>` bean that extracts the authenticated username from `SecurityContextHolder`.

---

### Q76: What is the difference between `BeanFactory` and `ApplicationContext`?
**Answer:**
- **`BeanFactory`:** The root interface for the Spring IoC container. Provides basic dependency injection and lazy initialization (beans are instantiated only when requested).
- **`ApplicationContext`:** A complete superset of `BeanFactory`. Adds enterprise features:
  1. **Eager Pre-instantiation** of singleton beans at startup (detects configuration errors early).
  2. Integrated Event publication (`ApplicationEventPublisher`).
  3. Internationalization / i18n message resolution.
  4. Environment profiles and AOP integration.

---

### Q77: How does `@Async` work in Spring Boot and why must you configure a custom `TaskExecutor`?
**Answer:**
- `@Async` runs a method in a separate background worker thread.
- **Default Danger:** By default, Spring uses `SimpleAsyncTaskExecutor`, which **does NOT pool threads**—it creates a brand-new OS thread for every single `@Async` call, leading to memory exhaustion under load.
- **Production Standard:** Always declare a custom `ThreadPoolTaskExecutor` bean configuring `corePoolSize`, `maxPoolSize`, and `queueCapacity`.

---

### Q78: What is the difference between `@Controller` and `@RestController`?
**Answer:**
- **`@Controller`:** Standard Spring MVC controller. Handler methods return a String representing a template view name (JSP/Thymeleaf) resolved by a `ViewResolver`.
- **`@RestController`:** Convenience annotation combining **`@Controller` + `@ResponseBody`**. Methods serialize returned Java objects directly into JSON or XML HTTP response bodies using Jackson `HttpMessageConverter`.

---

### Q79: How does Jackson serialize and deserialize polymorphic classes in Spring Boot?
**Answer:**
Use Jackson polymorphic type annotations on the base class:
```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = CreditCardPayment.class, name = "CREDIT_CARD"),
    @JsonSubTypes.Type(value = CryptoPayment.class, name = "CRYPTO")
})
public abstract class PaymentDto {}
```

---

### Q80: What is Spring Boot Actuator and why is it vital for production?
**Answer:**
- Exposes production-ready operational HTTP endpoints to monitor and manage applications:
  - `/actuator/health`: Liveness and readiness probes for Kubernetes.
  - `/actuator/metrics`: JVM memory, GC pauses, CPU, and thread count metrics (consumed by Prometheus).
  - `/actuator/info`: Git commit hash, build version.
  - `/actuator/loggers`: View and **dynamically change logging levels in real-time without restarting**!
