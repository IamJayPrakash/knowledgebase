import os

BASE_DIR = r"D:\Projects\knowledgebase\04-frontend-frameworks\angular"

ANGULAR_21_GUIDES = [
    {
        "file": "01_angular21_signals_and_reactivity.md",
        "title": "Angular 21 Signals: Writable, Computed, Effects & Signal Inputs",
        "hinglish": "Angular 21 me Signals primary reactivity primitive hain. Pehle Angular pura component tree check karta tha change detection ke liye. Signals ke saath Angular ko exact pata hota hai ki DOM ka kaunsa chhota sa tukda update karna hai, jisse rendering ultra-fast ho jati hai.",
        "analogy": "A smart home electricity grid: instead of turning on every generator in the city to check if a lamp was switched on, Signals pinpoint the exact wire and bulb directly.",
        "points": [
            "Writable Signals (`signal(value)`): Direct reactive value wrappers with `.set()` and `.update()` methods.",
            "Computed Signals (`computed(() => ...)`): Derived reactive values that are lazily evaluated and memoized (only recalculate when dependencies change).",
            "Effects (`effect(() => ...)`): Side-effect runners that execute whenever tracked signals change (logging, canvas rendering, local storage sync).",
            "Signal Inputs & Outputs (`input()`, `output()`, `model()`): Modern signal-based component communication replacing legacy `@Input()` and `@Output()` decorators."
        ],
        "diagram": """[Signal Value Updated: count.set(5)]
                │
                ├── Automatically notifies [computed: totalPrice] (Recalculates lazily)
                │
                └── Surgical O(1) DOM Update on <span>{{ count() }}</span>
                    (Zero Component Tree Traversal! No Zone.js!)""",
        "code": """// Angular 21 Reactive Signal Component
import { Component, signal, computed, effect, input, model } from '@angular/core';

@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  template: `
    <div class="cart-card">
      <h2>Item: {{ itemName() }}</h2>
      <p>Unit Price: ${{ unitPrice() }}</p>
      
      <!-- Reading signal value with parenthesis syntax count() -->
      <p>Quantity: {{ quantity() }}</p>
      <p>Total Cost: ${{ totalCost() }}</p>

      <button (click)="incrementQuantity()">+ Add One</button>
      <button (click)="decrementQuantity()">- Remove One</button>
    </div>
  `
})
export class ShoppingCartComponent {
  // Line 1: Signal-based input property (replaces @Input)
  readonly itemName = input.required<string>();
  readonly unitPrice = input<number>(25);

  // Line 2: Writable signal holding local reactive state
  readonly quantity = signal<number>(1);

  // Line 3: Computed signal derived from unitPrice and quantity (memoized!)
  readonly totalCost = computed(() => this.quantity() * this.unitPrice());

  constructor() {
    // Line 4: Effect runs automatically whenever quantity changes
    effect(() => {
      console.log(`[Analytics Event]: Cart quantity changed to ${this.quantity()}`);
      localStorage.setItem('cached_cart_qty', this.quantity().toString());
    });
  }

  // Line 5: Update signal using functional updater
  incrementQuantity(): void {
    this.quantity.update(q => q + 1);
  }

  // Line 6: Decrement with boundary validation
  decrementQuantity(): void {
    if (this.quantity() > 1) {
      this.quantity.update(q => q - 1);
    }
  }
}""",
        "pitch": "Angular 21 Signals introduce fine-grained reactivity as the core primitive. Unlike legacy Zone.js dirty-checking which traverses the component tree, Signals establish a dynamic dependency graph. Computed signals are lazily evaluated and memoized, while template bindings update only the specific DOM text nodes whose underlying signal has changed, dramatically boosting runtime performance.",
        "star": "Financial trading portal rendering 2,500 real-time cryptocurrency orderbook updates per second with frequent browser frame drops.",
        "action": "Refactored legacy RxJS component tree bindings to Angular 21 Signals and computed properties.",
        "metrics": "Browser UI thread CPU consumption dropped from 72% down to 14%; frame rate stabilized at a rock-solid 60 FPS."
    },

    {
        "file": "02_angular21_zoneless_architecture.md",
        "title": "Angular 21 Zoneless Architecture: Why Zone.js Was Removed & How It Works",
        "hinglish": "Zone.js browser ke saare asynchronous APIs (setTimeout, Promise, fetch, addEventListener) ko monkey-patch karta tha taaki Angular ko pata chale kab render karna hai. Angular 21 me Zoneless default hai: ab monkey-patching ki zaroorat nahi hai, Angular signals aur template events ke through directly schedule karta hai.",
        "analogy": "Removing an annoying spy that followed you to every single meeting and phone call, replacing it with a simple doorbell you ring only when you actually arrive.",
        "points": [
            "Why Zone.js Was Problematic: Added ~100KB to bundle size, monkey-patched native browser APIs making debugging stack traces painful, and triggered unnecessary change detection runs on un-rendered events.",
            "Zoneless Core Engine: Angular 21 change detection is triggered explicitly via Signal mutations, template event bindings, or `ChangeDetectorRef.markForCheck()`.",
            "Enabling Zoneless: Configured in `app.config.ts` via `provideZonelessChangeDetection()`.",
            "Performance Impact: Drastically smaller initial JavaScript bundle size, faster initial page boot, and cleaner async stack traces in developer tools."
        ],
        "diagram": """[Legacy Zone.js (Angular 2 - 17)]
 Browser Event / Timer ──> Zone.js Intercepts ──> Traverses Entire Component Tree (Heavy!)

[Modern Angular 21 Zoneless]
 Signal Mutation (.set / .update) ──> Scheduler ──> Notifies Only Subscribed Views (Surgical!)""",
        "code": """// app.config.ts - Configuring Zoneless Angular 21 Application
import { ApplicationConfig, provideZonelessChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    // Line 1: Activate official Zoneless change detection (Zero Zone.js dependency!)
    provideZonelessChangeDetection(),
    
    // Line 2: Standard router provider
    provideRouter(routes),
    
    // Line 3: Modern HTTP client with native fetch API backing
    provideHttpClient(withFetch())
  ]
};""",
        "pitch": "In Angular 21, the framework achieves its long-term vision of complete Zoneless operation. By removing Zone.js monkey-patching, Angular eliminates over 100KB of polyfill overhead and prevents blanket tree re-checks. Changes are driven explicitly by Signals and template event loops, resulting in pristine stack traces, reduced bundle sizes, and optimal core web vitals.",
        "star": "High-traffic media streaming dashboard suffering from micro-stutters during background telemetry heartbeats patched by Zone.js.",
        "action": "Migrated application configuration to `provideZonelessChangeDetection()` and converted background pollers to native Signals.",
        "metrics": "Initial JavaScript bundle payload dropped by 115KB; Total Blocking Time (TBT) improved by 65%."
    },

    {
        "file": "03_angular21_defer_block_and_lazy_loading.md",
        "title": "Angular 21 Template @defer Blocks: Declarative Component Lazy Loading",
        "hinglish": "Pehle kisi component ko lazy load karne ke liye alag se routing module ya complex dynamic import likhna padta tha. Angular me `@defer` block se aap template me hi likh sakte ho ki kab component load ho: jab user scroll karke wahan pahuche (`on viewport`), ya jab hover kare (`on hover`), ya jab button click kare (`on interaction`).",
        "analogy": "Hotel buffet heating trays: instead of cooking every dish at 6:00 AM, heavy evening dishes are prepared and brought out only when the dinner guests actually arrive at the table.",
        "points": [
            "`@defer`: Wraps heavy components or third-party libraries (charts, rich-text editors, video players) to split them into independent async chunks.",
            "Triggers (`on` & `when`): `on viewport` (uses IntersectionObserver), `on interaction`, `on hover`, `on idle` (requestIdleCallback), `on timer(5s)`, or `when isVisible()` signal.",
            "`@placeholder`: Lightweight UI element rendered immediately before the deferred chunk is fetched.",
            "`@loading`: Shown while the network is downloading the deferred chunk (with optional `minimum` and `after` debounce timers).",
            "`@error`: Fallback template rendered if the network request fails."
        ],
        "diagram": """[Initial Page Load]
 ├── Core Page Header & Content Rendered
 └── [@placeholder] Displays small skeleton box
           │
           ▼ (User scrolls down into view: 'on viewport')
 [@loading] Fetches heavy chunk from CDN (Network download)
           │
           ▼
 [@defer Content] Heavy Chart Component hydrates and renders smoothly!""",
        "code": """<!-- Angular 21 Declarative Template Lazy Loading -->
<div class="dashboard-container">
  <h1>Executive Performance Dashboard</h1>

  <!-- Line 1: @defer block fetches heavy analytics chart ONLY when scrolled into viewport -->
  @defer (on viewport; prefetch on idle) {
    <!-- Heavy Chart component (automatically extracted into a separate JS bundle chunk!) -->
    <app-heavy-financial-chart [chartData]="financeData()" />
  } @placeholder (minimum 300ms) {
    <!-- Line 2: Rendered immediately to avoid layout shifts (CLS) -->
    <div class="chart-skeleton-placeholder">
      <p>Chart will load when visible...</p>
    </div>
  } @loading (after 100ms; minimum 500ms) {
    <!-- Line 3: Displayed while downloading the chunk -->
    <div class="spinner-container">
      <span>Downloading analytical engines...</span>
    </div>
  } @error {
    <!-- Line 4: Graceful error fallback -->
    <div class="error-banner">
      <p>Failed to load chart component. Please check your network.</p>
    </div>
  }
</div>""",
        "pitch": "The `@defer` block in modern Angular revolutionizes template-level code splitting. Developers can declaratively defer the loading of components until specific triggers occur—such as viewport intersection, user interaction, or browser idle time. Paired with `@placeholder` and `@loading` blocks with built-in duration guards, it completely eliminates Cumulative Layout Shift (CLS) and slashes initial page weight.",
        "star": "Heavy enterprise ERP billing page loading a 2.8MB bundle due to unrendered PDF previewers and charting widgets.",
        "action": "Wrapped non-critical below-the-fold widgets in template `@defer (on viewport; prefetch on idle)` blocks.",
        "metrics": "Initial JavaScript payload plummeted from 2.8MB to 340KB (88% reduction); Largest Contentful Paint (LCP) dropped from 4.8s to 1.1s."
    },

    {
        "file": "04_angular21_standalone_components_and_inject.md",
        "title": "Angular 21 Standalone Components & The inject() Function",
        "hinglish": "Angular me ab `NgModule` ki zaroorat nahi hoti. Har component by default `standalone: true` hota hai aur apne zaroori dependencies direct apne `imports: [...]` array me declare karta hai. Aur constructor injection ki jagah modern `inject(ServiceName)` function use kiya jata hai.",
        "analogy": "Plugging an appliance directly into a wall outlet (`inject()`) instead of hiring an electrician to rewire the entire house electrical board (`NgModule`).",
        "points": [
            "Standalone by Default: Components, Directives, and Pipes manage their own dependencies directly without being declared in an `NgModule`.",
            "`inject()` Function: Functional dependency injection usable in class field initializers, constructor-less classes, and functional route guards.",
            "Functional Route Guards: Replaces class-based guards (`CanActivate` interfaces) with simple lambda functions (`canActivate: [() => inject(AuthService).isLoggedIn()]`).",
            "Better Tree-Shaking: Build tools (esbuild/Rollup) can identify and remove truly unused components and services."
        ],
        "diagram": """[Legacy Angular (NgModule)]
 Component A ──> Belongs to [SharedModule] ──> Imports 50 other unused components ──> Bloated Bundle!

[Modern Angular 21 (Standalone + inject)]
 Component A ──(imports)──> [Component B]
             └──(inject)───> [AuthService] (Lean, direct, 100% tree-shakable!)""",
        "code": """import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { UserService } from './services/user.service';

@Component({
  selector: 'app-user-profile',
  standalone: true, // Line 1: Standalone component (no NgModule required!)
  imports: [CommonModule], // Line 2: Explicitly import only what this component uses
  template: `
    <div *ngIf="user() as u">
      <h2>Welcome, {{ u.name }}</h2>
      <button (click)="logout()">Sign Out</button>
    </div>
  `
})
export class UserProfileComponent {
  // Line 3: Modern Dependency Injection using inject() function
  private readonly userService = inject(UserService);
  private readonly router = inject(Router);

  // Line 4: Direct signal binding from injected service
  readonly user = this.userService.currentUser;

  logout(): void {
    this.userService.clearSession();
    // Line 5: Navigation via injected router instance
    this.router.navigate(['/login']);
  }
}

// Line 6: Modern Functional Route Guard using inject()
export const authGuard = () => {
  const authService = inject(UserService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  return router.parseUrl('/login');
};""",
        "pitch": "Standalone Components streamline Angular's component model by removing NgModule indirection, enabling direct dependency imports and superior tree-shaking. The modern `inject()` API eliminates constructor boilerplate, allowing clean class field initialization and enabling functional route guards and interceptors.",
        "star": "Massive monolithic enterprise Angular codebase with 45 interdependent NgModules where changing one component recompiled the entire application.",
        "action": "Migrated the codebase to Standalone Components and replaced legacy class-based route guards with concise functional `inject()` guards.",
        "metrics": "Build times during local development dropped by 74%; production bundle size decreased by 32%."
    },

    {
        "file": "05_angular21_rxjs_interop_to_signal.md",
        "title": "Angular 21 RxJS Interop: toSignal(), toObservable() & When to Use Which",
        "hinglish": "Signals aane ka matlab ye nahi hai ki RxJS khatam ho gaya. Dono ka alag role hai: Signals State Management aur UI Data Binding ke liye best hain (synchronous, glitch-free), jabki RxJS Asynchronous Streams, WebSockets, Debouncing, aur Race Conditions handle karne ke liye best hai. `@angular/core/rxjs-interop` se hum dono ko aapas me connect karte hain.",
        "analogy": "RxJS is a high-speed express train moving packages across cities (asynchronous stream processing). Signals are the local delivery courier placing the package neatly onto your desk (synchronous UI presentation).",
        "points": [
            "`toSignal(observable$)`: Converts an RxJS Observable stream into a synchronous Signal for effortless template binding (no `| async` pipe needed).",
            "`toObservable(signal)`: Converts a Signal into an RxJS Observable to leverage operators like `debounceTime`, `switchMap`, `catchError`.",
            "When to Use Signals: Synchronous state, computed values, UI template bindings, input/output properties.",
            "When to Use RxJS: Handling asynchronous event streams, complex timing operators (`debounceTime`, `throttleTime`), WebSockets, cancelable HTTP requests (`switchMap`)."
        ],
        "diagram": """[Incoming Asynchronous Stream: Search Keystrokes]
                        │
                        ▼ (RxJS Operators)
       [debounceTime(300ms)] ──> [distinctUntilChanged()] ──> [switchMap(fetchApi)]
                                                                    │
                                                                    ▼
                                                            [toSignal(results$)]
                                                                    │
                                                                    ▼
                                                    [Angular 21 Template Binding]
                                                     <ul>@for (item of results())</ul>""",
        "code": """import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toSignal, toObservable } from '@angular/core/rxjs-interop';
import { signal } from '@angular/core';
import { debounceTime, distinctUntilChanged, switchMap, catchError, of } from 'rxjs';

@Component({
  selector: 'app-search-autocomplete',
  standalone: true,
  template: `
    <input (input)="onSearchInput($event)" placeholder="Search products..." />
    
    <!-- Render signal array cleanly with @for block -->
    <ul>
      @for (item of searchResults(); track item.id) {
        <li>{{ item.name }} - ${{ item.price }}</li>
      } @empty {
        <li>No results found.</li>
      }
    </ul>
  `
})
export class SearchAutocompleteComponent {
  private readonly http = inject(HttpClient);

  // Line 1: Signal holding current search text input
  readonly searchQuery = signal<string>('');

  // Line 2: Convert signal to RxJS Observable to apply debounceTime and switchMap
  private readonly searchStream$ = toObservable(this.searchQuery).pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(query => {
      if (!query.trim()) return of([]);
      return this.http.get<any[]>(`/api/search?q=${encodeURIComponent(query)}`).pipe(
        catchError(() => of([]))
      );
    })
  );

  // Line 3: Convert the processed RxJS stream back to a Signal for template rendering!
  readonly searchResults = toSignal(this.searchStream$, { initialValue: [] });

  onSearchInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.searchQuery.set(input.value);
  }
}""",
        "pitch": "Signals and RxJS are complementary tools in modern Angular. RxJS excels at complex asynchronous orchestration, debouncing, and cancellation pipelines. Signals excel at synchronous state derivation and fine-grained template binding. With `@angular/core/rxjs-interop`, we pipe RxJS streams through `toSignal()` to achieve clean, declarative components without subscription leaks or `async` pipe boilerplate.",
        "star": "Live search autocomplete leaking memory and suffering race conditions where slow older API requests overwrote newer search keystroke results.",
        "action": "Built an RxJS `switchMap` cancellation pipeline and converted the output stream to an Angular Signal using `toSignal()`.",
        "metrics": "Eliminated 100% of out-of-order race conditions; reduced network payload overhead by 80% via debouncing."
    },

    {
        "file": "interview-questions/angular21_top_interview_questions.md",
        "title": "Angular 21 Interview Master Guide: Zoneless, Signals, @defer & Modern Architecture",
        "hinglish": "Angular 21 ke technical interview me sabse zyada questions modern architecture par aate hain: Zoneless change detection vs Zone.js, Signals vs RxJS, Template @defer blocks, inject() vs Constructor, aur Standalone components.",
        "analogy": "An architectural certification audit: proving you understand the transition from legacy monolithic enterprise Angular to modern, ultra-lean reactive Angular 21.",
        "points": [
            "Q1: What is Zoneless Angular and how does change detection work without Zone.js?",
            "Q2: Differentiate between Writable Signals, Computed Signals, and Effects.",
            "Q3: When would you use RxJS instead of Signals in an Angular 21 project?",
            "Q4: Explain the triggers and utility of the `@defer` block in templates.",
            "Q5: Why is the `inject()` function preferred over constructor injection in modern Angular?"
        ],
        "diagram": """[Key Concepts Tested in Angular 21 Interviews]
 ├── 1. Signals & Reactivity (signal, computed, effect, input, model)
 ├── 2. Zoneless Execution (provideZonelessChangeDetection)
 ├── 3. Template Code Splitting (@defer, @placeholder, @loading, @error)
 ├── 4. Dependency Injection Evolution (inject() in field & guards)
 └── 5. RxJS Interop (toSignal & toObservable bridging)""",
        "code": """// Quick-Reference Summary Code for Angular 21 Interviews
// 1. Standalone + inject()
export class ModernComponent {
  private auth = inject(AuthService); // Modern DI
  
  // 2. Signals
  count = signal(0);
  double = computed(() => this.count() * 2); // Memoized
  
  // 3. Signal Inputs & Models
  userId = input.required<string>(); // Replaces @Input()
  theme = model<'light' | 'dark'>('light'); // Two-way binding signal
}""",
        "pitch": "Angular 21 marks the culmination of Angular's modernization: Zoneless by default, Signals as the core reactive primitive, declarative template lazy-loading with @defer, and constructor-less dependency injection via inject(). Understanding these architectural shifts proves readiness to lead modern enterprise web applications.",
        "star": "Leading an enterprise Angular migration for a 35-developer organization from Angular 14 (NgModules + Zone.js) to Angular 21.",
        "action": "Devised automated migration schematics converting NgModules to Standalone and adopted Zoneless Signals across all shared UI libraries.",
        "metrics": "Decreased average build duration by 60%; reduced client bundle sizes by 42%; boosted Lighthouse performance score from 58 to 96."
    }
]

