# Spring Boot 3 Security Architecture: JWT, Filter Chains, and OAuth2 Resource Server

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Spring Security ek **Multi-Tier Airport Border Security** ki tarah hai:
1. **SecurityFilterChain**: Har passenger ko alag-alag security counters se guzarna padta hai (Passport check, baggage scanner, metal detector).
2. **OncePerRequestFilter (JWT Check)**: Guard passenger ka wristband (JWT Token) scan karta hai, dekhta hai ki signature valid hai ya nahi, aur passenger ka verified identity badge (`SecurityContextHolder`) pehnata hai.
3. **Method Security (`@PreAuthorize`)**: VIP Lounge ke gate par ek aur guard khada hai jo sirf un logo ko andar jane deta hai jinke badge pe `ROLE_ADMIN` likha ho!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`SecurityFilterChain` Bean**: In Spring Boot 3 (Spring Security 6), `WebSecurityConfigurerAdapter` is deprecated. Security is configured declaratively via `@Bean SecurityFilterChain`.
2. **Session Creation Policy**: Set to `SessionCreationPolicy.STATELESS` for REST APIs to prevent server-side HTTP session storage.
3. **`OncePerRequestFilter`**: Guarantees execution exactly once per request dispatch, ideal for parsing `Authorization: Bearer <jwt>`.
4. **`SecurityContextHolder`**: Uses `ThreadLocal` storage by default to store the authenticated `Authentication` token for the duration of the thread.

---

## 💻 3. Line-by-Line Commented Code Snippets

```java
package com.knowledgebase.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableMethodSecurity // Enables @PreAuthorize("hasRole('ADMIN')")
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter) {
        this.jwtAuthFilter = jwtAuthFilter;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // Line 25: Disable CSRF since REST APIs use stateless JWT tokens
            .csrf(csrf -> csrf.disable())
            // Line 27: Enforce stateless session management
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // Line 29: Configure URL authorization rules
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**", "/actuator/health").permitAll()
                .anyRequest().authenticated()
            )
            // Line 34: Inject custom JWT filter BEFORE standard username/password filter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```
