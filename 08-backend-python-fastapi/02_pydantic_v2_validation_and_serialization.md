# FastAPI with Pydantic V2: Rust-Powered Validation & Type Serialization

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Pydantic V1 ek manual airport luggage inspector jaisa tha jo Python mein line-by-line check karta tha.
Pydantic V2 ek **High-Speed Industrial Scanner** hai jiska core engine pure **Rust (`pydantic-core`)** mein likha gaya hai. Ye 5x se 20x fast validation karta hai aur invalid data ko API router ke andar ghusne hi nahi deta.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Rust Core Architecture**: Pydantic V2 rewrote the entire validation and serialization engine in Rust (`pydantic-core`).
2. **`model_validator` & `field_validator`**: Replaces V1's `@validator` and `@root_validator`.
3. **Serialization Mode**: `model.model_dump()` replaces `.dict()`, and `model.model_dump_json()` replaces `.json()`.
4. **Strict vs Lax Mode**: By default, Pydantic coerces compatible types (e.g. string `"42"` to int `42`). Setting `strict=True` forbids coercion.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from typing import Optional
from datetime import datetime

# Line 6: User registration model with Pydantic V2 syntax
class UserRegistrationSchema(BaseModel):
    # Line 8: Strict type constraints with Field
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Line 15: Field validator for username
    @field_validator("username")
    @classmethod
    def validate_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return v.lower()

    # Line 23: Model validator checking cross-field rules (passwords match)
    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegistrationSchema":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match!")
        return self
```
