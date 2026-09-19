# DevOps & Cloud-Native: Docker, Kubernetes, and CI/CD (Q26 - Q50)

> A master question bank covering production containerization, Kubernetes cluster architecture, Helm, GitOps, zero-downtime deployments, and SRE incident response for Senior DevOps & Platform Engineers.

---

### Q26: How do Linux Namespaces, cgroups, and UnionFS form the core of Docker Containers?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:** Container koi alag virtual computer (VM) nahi hota, ye host operating system par chalne wala ek normal Linux process hi hota hai. Usko teen cheezon se baandh diya jata hai:
  1. **Namespaces:** Process ki aankhon par patti baandhna taaki usko lage wo akela hai (process, network, file isolation).
  2. **cgroups:** Process ke resources par limit lagana (zyada se zyada 2GB RAM, 1 CPU).
  3. **UnionFS:** Alag-alag file layers ko ek transparent glass ki tarah jodkar ek single filesystem dikhana.
- **Real-World Analogy:** Renting a private cubicle in a co-working office: you have your own private desk and phone line (Namespaces), an electricity usage quota (cgroups), and access to a shared library of company books (UnionFS).

#### 2. Core Mechanics & Key Points

- **Namespaces (Isolation Boundary):**
  - `pid`: Process ID isolation (container process sees itself as PID 1).
  - `net`: Network isolation (own IP, loopback, routing table, port bindings).
  - `mnt`: Mount points and filesystem isolation.
  - `ipc`: Inter-process communication isolation.
  - `uts`: Hostname isolation.
  - `user`: User and group ID mapping.
- **cgroups (Resource Controls):** Enforces hard limits and accounting on CPU shares, memory allocation, block I/O, and pids.
- **UnionFS / OverlayFS (Storage Layering):** Layered file system combining read-only image layers into a unified view with a single thin read-write container layer on top (Copy-on-Write).

#### 3. Visual Architecture Diagram

```
  +-----------------------------------------------------------+
  |                   Container Process (PID 1)               |
  +-----------------------------------------------------------+
         |                        |                       |
         v                        v                       v
  [ Namespaces ]             [ cgroups ]             [ OverlayFS ]
  (PID, NET, MNT, IPC)      (Limit: 2GB, 1 CPU)     (Layered COW Storage)
         \                        |                       /
          +-----------------------+----------------------+
                                  v
                       [ Shared Linux Kernel ]
```

#### 5. Senior Interview Answering Pitch
>
> "Containers are not hypervisor-virtualized machines; they are standard Linux processes isolated by kernel primitives. Namespaces provide the illusion of dedicated system resources like PID tables, network interfaces, and mount trees. Control Groups (cgroups) meter and restrict physical resources like CPU and RAM. OverlayFS merges stacked, immutable image layers using Copy-on-Write."

---

### Q27: How do Docker Multi-Stage Builds minimize image size and improve security?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:** Ek cake banane ke liye kitchen me aata, ande, mixer aur oven ki zaroorat hoti hai. Lekin customer ko sirf finished baked cake serve kiya jata hai, pura mixer aur kachra customer ke plate me nahi diya jata! Multi-stage builds me build tools (Node.js SDK, compilers, devDependencies) builder stage me rehte hain, aur final runtime container me sirf compiled binary copy hoti hai.
- **Real-World Analogy:** A sculpture workshop: heavy chisels, hammers, and stone dust remain in the quarry; only the finished polished marble statue is delivered to the museum.

#### 2. Practical Implementation & Code Snippet

```dockerfile
# Stage 1: Build & Compilation (Contains heavy toolchain)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 2: Minimal Production Runtime (Ultra-secure & lightweight)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Security: Run as dedicated non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copy ONLY production artifacts from builder stage
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

EXPOSE 8080
CMD ["node", "dist/server.js"]
```

#### 5. Senior Interview Answering Pitch
>
> "Multi-stage builds decouple the build environment from the execution environment. Heavy compilers, package managers, and secret keys remain in intermediate ephemeral layers. The final stage copies only the built artifacts into a minimal, non-root base image, drastically reducing image size from gigabytes to megabytes and drastically shrinking the CVE attack surface."

---

### Q28: What is the difference between Kubernetes Liveness, Readiness, and Startup Probes?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:**
  - **Startup Probe:** "Kya app boot ho chuka hai?" (Initial initialization ke dauran liveness ko roke rakhta hai).
  - **Readiness Probe:** "Kya app abhi traffic lene ke liye tayar hai?" (Agar fail ho, toh Service se Pod ka IP hata do taaki user ko error na mile).
  - **Liveness Probe:** "Kya app zinda hai ya deadlock me phasa hai?" (Agar fail ho, toh Pod ko kill karke restart kar do).
