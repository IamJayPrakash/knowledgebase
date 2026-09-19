# 🤝 Contributing to The Universal Tech Knowledge Base

First off, thank you for considering contributing to the **Universal Tech & Senior Interview Knowledge Base**! 🎉

This repository is an open-source, community-driven master reference for Software Engineers, Tech Leads, and Architects worldwide. We welcome contributions of all levels—whether you are fixing a typo, adding a production war story, proposing an edge case, or authoring a new deep-dive question.

---

## 📜 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [What Can I Contribute?](#what-can-i-contribute)
3. [The Mandatory 6-Pillar Format](#the-mandatory-6-pillar-format)
4. [Contribution Workflow](#contribution-workflow)
5. [Local Development & Link Validation](#local-development--link-validation)
6. [Issue Labels & Finding Tasks](#issue-labels--finding-tasks)
7. [Submitting a Pull Request](#submitting-a-pull-request)

---

## 1. Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). Please be welcoming, respectful, and constructive.

---

## 2. What Can I Contribute?

- **New Interview Questions:** Adding high-yield technical interview questions for any of our 16 tracks.
- **Code Refinements & Bug Fixes:** Improving optimal solutions, fixing typos, or updating outdated syntax (e.g. Next.js 15, Angular 21, React 19).
- **Edge Cases & Visuals:** Adding ASCII/Mermaid architecture diagrams and tricky production edge cases.
- **STAR Production War Stories:** Adding authentic, metrics-grounded incident responses and engineering decisions.
- **Translations / Accessibility:** Enhancing clarity or explanations for global software engineers.

---

## 3. The Mandatory 6-Pillar Format

Every single concept or interview question in this repository **must** strictly adhere to our 6-Pillar standard:

```markdown
### Q<Number>: <Clear, Precise Question Title>
#### 1. Layman's Analogy (Hinglish + Real-World ELI5)
- Intuitive, zero-jargon explanation using relatable real-life analogies.

#### 2. Core Mechanics & Key Points
- Concise technical breakdown of internal engine/runtime execution and edge cases.

#### 3. Visual Architecture Diagram
- ASCII flowcharts, memory layouts, or Mermaid diagrams mapping data flow.

#### 4. Practical Implementation & Code Snippet
- Complete, runnable code with **100% line-by-line comments** explaining what each line accomplishes.

#### 5. Senior Interview Answering Pitch
- Exact, natural professional English phrasing to answer the question authoritatively in a high-stakes interview.

#### 6. Real-World Project Challenge (STAR Production Story)
- Authentic Situation, Task, Action, and quantified Business/System Metrics (Latency, Throughput, Memory).
```

---

## 4. Contribution Workflow

### Step 1: Fork & Clone

```bash
# 1. Fork repository on GitHub: https://github.com/IamJayPrakash/knowledgebase/fork
# 2. Clone your fork locally:
git clone https://github.com/<your-username>/knowledgebase.git
cd knowledgebase
```

### Step 2: Create a Feature Branch

Use a clear, descriptive branch naming convention:

```bash
# For a new feature or question bank:
git checkout -b feat/add-react19-compiler-qna

# For a bug fix or link correction:
git checkout -b fix/correct-v8-gc-diagram
```

### Step 3: Make Changes & Test

Edit or create markdown files following the directory conventions:

- Place concept guides in `<track-name>/`
- Place interview questions in `<track-name>/interview-questions/`
- Update the relevant `<track-name>/README.md` and `<track-name>/interview-questions/README.md` to link your new file.

---

## 5. Local Development & Link Validation

### Previewing the Documentation Portal Locally

You can preview the interactive Single-Page Application locally without installing any heavy build tools:

```bash
# Run a simple Python static server:
python -m http.server 8000
# Open http://localhost:8000 in your browser!
```

### Validating Links

Before submitting a PR, verify that zero broken links exist:

```bash
python -c "
import re, sys
from pathlib import Path

root = Path('.')
md_files = [p for p in root.rglob('*.md') if '.git' not in p.parts]
link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
broken = 0

for p in md_files:
    lines = p.read_text(encoding='utf-8').splitlines()
    in_code = False
    for line_num, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in link_regex.finditer(line):
            target = m.group(2).strip()
            if target.startswith(('http://', 'https://', '#', 'mailto:')):
                continue
            path_part = target.split('#')[0]
            if not path_part:
                continue
            resolved = (p.parent / path_part).resolve()
            if not resolved.exists():
                print(f'BROKEN: {p}:{line_num} -> {target}')
                broken += 1

if broken > 0:
    print(f'Found {broken} broken links!')
    sys.exit(1)
else:
    print('All links validated successfully!')
"
```

---

## 6. Issue Labels & Finding Tasks

Check out our [Issues tab](https://github.com/IamJayPrakash/knowledgebase/issues) to find tasks to work on:

- `good first issue` — Perfect starting points for newcomers.
- `help wanted` — High-priority community requests.
- `track: <name>` — Domain-specific topics (e.g. `track: ai-genai`, `track: react`).
- `documentation` — Improvements to formatting, diagrams, or explanations.

---

## 7. Submitting a Pull Request

1. Commit your changes with clear, conventional messages:

   ```bash
   git commit -m "feat(react): add Q21-Q30 covering Server Actions and useOptimistic"
   ```

2. Push to your fork:

   ```bash
   git push origin feat/add-react19-compiler-qna
   ```

3. Open a Pull Request against the `main` branch of `IamJayPrakash/knowledgebase`.
4. Fill out the automated PR template completely.
5. Our automated GitHub Actions workflows will verify link integrity and trigger a preview deployment!

Thank you for contributing to make this the ultimate engineering knowledge base! 🚀
