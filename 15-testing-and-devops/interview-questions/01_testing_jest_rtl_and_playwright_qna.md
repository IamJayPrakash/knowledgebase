# Automated Testing: Jest, React Testing Library, and Playwright (Q1 - Q25)

> A master question bank covering modern automated testing: Test pyramid, Jest mocking, React Testing Library philosophies, Mock Service Worker (MSW), Playwright E2E automation, trace analysis, and load testing for Senior QA & Lead Engineers.

---

### Q1: What is the Test Pyramid and how should an engineering team distribute its testing investment?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** Agar aap sirf browser E2E tests likhoge, toh build chalne me 2 ghante lagenge aur har chhota sa UI change test fail kar dega (flaky). Testing pyramid bolta hai: sabse zyada saste aur super-fast Unit tests likho (base), beech me Integration tests, aur top par thode se critical user-journey E2E tests.
- **Real-World Analogy:** An automobile manufacturing plant: inspect individual bolts and sensors (unit), test the engine connected to the transmission (integration), and test-drive a few fully assembled cars on the highway (E2E).

#### 2. Core Mechanics & Key Points
- **Unit Tests (70%):** Test pure functions, utility algorithms, and isolated classes without network or database dependencies. Execute in milliseconds.
- **Integration Tests (20%):** Test multiple modules or components working together (e.g., React component with Redux store and mocked API via MSW).
- **End-to-End (E2E) Tests (10%):** Spin up real browsers (Playwright/Cypress) and execute mission-critical user paths (Sign up, Checkout, Payment). High fidelity but expensive and prone to network flakiness.

#### 3. Visual Architecture Diagram
```
              /\
             /  \     E2E Tests (10%) - Slowest, Highest Cost, Highest Fidelity
            /----\    (Playwright / Cypress)
           /      \   Integration Tests (20%) - Component + State + Network
          /--------\  (React Testing Library + MSW)
         /          \ Unit Tests (70%) - Fastest, Lowest Cost, Isolated Logic
        /------------\ (Jest / Vitest)
```

#### 5. Senior Interview Answering Pitch
> "I structure our testing pyramid to maximize return on investment while maintaining continuous deployment confidence. The base consists of lightning-fast unit tests for pure domain algorithms, the middle layer leverages React Testing Library and MSW for integration behavior testing, and the apex reserves Playwright E2E suites for core revenue-critical funnels like user checkout and onboarding."

---

### Q2: What is the core philosophy of React Testing Library (RTL) and how does it prevent brittle tests?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** Purana Enzyme framework component ke private internal state aur methods ko inspect karta tha (`wrapper.state('count')`). RTL ka simple mantra hai: "The more your tests resemble the way your software is used, the more confidence they can give you." User ko internal state nahi dikhti, usko screen par button ka text aur labels dikhte hain. Isliye RTL user ki tarah screen interact karta hai.
- **Real-World Analogy:** Testing a microwave: press the "Start" button and check if the food gets warm, rather than unscrewing the casing to measure transistor resistance inside the circuit board.

#### 2. Core Mechanics & Key Points
- **Avoid Testing Implementation Details:** Refactoring component state (e.g., switching from `useState` to `useReducer` or Signals) should never break existing tests if the rendered output and user behavior remain unchanged.
- **Accessible Queries:** Prioritizes queries that mirror user accessibility:
  1. `getByRole` (accessible roles like `button`, `heading`, `textbox`).
  2. `getByLabelText` (form inputs).
  3. `getByPlaceholderText` / `getByText`.
  4. Avoids `getByTestId` except when no accessible role or label exists.

#### 3. Practical Implementation & Code Snippet
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