def generate_angular_guides():
    os.makedirs(BASE_DIR, exist_ok=True)
    count = 0
    for item in ANGULAR_21_GUIDES:
        target_path = os.path.join(BASE_DIR, item["file"])
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        points_md = "\n".join([f"- {p}" for p in item["points"]])

        content = f"""# {item['title']}

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {item['hinglish']}
>
> **Real-World Analogy:** {item['analogy']}

---

## 2. 📌 Core Mechanics & Key Points
{points_md}

---

## 3. 📊 Visual Architecture Diagram

```text
{item['diagram']}
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```typescript
{item['code']}
```

---

## 5. 🎯 Senior Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {item['title'].split(':')[0]} and how you use it in Angular 21?"
>
> **You:** "{item['pitch']}"

---

## 6. 💼 Real-World Project Challenge (STAR Production Story)
* **Situation:** {item['star']}
* **Task / Challenge:** Modernizing frontend architecture, resolving change detection performance bottlenecks, and optimizing bundle weight.
* **Action Taken:** {item['action']}
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In our enterprise Angular applications, {item['star'].lower()} I spearheaded the modernization by {item['action'].lower()}, which successfully {item['metrics'].lower()}."*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"Generated Angular 21 Guide: {target_path}")

    print(f"Successfully generated {count} Angular 21 deep-dive files!")

if __name__ == "__main__":
    generate_angular_guides()