- **Real-World Analogy:** A restaurant chef: Startup is getting dressed and lighting the ovens; Readiness is having enough prepared ingredients to take customer orders; Liveness is checking that the chef hasn't passed out from heat exhaustion.

#### 2. Probe Comparison Matrix

| Probe Type | What it Detects | Failure Action | Prevents |
| :--- | :--- | :--- | :--- |
| **Startup** | Slow application initialization | Kills container and restarts | Premature liveness kills on slow boots |
| **Readiness** | Overloaded or unready container | **Removes Pod from Service Endpoints** (No restart) | 502/503 errors during cold start or database reconnects |
| **Liveness** | Deadlocks, infinite loops, unrecoverable crashes | **Kills container and restarts** | Zombie pods permanently consuming memory |

#### 3. Practical Implementation & Code Snippet

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    spec:
      containers:
        - name: web
          image: company/api:v1.0.0
          # 1. Startup Probe: gives app up to 60s to boot
          startupProbe:
            httpGet:
              path: /healthz/startup
              port: 8080
            failureThreshold: 30
            periodSeconds: 2
          # 2. Readiness Probe: routes traffic only when DB is connected
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: 8080
            periodSeconds: 5
            failureThreshold: 2
          # 3. Liveness Probe: detects deadlocks
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
```

#### 5. Senior Interview Answering Pitch
>
> "Startup probes protect slow-initializing containers from premature termination. Readiness probes control traffic ingestion—if an application is warming its cache or reconnecting to a database, readiness failures remove it from the Service endpoints without restarting it. Liveness probes detect deadlocks, restarting containers that have entered an unrecoverable state."

---

### Q29: What are the differences between Kubernetes Service Types: `ClusterIP`, `NodePort`, `LoadBalancer`, and `ExternalName`?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:**
  - `ClusterIP`: Sirf cluster ke andar baat karne ke liye internal private IP (default).
  - `NodePort`: Har worker node ke ek specific port (30000-32767) par service expose karna.
  - `LoadBalancer`: Cloud provider (AWS/GCP) se ek real public IP address mangwana jo traffic baante.
  - `ExternalName`: Internal DNS CNAME bana kar kisi bahar ke domain (jaise AWS RDS) par redirect karna.
- **Real-World Analogy:** ClusterIP is an internal intercom; NodePort is dialing a specific building extension; LoadBalancer is a central corporate receptionist; ExternalName is an auto-forward to an external consulting firm.

#### 2. Architecture Comparison Diagram

```
  [ Internet Traffic ]
          |
  [ Cloud LoadBalancer Service ] (Public IP: 35.200.1.2)
          |
  [ Ingress Controller / NodePort ] (Port 31250 on all Nodes)
          |
  [ ClusterIP Service ] (Internal Virtual IP: 10.96.0.10)
     /         |         \
  [ Pod 1 ] [ Pod 2 ] [ Pod 3 ]
```

#### 5. Senior Interview Answering Pitch
>
> "`ClusterIP` provides an internal-only virtual IP for east-west cluster communication. `NodePort` exposes an open static port across all worker nodes for direct host access. `LoadBalancer` integrates with cloud APIs to provision external network load balancers. In enterprise production, we typically expose one cloud LoadBalancer attached to an Ingress Controller, which routes traffic to internal `ClusterIP` services via L7 host/path rules."

---

### Q30: How does the Kubernetes Horizontal Pod Autoscaler (HPA) compute scaling decisions?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:** HPA har 15 second me check karta hai ki pods par kitna load hai. Formula simple hai: `DesiredReplicas = ceil(CurrentReplicas * (CurrentMetric / TargetMetric))`. Agar 2 pods hain aur target 50% CPU tha, par actual CPU 100% ho gaya, toh `ceil(2 * (100 / 50)) = 4` pods ho jayenge!
- **Real-World Analogy:** A highway toll booth supervisor: if the line at each booth exceeds 5 cars, open more booths immediately according to the traffic ratio.

#### 2. Mathematical Formula & Scaling Algorithm

$$\text{Desired Replicas} = \left\lceil \text{Current Replicas} \times \left( \frac{\text{Current Metric Value}}{\text{Target Metric Value}} \right) \right\rceil$$

#### 3. Practical Implementation & Code Snippet

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 30
  metrics:
    # 1. Resource metric (CPU utilization)
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    # 2. Custom Prometheus metric (HTTP requests per second)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 1000m
  behavior:
    # Scale-down stabilization window to prevent "thrashing" / flapping
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

#### 5. Senior Interview Answering Pitch
>
> "The HPA polls metrics via the Metrics Server or Custom Metrics API every 15 seconds. It calculates desired replicas using the ratio of current metric value to target value. In production, we configure stabilization windows in the `behavior` field to prevent rapid scale flapping and pair CPU/memory metrics with custom application signals like active queue depth or requests per second."

---

### Q31: What is GitOps and how does ArgoCD enforce Declarative Infrastructure Reconciliation?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:** Pehle log terminal khol kar `kubectl apply` chalate the, jisse koi audit trail nahi rehta tha aur cluster me drift aa jata tha. GitOps me Git repository hi "Single Source of Truth" hoti hai. ArgoCD cluster ke andar baithta hai aur Git repo ko monitor karta hai: agar kisi ne live cluster me manual change kiya ya Git me naya commit aaya, toh ArgoCD cluster ko automatically sync karke Git ke mutabik bana deta hai!
- **Real-World Analogy:** A thermostat: you set the target temperature to 72°F on the wall (Git commit). The AC system (ArgoCD) continuously measures the room and adjusts cooling until the reality matches the target setting.

#### 2. Visual Architecture Diagram

```
  Developer Git Push ---> [ GitHub Main Branch ] (Desired State)
                                 |
                          ArgoCD Polls / Webhook
                                 |
                                 v
                     [ ArgoCD Controller ]
                                 |
                     Reconciliation Loop (Compare)
                                 |
                         Does Live == Git?
                        /                 \
                 (YES) v                   v (NO - Out of Sync)
              [ Healthy ]            [ Self-Heal / Auto-Sync ]
                                           |
                                 Kubernetes API Server