test('submits valid user credentials and displays success banner', async () => {
  // 1. Setup user event instance
  const user = userEvent.setup();

  // 2. Render component
  render(<LoginForm onLoginSuccess={jest.fn()} />);

  // 3. Query elements by accessible role & label (No implementation details!)
  const emailInput = screen.getByRole('textbox', { name: /email address/i });
  const passwordInput = screen.getByLabelText(/password/i);
  const submitButton = screen.getByRole('button', { name: /sign in/i });

  // 4. Simulate realistic user interactions
  await user.type(emailInput, 'engineer@company.com');
  await user.type(passwordInput, 'SuperSecretPass123!');
  await user.click(submitButton);

  // 5. Assert user-visible outcome
  expect(await screen.findByRole('alert')).toHaveTextContent(/login successful/i);
});
```

#### 5. Senior Interview Answering Pitch
> "React Testing Library eliminates brittle tests by asserting exclusively on user-observable DOM behavior and accessibility roles (`getByRole`, `getByLabelText`) rather than internal component states, props, or lifecycle hooks. This ensures tests survive internal architecture refactors without false negatives."

---

### Q3: Explain the query hierarchy in React Testing Library: `getBy*` vs `queryBy*` vs `findBy*`.
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:**
  - `getBy`: "Element abhi hona chahiye! Agar nahi mila toh test turant fail karo."
  - `queryBy`: "Element check karo; agar nahi hai toh `null` return karo (element ke absence check karne ke liye)."
  - `findBy`: "Element thoda ruk kar aane wala hai (async), 1 second tak wait karo, fir return karo."
- **Real-World Analogy:** Looking for a friend: `getBy` shouts in the room and cries if they aren't there; `queryBy` peeks through the window to confirm they are absent; `findBy` waits at the bus stop for them to arrive.

#### 2. Query Decision Matrix
| Query Family | Element Found | Element NOT Found | Multiple Found | Asynchronous? | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`getBy*`** | Returns element | **Throws Exception** | Throws Exception | ❌ No | Verifying immediate synchronous presence |
| **`queryBy*`** | Returns element | **Returns `null`** | Throws Exception | ❌ No | Asserting **absence** (`expect(queryBy...).not.toBeInTheDocument()`) |
| **`findBy*`** | Resolves Promise | **Rejects Promise** | Rejects Promise | ✅ Yes (Async) | Waiting for elements appearing after API fetch or animation |

#### 5. Senior Interview Answering Pitch
> "We select RTL query methods based on synchronous presence and error handling. `getBy*` is the default for synchronous assertions because it fails fast. `queryBy*` is reserved strictly for asserting non-existence where throwing would abort the test. `findBy*` wraps queries in `waitFor` promises to test elements that appear asynchronously after network responses."

---

### Q4: Why is Mock Service Worker (MSW) superior to manual `global.fetch` or Axios mocking?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** `jest.spyOn(global, 'fetch')` me aap JavaScript ke function ko fake bana dete ho. Isse network boundary test nahi hoti aur headers ya status codes me errors chhoot jate hain. MSW browser/Node ke actual network level par Service Worker laga deta hai. Code sochta hai ki wo real server se baat kar raha hai!
- **Real-World Analogy:** Manual mocking is asking an actor to pretend to be a customer; MSW is routing real customer telephone calls through an internal testing switchboard.

#### 2. Core Mechanics & Key Points
- MSW intercepts network traffic at the operating system / browser Service Worker level (or Node `http/https` module level via class interceptors).
- Your application's actual HTTP client code (fetch, axios, Apollo, React Query) executes 100% untouched.
- Shared between unit tests, integration tests, and local browser development mock servers.

#### 3. Practical Implementation & Code Snippet
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('https://api.myapp.com/v1/user', () => {
    return HttpResponse.json({
      id: 'usr_101',
      name: 'Sarah Connor',
      role: 'ADMIN',
    });
  }),
];

// tests/UserProfile.test.tsx
import { setupServer } from 'msw/node';
import { handlers } from '../mocks/handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches and displays user profile', async () => {
  // App makes real fetch() call; intercepted seamlessly by MSW!
});
```

#### 5. Senior Interview Answering Pitch
> "MSW intercepts requests at the network layer rather than monkey-patching JavaScript client libraries. This validates that serialization, custom headers, status codes, and HTTP interceptors execute genuinely in the test runtime, while allowing the exact same mock definitions to be reused across unit tests, Storybook, and local development."

---

### Q5: How does Playwright's Auto-Waiting mechanism eliminate flaky tests compared to Selenium and Cypress?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** Purane Selenium tests me `sleep(5000)` likhna padta tha kyunki button load hone me time leta tha. Agar network slow hua toh test fail, fast hua toh 5 second waste! Playwright button click karne se pehle automatically check karta hai: kya element visible hai? Kya wo stable hai (move nahi ho raha)? Kya wo clickable hai (disabled nahi hai)? Aur tabhi click karta hai.
- **Real-World Analogy:** A patient photographer: waiting until everyone stops blinking and moving before pressing the shutter button, rather than blindly firing the camera on a timer.

#### 2. Core Mechanics & Key Points
Before performing any action (e.g., `page.click(selector)`), Playwright performs automated **Actionability Checks**:
1. **Attached:** Element is attached to the DOM.
2. **Visible:** Element is visible (not `display: none`, `visibility: hidden`, or zero opacity).
3. **Stable:** Element is not animating or moving across frames.
4. **Receives Events:** Element is not obscured or occluded by other elements (like modals or overlays).
5. **Enabled:** Element is not disabled.

#### 3. Practical Implementation & Code Snippet
```typescript
import { test, expect } from '@playwright/test';

test('flawless checkout submission without manual sleeps', async ({ page }) => {
  await page.goto('https://shop.example.com/checkout');

  // ANTI-PATTERN in legacy suites:
  // await page.waitForTimeout(5000); // NEVER DO THIS IN PLAYWRIGHT!

  // Playwright automatically waits for:
  // 1. input to be attached, visible, editable, and ready
  await page.getByLabel('Card Number').fill('4242424242424242');

  // 2. Playwright waits for pay button to become enabled after card validation
  await page.getByRole('button', { name: 'Complete Order' }).click();

  // 3. Web-first assertion automatically polls until condition passes
  await expect(page.getByText('Order # confirmed')).toBeVisible();
});
```

