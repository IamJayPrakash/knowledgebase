# Jest & React Testing Library: Unit, Integration, and Mocking Mastery

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Code test na karna **Bina Safety Net Ke Circus Mein Rope Par Chalne Jaisa Hai**.
**Unit Test** ek screw check karne jaisa hai: "Kya ye screw theek se tight ho raha hai?".
**Integration Test** poori bicycle chala ke dekhne jaisa hai: "Pedal marne par chain ghoom rahi hai aur pahiya chal raha hai ya nahi?".
**React Testing Library** ka golden rule hai: **"Test your app the way real users use it!"** Internal state variables check mat karo; check karo ki button screen par dikh raha hai aur click karne par expected text aaya ya nahi.

---

## 💻 2. Line-by-Line Commented Code Snippets

```javascript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UserProfileLoader } from "./UserProfileLoader";

// Line 6: Mocking external fetch API
beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.clearAllMocks();
});

describe("UserProfileLoader Integration Test", () => {
  test("renders user profile data after successful API fetch", async () => {
    // Line 17: Mock resolved API payload
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 101, username: "jay_lead", email: "jay@test.com" })
    });

    // Line 23: Render component into simulated DOM
    render(<UserProfileLoader userId={101} />);

    // Line 26: Verify loading spinner appears initially
    expect(screen.getByText(/loading profile/i)).toBeInTheDocument();

    // Line 29: Wait for asynchronous fetch resolution and UI update
    await waitFor(() => {
      expect(screen.getByText(/jay_lead/i)).toBeInTheDocument();
    });

    // Line 34: Assert API was called with correct parameters
    expect(global.fetch).toHaveBeenCalledWith("/api/v1/users/101");
  });
});
```