```

#### 5. Senior Interview Answering Pitch
>
> "GitOps establishes Git repositories as the single source of truth for declared infrastructure and application manifests. ArgoCD continuously runs an automated reconciliation loop inside the cluster, comparing the desired Git state against the live state. It provides automated drift detection, automated self-healing, cryptographic commit verification, and instant zero-risk rollbacks via `git revert`."

---

### Q32: Compare Zero-Downtime Deployment Strategies: Rolling Updates vs Blue-Green vs Canary

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:**
  - **Rolling Update:** Ek-ek karke purane pod ko delete karo aur naya pod start karo (sasta, default).
  - **Blue-Green:** Ek pura naya identical cluster khada karo (Green). Jab tests pass ho jayein, toh load balancer ka router switch ghuma do (Instant switch, expensive).
  - **Canary:** Naye version ko sirf 5% users ko dikhao (canary bird). Agar error rate badhe toh turant band karo, agar normal rahe toh dheere-dheere 100% kar do.
- **Real-World Analogy:** Miners sending a canary bird into the coal mine to test air toxicity before human workers enter.

#### 2. Strategy Decision Matrix

| Strategy | Resource Cost | Rollback Speed | Blast Radius | Implementation Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Rolling Update** | 100% + `maxSurge` (Low) | Slow (Must re-roll) | Medium (All users hit both versions) | Simple (Built into K8s) |
| **Blue-Green** | 200% (High - 2x fleet) | **Instant** (Flip router) | Zero (Tested before traffic flip) | Medium (Argo Rollouts) |
| **Canary** | 100% + ~10% (Low) | Fast (Scale down Canary) | **Minimal** (Only 1-5% of traffic affected) | High (Service Mesh / Flagger) |

#### 5. Senior Interview Answering Pitch
>
> "Rolling updates are cost-effective but expose the entire user base to gradual failures. Blue-Green offers instantaneous cutover and zero-downtime rollbacks by maintaining twin production environments at double infrastructure cost. For mission-critical systems, Canary deployments using Argo Rollouts or Istio are preferred: routing a fractional percentage of traffic to the new revision while analyzing automated Prometheus error metrics to trigger automatic rollbacks."

---

### Q33: How do you troubleshoot a Pod stuck in `CrashLoopBackOff` or `OOMKilled`?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:**
  - `CrashLoopBackOff`: Pod start hota hai, crash ho jata hai, Kubernetes usko bar-bar restart karta hai aur har bar wait time (backoff) badhata jata hai.
  - `OOMKilled`: Pod ne apni cgroup memory limit (jaise 512MB) cross kar di, toh Linux kernel ne `SIGKILL` bhej kar process ko turant khatam kar diya.
- **Real-World Analogy:** A car stalling because of no fuel (`CrashLoopBackOff` - misconfigured env/DB) vs the engine seizing because it exceeded maximum allowable temperature (`OOMKilled`).

#### 2. Systematic 5-Step SRE Diagnostic Procedure

1. **Inspect Pod Exit Code & Reason:**

   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   # Look at: Last State -> Reason: OOMKilled or Error, Exit Code: 137 (OOM) or 1
   ```