#### 5. Senior Interview Answering Pitch
> "Playwright eliminates test flakiness through built-in actionability checks. Before dispatching click or fill events, Playwright continuously verifies that target elements are attached, visible, stable, un-occluded, and enabled. Coupled with web-first auto-polling assertions (`expect(locator).toBeVisible()`), it eradicates the need for arbitrary `sleep()` timeouts."

---

### Q6: How do Playwright Storage State and Global Setup enable fast authenticated testing?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** Agar aapke pass 200 E2E tests hain aur har test browser kholkar email aur password type karke login karega, toh 30 minute sirf login karne me nikal jayenge. Playwright Global Setup me hum ek bar login karke browser ke cookies aur localStorage ko ek JSON file (`storageState.json`) me save kar lete hain. Baki sare 199 tests us JSON file ko inject karke seedhe logged-in state me start hote hain!
- **Real-World Analogy:** Showing a saved VIP security wristband at the express gate rather than standing in the 45-minute passport queue every single time you enter the venue.

#### 2. Practical Implementation & Code Snippet
```typescript
// auth.setup.ts (Runs ONCE before all test suites)
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate user once', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@company.com');
  await page.getByLabel('Password').fill('SecurePassword123');
  await page.getByRole('button', { name: 'Log in' }).click();

  await page.waitForURL('/dashboard');
  // Save browser cookies and local storage tokens into JSON snapshot:
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      dependencies: ['setup'],
      use: {
        // All test workers reuse authenticated storage state instantly!
        storageState: 'playwright/.auth/user.json',
      },
    },
  ],
});
```

#### 5. Senior Interview Answering Pitch
> "Authenticating through the UI on every test creates massive CI latency and rate-limiting issues. Using Playwright's `storageState`, we run authentication once in a global setup project, save browser cookies and storage tokens to a JSON artifact, and inject that state into parallel worker browser contexts, slashing overall E2E execution times by up to 75%."

---

### Q7: What is Playwright's Trace Viewer and how does it revolutionize CI debugging?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** CI server par test fail hota hai toh developer ko sirf ek error message dikhta hai: "Button not found". Playwright Trace Viewer ek flight black box ki tarah hai: ye fail hone wale test ka har millisecond ka video, DOM snapshot, console logs, network calls, aur actionability timing record kar leta hai. Developer apne local computer par test ko frame-by-frame piche karke dekh sakta hai!
- **Real-World Analogy:** A time-traveling sports replay camera with full telemetry data (speed, heart rate, wind velocity) for every player on the field.

#### 2. Core Mechanics & Key Points
- Enabled in `playwright.config.ts` via `trace: 'on-first-retry'` or `trace: 'retain-on-failure'`.
- Packages snapshots into a `.zip` artifact containing:
  1. Full DOM snapshot before and after every action.
  2. Network waterfall with request/response bodies and headers.
  3. Visual action filmstrip with exact click coordinates.
  4. Browser console logs and terminal output.

#### 5. Senior Interview Answering Pitch
> "Playwright's Trace Viewer acts as an interactive forensic black box for failed CI tests. By configuring `trace: 'on-first-retry'`, Playwright records DOM snapshots, network requests, console logs, and action timings exclusively when a test fails, allowing engineers to locally inspect the exact historical state of the remote browser at any millisecond of test execution."

---

### Q8: How do you structure E2E test suites using the Page Object Model (POM)?
#### 1. Layman's Analogy (Hinglish + Real-World)
- **Hinglish Intuition:** Agar checkout page par submit button ka selector badal jaye aur aapne 50 tests me direct `page.click('#submit')` likha ho, toh 50 tests manually edit karne padenge. Page Object Model me checkout page ke sare selectors aur actions ek single class `CheckoutPage` me rehte hain. Selector badle toh sirf ek file change karni hoti hai.
- **Real-World Analogy:** Calling a travel concierge rather than negotiating with airlines, hotels, and car rentals individually.

#### 2. Practical Implementation & Code Snippet
```typescript
// pages/CheckoutPage.ts
import { type Page, type Locator } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly cardNumberInput: Locator;
  readonly submitButton: Locator;
  readonly orderSuccessBadge: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cardNumberInput = page.getByLabel('Card Number');
    this.submitButton = page.getByRole('button', { name: 'Pay Now' });
    this.orderSuccessBadge = page.getByRole('status');
  }

  async goto() {
    await this.page.goto('/checkout');
  }

  async completePayment(cardNumber: string) {
    await this.cardNumberInput.fill(cardNumber);
    await this.submitButton.click();
  }
}

// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { CheckoutPage } from '../pages/CheckoutPage';

test('user successfully buys item', async ({ page }) => {
  const checkout = new CheckoutPage(page);
  await checkout.goto();
  await checkout.completePayment('4242424242424242');

  await expect(checkout.orderSuccessBadge).toContainText('Payment Received');
});
```

#### 5. Senior Interview Answering Pitch
> "The Page Object Model encapsulates UI selectors and interaction workflows into reusable class abstractions. This decouples test specifications from volatile DOM selector implementations, drastically reducing maintenance overhead and enforcing DRY principles across enterprise test suites."
