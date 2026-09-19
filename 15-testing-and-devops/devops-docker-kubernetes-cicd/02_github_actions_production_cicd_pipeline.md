# Production CI/CD Pipeline with GitHub Actions and Docker Buildx

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
GitHub Actions ek **Automated Assembly Inspection Robot** hai:
Jaise hi developer code commit karke push karta hai:
1. Robot code download karta hai.
2. Linter aur TypeScript compiler chala ke spelling aur types check karta hai.
3. Automated test suits chala ke verify karta hai ki koi feature toota toh nahi.
4. Docker container build karta hai aur production server (Kubernetes) par naya code live deploy kar deta hai bina kisi manual button dabaye!

---

## 💻 2. Line-by-Line Commented Workflow YAML

```yaml
name: Production CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Run ESLint & TypeScript Validation
        run: npm run lint && npm run type-check

      - name: Execute Automated Unit Tests
        run: npm test -- --ci --coverage

  build-and-push-docker:
    needs: test-and-lint
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: actions/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push Multi-Arch Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```
