# Machine Coding: Hard TypeScript Custom Utility Types

---

## Challenge 1: `DeepPartial<T>`

Recursively transforms all properties of an object (including nested objects and arrays) to optional.

```typescript
// Solution:
type DeepPartial<T> = T extends (...args: any[]) => any
  ? T
  : T extends Array<infer U>
  ? _DeepPartialArray<U>
  : T extends object
  ? _DeepPartialObject<T>
  : T;

type _DeepPartialArray<T> = Array<DeepPartial<T>>;
type _DeepPartialObject<T> = { [K in keyof T]?: DeepPartial<T[K]> };

// Test
interface ComplexUser {
  id: number;
  profile: {
    avatar: string;
    preferences: {
      theme: "light" | "dark";
      notifications: boolean;
    };
  };
}

const partialData: DeepPartial<ComplexUser> = {
  profile: {
    preferences: {
      theme: "dark"
    }
  }
};
```

---

## Challenge 2: `FlattenObjectKeys<T>` (Dot Notation Path Extractor)

Transforms a nested object type into dot-notated string literal paths (`"profile.preferences.theme"`).

```typescript
type FlattenObjectKeys<T extends object> = {
  [K in keyof T & string]: T[K] extends object
    ? `${K}` | `${K}.${FlattenObjectKeys<T[K]>}`
    : `${K}`;
}[keyof T & string];

type AppPaths = FlattenObjectKeys<ComplexUser>;
// Result: "id" | "profile" | "profile.avatar" | "profile.preferences" | "profile.preferences.theme" | "profile.preferences.notifications"
```

---

## Challenge 3: `RequireAtLeastOne<T, Keys>`

Enforces that at least one of the specified properties must be present.

```typescript
type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = Pick<
  T,
  Exclude<keyof T, Keys>
> &
  {
    [K in Keys]-?: Required<Pick<T, K>> &
      Partial<Pick<T, Exclude<Keys, K>>>;
  }[Keys];

interface ContactForm {
  name: string;
  email?: string;
  phone?: string;
}

// User must provide at least email OR phone
type ValidatedContact = RequireAtLeastOne<ContactForm, "email" | "phone">;

const valid1: ValidatedContact = { name: "Jay", email: "jay@test.com" };
const valid2: ValidatedContact = { name: "Jay", phone: "1234567890" };
// const invalid: ValidatedContact = { name: "Jay" }; // Error: Property 'email' or 'phone' missing!
```