2. **Fetch Logs from the CRASHED Container:**

   ```bash
   kubectl logs <pod-name> --previous -n <namespace>
   # The '--previous' flag reads logs from the crashed container before restart!
   ```

3. **Verify ConfigMaps & Environment Secrets:**
   Check if missing database passwords or misconfigured URLs caused application boot panic.
4. **Check cgroup Memory Limits:**
   If Exit Code is `137`, verify whether JVM heap `-Xmx` or Node.js `--max-old-space-size` exceeds Kubernetes container `resources.limits.memory`.
5. **Debug Interactively with an Ephemeral Container:**

   ```bash
   kubectl debug -it <pod-name> --image=busybox --target=<container-name>
   ```

#### 5. Senior Interview Answering Pitch
>
> "To resolve `CrashLoopBackOff`, I first execute `kubectl describe pod` to inspect termination reasons and exit codes. Exit code 137 signals an `OOMKilled` event where process memory exceeded cgroup limits, requiring heap tuning or limit adjustments. For exit code 1 or 2, I inspect `kubectl logs --previous` to analyze stack traces prior to termination, typically discovering database connection timeouts or missing secret mounts."

---

### Q34: How do SREs use SLIs, SLOs, and Error Budgets to balance feature velocity with reliability?

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:**
  - **SLI:** Meter ki reading (e.g., 99.92% requests successful the).
  - **SLO:** Hamara internal target (e.g., 99.9% success hona chahiye).
  - **SLA:** Customer ke sath legal contract (e.g., agar 99.5% se niche gaya toh refund dena padega).
  - **Error Budget:** `100% - SLO`. Wo paisa jisko aap feature launch aur experiments me risk le sakte ho. Agar budget khatam ho gaya, toh sare naye features freeze aur sirf bug-fixes!
- **Real-World Analogy:** A monthly spending allowance: as long as you stay within budget, you can spend on entertainment (new features). If you overspend, all entertainment stops until the account recovers.

#### 2. Core Equations

$$\text{SLO} = 99.9\% \quad \implies \quad \text{Error Budget} = 0.1\% \text{ allowable failures}$$
$$\text{In a 30-day month: } 0.1\% \times 30 \times 24 \times 60 \text{ minutes} = 43.2 \text{ minutes allowable downtime}$$

#### 5. Senior Interview Answering Pitch
>
> "Service Level Indicators (SLIs) measure real-time platform health (e.g., p99 latency < 200ms). Service Level Objectives (SLOs) represent internal target reliability goals agreed with product teams. The Error Budget (`1 - SLO`) provides a mathematical contract: while budget remains, engineering teams ship features rapidly. When the error budget is exhausted, deployments freeze and all sprint resources pivot to reliability, testing, and technical debt reduction."

---

### Q35: Production War Story: Diagnosing and Mitigating an Ingress Controller Cascading Failure during a Cyber Monday Traffic Spike

#### 1. Layman's Analogy (Hinglish + Real-World)

- **Hinglish Intuition:** Cyber Monday ke din 100,000 customers ek sath aaye. NGINX Ingress Controller pods par itne connections khul gaye ki unka worker connection limit khatam ho gaya. Ek pod crash hua, baki bache hue pods par aur zyada load aa gaya, aur wo ek ke baad ek dominos ki tarah crash ho gaye (Cascading failure). Humne HPA tune kiya aur rate-limiting lagayi.
- **Real-World Analogy:** A bridge collapsing under traffic: when one lane gives out, all remaining cars pile into the remaining lanes, overloading them until the entire bridge fails.

#### 2. STAR Incident Breakdown

- **Situation:** During peak Cyber Monday checkout traffic (80,000 RPS), the ingress layer collapsed, yielding 502/504 gateway errors across all microservices for 12 minutes.
- **Task:** Halt the cascading failure, restore ingress routing immediately, and prevent recurrence.
- **Action:**
  1. Identified that NGINX ingress pods were bottlenecked on file descriptors (`worker_connections: 1024` default) and memory leaks during SSL renegotiation, causing worker OOMKills.
  2. Increased Ingress Replica count immediately from 4 to 24 pods using `kubectl scale`.
  3. Tuned NGINX configuration via ConfigMap: raised `worker-connections` to `65535`, enabled HTTP/2 multiplexing, and configured keepalive connections to upstream backends.
  4. Deployed Cloudflare Edge Rate Limiting to drop bot scraper floods at the CDN boundary before reaching Kubernetes.
- **Result:**
  - Cluster recovered within 3 minutes of re-scaling.
  - Handled sustained 95,000 RPS without dropping a single payment transaction.
  - Implemented an automated Ingress HPA based on active TCP connections.
